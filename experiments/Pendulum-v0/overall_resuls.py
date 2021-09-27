import math
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('bmh')

import tqdm

ROLLING_WINDOW_SIZE = 100


def con_sin_to_theta(cos_th, sin_th):
    acos_th, asin_th = math.acos(cos_th), math.asin(sin_th)
    if asin_th > 0:
        return acos_th
    else:
        return -acos_th


def angle_normalize(x):
    return ((x + np.pi) % (2 * np.pi)) - np.pi


def episode_rewards(df):
    eps = df[df['step'] == 0]

    theta_ranges = np.linspace(-np.pi, np.pi, SPLIT_THETA_RANGE_IN + 1)
    colors = ['C0', 'C1', 'C2', 'C3']
    for i in range(len(theta_ranges) - 1):
        th_s, th_e = theta_ranges[i], theta_ranges[i + 1]
        episodes_list = eps[(eps['state_th'] > th_s) & (eps['state_th'] < th_e)]['episode'].to_list()

        df_res = df[df['episode'].isin(episodes_list)]

        episode_rewards = df_res.groupby('episode').agg({'reward': 'sum'})

        plt.plot(episode_rewards,
                 alpha=0.2,
                 linewidth=2)

        rolling_size = min(100, int(ROLLING_AVG_SIZE_RATIO * len(episode_rewards)))
        rolling_avg = episode_rewards.rolling(rolling_size,
                                              center=True,
                                              min_periods=rolling_size // 2).mean()

        plt.plot(rolling_avg, color=colors[i], label=f'{th_s:.02f} < | th 0 | < {th_e:.02f}', linewidth=3)

    plt.title("Score per episode")
    plt.xlabel("Episodes")
    plt.ylabel("Reward")
    plt.legend()


def plot_episode(episode_df):
    plt.scatter(episode_df['state_th'], episode_df['step'], alpha=0.5)
    # plt.plot(episode_df['state_th'], episode_df['step'], alpha=0.2)
    plt.title(f"Episode {episode_df['episode'].max()}")
    # plt.legend()
    plt.grid()
    pass

def plot_episode_reward(episode_df):
    total_reward = episode_df['reward']
    theta_cost = -angle_normalize(episode_df['state_th']) ** 2
    thetadot_cost = -0.1*episode_df['state_2']**2
    u_cost = -0.001 * (episode_df['action_0'] ** 2)

    plt.plot(total_reward, episode_df['step'], ':', color='black', label=f'total {total_reward.sum():.2f}')
    plt.plot(theta_cost, episode_df['step'], ':', color='r', label='theta cost')
    plt.plot(thetadot_cost, episode_df['step'], ':', color='b', label='theta\' cost')
    plt.plot(u_cost, episode_df['step'], ':', color='g', label='action cost')

    plt.title(f"Episode {episode_df['episode'].max()}")
    plt.legend()
    plt.grid()
    pass

def plot(file):
    df = pd.read_csv(file, index_col=False)
    df['state_th'] = list(map(con_sin_to_theta, df['state_0'], df['state_1']))


    plt.figure(figsize=(10, 10))

    plt.subplot(2, 1, 1)
    episode_rewards(df)

    episodes = df['episode'].unique()
    top_episodes = [1]
    for ep in top_episodes:
        episode_number = min(int(ep*len(episodes)), len(episodes)-1)
        episode_df = df[df['episode']==episode_number]
        plt.subplot(2, 2, 3)
        plot_episode(episode_df)
        plt.subplot(2, 2, 4)
        plot_episode_reward(episode_df)

    plt.tight_layout()
    plt.show()

if __name__=="__main__":
    dir = 'csvs/'
    files = [dir+f for f in os.listdir(dir)]
    print(files)

    file = files[-1]
    plot(file)
