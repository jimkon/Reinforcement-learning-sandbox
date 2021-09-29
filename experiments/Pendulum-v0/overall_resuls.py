import math
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('bmh')

from tqdm import tqdm

ROLLING_WINDOW_SIZE = 100


def con_sin_to_theta(cos_th, sin_th):
    acos_th, asin_th = math.acos(cos_th), math.asin(sin_th)
    if asin_th > 0:
        return acos_th
    else:
        return -acos_th


def labeling_thetas(x):
    return 'BL' if x < -np.pi / 2 else 'UL' if x < 0 else 'UR' if x < np.pi / 2 else 'BR'


def detect_balance(thetas, theta_threshold=.5, thetadot_threshold=0.02, balance_cnt_threshold=10):
    thetadots = np.diff(thetas)
    thetadots = np.abs(np.append(thetadots, thetadots[-1]))
    thetas_abs = thetas.abs()

    cnt = 0
    for theta, thetadot in zip(thetas_abs[::-1], thetadots[::-1]):
        if theta > theta_threshold or thetadot > thetadot_threshold:
            break
        else:
            cnt += 1

    if cnt >= balance_cnt_threshold:
        return len(thetas) - cnt
    else:
        return -1


def process_df(df_in, theta_threshold=.5, thetadot_threshold=0.02, balance_cnt_threshold=10):
    print('Enriching dataframe.')
    df_in['acos'] = np.arccos(df_in['state_0'])
    df_in['asin_sign'] = 1 - 2 * (np.arcsin(df_in['state_1']) < 0).astype(int)

    df_in['state_th'] = df_in['acos'] * df_in['asin_sign']
    df_in['theta_label'] = np.digitize(df_in['state_th'], bins=[-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
    df_in['theta_label'] = df_in['theta_label'].map({1: 'BL', 2: 'UL', 3: 'UR', 4: 'BR'})

    del df_in['acos']
    del df_in['asin_sign']

    df_in['state_th2'] = df_in['state_th'].shift(1)
    df_in['state_thdot_abs'] = (df_in['state_th2'] - df_in['state_th']).abs()
    df_in['state_th_abs'] = df_in['state_th'].abs()
    df_in['is_unbalanced'] = 1 - ((df_in['step'] > 0) & (df_in['state_th_abs'] <= theta_threshold) & (
                df_in['state_thdot_abs'] <= thetadot_threshold)).astype(int)
    df_in['unbalanced_step'] = df_in['is_unbalanced'] * df_in['step']

    balancing_step_df = df_in.groupby('episode').agg({'unbalanced_step': 'max'}).reset_index().rename(
        columns={'unbalanced_step': 'balance_step'})
    balancing_step_df['balance_step'] = balancing_step_df['balance_step'].replace(199, -1)
    balancing_step_df.loc[balancing_step_df['balance_step'] > (200 - balance_cnt_threshold), 'balance_step'] = -1

    episode_stats_df = df_in.groupby('episode').agg(
        {'reward': 'sum', 'state_th': 'first', 'theta_label': 'first'}).reset_index().rename(
        columns={'state_th': 'theta_0', 'theta_label': 'theta_0_label'})
    episode_stats_df = episode_stats_df.merge(balancing_step_df, on='episode', how='left')
    episode_stats_df['solved'] = (episode_stats_df['balance_step'] >= 0).astype(int)

    del df_in['state_th2']
    del df_in['state_thdot_abs']
    del df_in['state_th_abs']
    del df_in['is_unbalanced']
    del df_in['unbalanced_step']

    return df_in, episode_stats_df


def episode_rewards(df):
    eps = df[df['step'] == 0]
    for l, c in zip(['UL', 'UR', 'BL', 'BR'], ['C1', 'C2', 'C0', 'C3']):
        episodes_list = eps[eps['theta_label'] == l]['episode'].to_list()

        df_res = df[df['episode'].isin(episodes_list)]

        episode_rewards = df_res.groupby('episode').agg({'reward': 'sum'})

        plt.plot(episode_rewards,
                 alpha=0.3,
                 linewidth=2,
                 c=c)

        rolling_avg = episode_rewards.rolling(ROLLING_WINDOW_SIZE,
                                              center=True,
                                              min_periods=ROLLING_WINDOW_SIZE // 5).mean()

        plt.plot(rolling_avg, color='black', linewidth=3)
        plt.plot(rolling_avg, color=c, label=l, linewidth=2)

    plt.title("Score per episode")
    # plt.xlabel("Episodes")
    plt.ylabel("Reward")
    plt.legend()


def solution_ratios(episode_stats_df):
    solutions = 100 * episode_stats_df['solved'].rolling(window=ROLLING_WINDOW_SIZE, center=True, min_periods=1).mean()
    plt.plot(solutions, c='black', alpha=0.8, linewidth=3)
    plt.plot(solutions, c='grey', alpha=0.8, linewidth=2, label='Overall')

    for l, c in zip(['UL', 'UR', 'BL', 'BR'], ['C1', 'C2', 'C0', 'C3']):
        plt.plot(
            100 * episode_stats_df[episode_stats_df['theta_0_label'] == l]['solved'].rolling(window=100, center=True,
                                                                                             min_periods=1).mean(),
            linewidth=1, c=c, label=l, alpha=1)

    ax = plt.gca()
    xticks = list(ax.get_xticks())#list(range(0, len(solutions) + 1, 500))
    for y in [50, 75, 90, 95, 99, 100]:
        episode_numbers = np.where(solutions >= y)[0]
        if len(episode_numbers) == 0:
            break
        x = episode_numbers[0]
        plt.plot([0, x], [y, y], alpha=0.35, c='y')
        plt.plot([x, x], [0, y], alpha=0.45, c='y')
        # plt.scatter(x, y, marker='o', c='black')
        # plt.scatter(x, y, marker='x', c='y')
        xticks.append(x)
    plt.xticks(np.sort(xticks), rotation=-90)

    plt.legend()
    # plt.xlabel('Episodes')
    plt.ylabel('%')
    plt.title('% of episodes been solved')
    plt.yticks(range(0, 101, 10))


def balance_steps(episode_stats_df):
    for l, c in zip(['UL', 'UR', 'BL', 'BR'], ['C1', 'C2', 'C0', 'C3']):
        temp_df = episode_stats_df[episode_stats_df['theta_0_label'] == l]
        temp_df = temp_df[temp_df['solved'] > 0]
        plt.scatter(temp_df['episode'], temp_df['balance_step'], c=c, label=l, marker='s', alpha=0.25)
        line = temp_df['balance_step'].rolling(window=max(min(ROLLING_WINDOW_SIZE, int(len(temp_df)*0.5)), 1),
                                               center=True,
                                               min_periods=1).mean()
        plt.plot(line, c='black', linewidth=4)
        plt.plot(line, c=c, linewidth=2)

    plt.xticks(np.linspace(0, len(episode_stats_df), 11))
    # plt.xticks(rotation=-90)
    plt.xlabel('Episodes')
    plt.ylabel('Count')
    plt.title('Step count before solution')
    plt.legend()


def balancing_progress(df, episode_stats_df):
    temp_df = df.merge(episode_stats_df[['episode', 'balance_step']], on='episode')
    temp_df = temp_df[temp_df['balance_step'] > -1]
    min_ep, max_ep = temp_df['episode'].min(), temp_df['episode'].max()
    # temp_df['after_balancing'] = temp_df['balance_step']>=temp_df['step']
    temp_df = temp_df[temp_df['balance_step'] <= temp_df['step']]
    temp_df = temp_df.groupby('episode').agg({'state_th': 'mean'})
    # temp_df

    plt.plot(temp_df['state_th'].rolling(window=ROLLING_WINDOW_SIZE, center=True, min_periods=1).mean(), c='C3',
             label='mean')

    mean_abs = temp_df['state_th'].abs().rolling(window=ROLLING_WINDOW_SIZE, center=True, min_periods=1).mean()

    plt.plot(mean_abs, c='C0', label='mean(abs)')
    plt.plot([min_ep, max_ep], [mean_abs.mean()] * 2, alpha=0.5, c='grey',
             label=f'overall mean {mean_abs.mean():.02f}')

    plt.plot(temp_df['state_th'].abs().rolling(window=ROLLING_WINDOW_SIZE, center=True, min_periods=1).max(),
             c='C1', label='max(abs)')

    plt.title('Theta averages after balancing')
    plt.xlabel('Episodes')
    plt.ylabel('Theta (rads)')
    plt.yticks(np.linspace(-.5, .5, 11))
    plt.legend()


def plot(df):
    exp_id = df['experiment_id'][0]

    enriched_df, episode_stats_df = process_df(df)

    fig = plt.figure(figsize=(15, 10))
    fig.suptitle(exp_id)
    fig.patch.set_facecolor('xkcd:light grey')

    plt.subplot(2, 2, 1)
    episode_rewards(enriched_df)

    plt.subplot(2, 2, 2)
    solution_ratios(episode_stats_df)

    plt.subplot(2, 2, 3)
    balance_steps(episode_stats_df)

    plt.subplot(2, 2, 4)
    balancing_progress(enriched_df, episode_stats_df)

    plt.tight_layout()
    plt.show()

if __name__=="__main__":
    dir = 'csvs/'
    files = [dir+f for f in os.listdir(dir)]
    print(files)

    file = files[3]
    print(f'Reading file: {file}')
    df = pd.read_csv(file, index_col=False)
    plot(df)
