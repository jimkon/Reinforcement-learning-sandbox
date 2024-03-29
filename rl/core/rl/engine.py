import time
from tqdm import tqdm

import numpy as np

from rl.core.utilities.logging import log
from rl.core.utilities.timestamp import timestamp_str
from rl.core.configs.storage_configs import DATA_COLUMNS,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_EPISODES,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_STEPS,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_STATES, \
                                        DB_EXPERIMENT_TABLE_NAME_COL_ACTIONS,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_REWARDS,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_DONE

"""
TODO
save expreiment stats (name, total reward, total steps, time_start, time_end) in experiments table
"""


def __env_name_to_table(s):
    if '<' in s and '>' in s:
        s = s.split('<')[-1]
        s = s.split('>')[0]

    s = s.replace('-', '_')
    return s


def __verbosity_string_to_num(verbosity):
    if isinstance(verbosity, str):
        verbosity = {
            'progress': 1,
            'total': 2,
            'episode': 3,
            'step': 4
        }[verbosity]
    return verbosity


def run_episodes(env, agent, n_episodes, storage_dict=None, render=False, verbosity='progress'):
    """
    storage_dict(optional): dict to store the transition data in the form of {'episodes': [...], 'steps_list': [...], 'states': [...], 'actions': [...], 'rewards': [...], 'dones': [...]}
    verbosity: None or 0, 'progress' or 1, 'total' or 2, 'episode' or 3, 'step' or 4
    """

    start_time = time.time()

    verbosity = __verbosity_string_to_num(verbosity)

    agent.set_env(env)

    if not storage_dict:
        storage_dict = {col: [] for col in DATA_COLUMNS}

    episode_rewards = []

    total_reward, total_steps = 0, 0

    n_actions = None

    if verbosity == 1:
        _iter = tqdm(range(n_episodes), f"Agent {agent.name} execution in {str(env)} environment")
    else:
        _iter = range(n_episodes)

    episode = 0
    for episode in _iter:
        episode_reward = 0
        step = 0
        state = env.reset()
        done = False

        while not done:

            action = agent.act(state)

            if not n_actions:
                n_actions = len(np.atleast_1d(action))

            next_state, reward, done, _ = env.step(action)

            agent.observe(state, action, reward, next_state, done)

            episode_reward += reward

            if verbosity >= 4:
                log (
                    f"Episode:{episode}, Step:{step}, state:{state}, action:{action}, reward:{reward}, next state:{next_state}, done:{done}",
                    tags='markdown_heading3')

            action = np.atleast_1d(action)

            storage_dict[DB_EXPERIMENT_TABLE_NAME_COL_EPISODES].append(episode)
            storage_dict[DB_EXPERIMENT_TABLE_NAME_COL_STEPS].append(step)
            storage_dict[DB_EXPERIMENT_TABLE_NAME_COL_STATES].append(state)
            storage_dict[DB_EXPERIMENT_TABLE_NAME_COL_ACTIONS].append(action)
            storage_dict[DB_EXPERIMENT_TABLE_NAME_COL_REWARDS].append(reward)
            storage_dict[DB_EXPERIMENT_TABLE_NAME_COL_DONE].append(done)

            if done:
                storage_dict[DB_EXPERIMENT_TABLE_NAME_COL_EPISODES].append(episode)
                storage_dict[DB_EXPERIMENT_TABLE_NAME_COL_STEPS].append(step+1)
                storage_dict[DB_EXPERIMENT_TABLE_NAME_COL_STATES].append(next_state)
                storage_dict[DB_EXPERIMENT_TABLE_NAME_COL_ACTIONS].append(['null'] * n_actions)
                storage_dict[DB_EXPERIMENT_TABLE_NAME_COL_REWARDS].append(.0)
                storage_dict[DB_EXPERIMENT_TABLE_NAME_COL_DONE].append(-1)
                step += 1
            else:
                state = next_state
                step += 1

            if render and hasattr(env, 'render'):
                env.render()

        episode_rewards.append(episode_reward)
        total_reward += episode_reward
        total_steps += step
        if verbosity >= 3:
            avg_rewards = np.mean(episode_rewards[int(0.1 * len(episode_rewards)):])
            log (
                f"Agent {agent.name} completed the episode {episode}. Steps {step}, Total reward {episode_reward}, rolling avg reward(10%) {avg_rewards:.02f}",
                tags='markdown_heading3')

    elapsed_time = time.time() - start_time
    if verbosity >= 1:
        episode += 1
        avg_rewards = np.mean(episode_rewards[int(0.1 * len(episode_rewards)):])
        log (
            f"Agent {agent.name} completed {episode} episodes in {elapsed_time:.02f} seconds in {str(env)}. Total reward {total_reward} (avg ep. reward(100%) {total_reward / episode}, rolling avg ep. reward(10%) {avg_rewards:.02f}). Steps {total_steps}",
            tags='markdown_heading3')

    return storage_dict

# TODO DELETE
# def run_and_store_episodes(env, agent, n_episodes, experiment_name=None, store_results_func=None, verbosity='progress'):
#     if experiment_name is None:
#         experiment_name = f"{agent.name}_{__env_name_to_table(str(env))}"
#
#     res_dict = {col: [] for col in DATA_COLUMNS}
#     start_time, duration_secs = None, None
#     start_time_str = timestamp_str()
#     try:
#         start_time = time.time()
#         res_dict = run_episodes(env,
#                                 agent,
#                                 n_episodes,
#                                 storage_dict=res_dict,
#                                 render=False,
#                                 verbosity=verbosity)
#         duration_secs = time.time()-start_time
#     except Exception as e:
#         pass
#     finally:
#         if store_results_func is None:
#             pass
#         elif store_results_func.lower() == 'dataframe':
#             store_results_as_dataframe(res_dict,
#                                        name=experiment_name)
#         elif store_results_func.lower() == 'database':
#             store_results_in_database(res_dict,
#                                       to_table=__env_name_to_table(str(env)),
#                                       experiment_id=experiment_name,
#                                       agent_id=agent.name(),
#                                       env_id=str(env),
#                                       start_time=start_time_str,
#                                       duration_secs=duration_secs,
#                                       comment=None)

