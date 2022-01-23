import time
from tqdm import tqdm

import numpy as np

from src.rl.core.logging import log
from src.rl.core.files import StoreResultsInDataframe, StoreResultsInDatabase


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


def run_episodes(env, agent, n_episodes, experiment_name=None, store_results=None, storage_dict=None,
                 render=False, verbosity='progress'):
    """
    verbosity: None or 0, 'progress' or 1, 'total' or 2, 'episode' or 3, 'episode_step' or 4
    """

    start_time = time.time()

    if isinstance(verbosity, str):
        verbosity = {
            'progress': 1,
            'total': 2,
            'episode': 3,
            'episode_step': 4
        }[verbosity]
    else:
        verbosity = 0

    agent.set_env(env)

    if not storage_dict:
        storage_dict = {
            'episodes': [],
            'steps_list': [],
            'states': [],
            'actions': [],
            'rewards': [],
            'dones': []
        }

    episode_rewards = []

    total_reward, total_steps = 0, 0

    n_actions = None

    if verbosity == 1:
        _iter = tqdm(range(n_episodes), f"Agent {agent.name()} execution in {str(env)} environment")
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
                    f"Episode:{episode}, Step:{step}, state:{state}, action:{action}, reward:{reward}, next state:{next_state}, done:{done}")

            action = np.atleast_1d(action)

            storage_dict['episodes'].append(episode)
            storage_dict['steps_list'].append(step)
            storage_dict['states'].append(state)
            storage_dict['actions'].append(action)
            storage_dict['rewards'].append(reward)
            storage_dict['dones'].append(done)

            if done:
                storage_dict['episodes'].append(episode)
                storage_dict['steps_list'].append(step+1)
                storage_dict['states'].append(next_state)
                storage_dict['actions'].append(['null'] * n_actions)
                storage_dict['rewards'].append(.0)
                storage_dict['dones'].append(-1)
                step += 1
            else:
                state = next_state
                step += 1

            if render and hasattr(env, render):
                env.render()

        episode_rewards.append(episode_reward)
        total_reward += episode_reward
        total_steps += step
        if verbosity >= 3:
            avg_rewards = np.mean(episode_rewards[int(0.1 * len(episode_rewards)):])
            log (
                f"Agent {agent.name()} completed the {episode} episode. Steps {step}, Total reward {episode_reward}, rolling avg reward(10%) {avg_rewards:.02f}")

    elapsed_time = time.time() - start_time
    if verbosity >= 1:
        episode += 1
        avg_rewards = np.mean(episode_rewards[int(0.1 * len(episode_rewards)):])
        log (
            f"Agent {agent.name()} completed {episode} episodes in {elapsed_time:.02f} seconds in {str(env)}. Total reward {total_reward} (avg ep. reward(100%) {total_reward / episode}, rolling avg ep. reward(10%) {avg_rewards:.02f}). Steps {total_steps}")

    return storage_dict


# def run_and_store_episodes():
#     if experiment_name is None:
#         experiment_name = f"{agent.name()}_{env_name_to_table(str(env))}"
#     # store_results = store_results if store_results else DEFAULT_STORE_RESULTS_OBJECT
#     if store_results == 'database':
#         store_results_obj = StoreResultsInDatabase(experiment_name=experiment_name,
#                                                    to_table=env_name_to_table(str(env)),
#                                                    agent_id=agent.name(),
#                                                    env_id=str(env))
#     elif store_results == 'dataframe':
#         store_results_obj = StoreResultsInDataframe(experiment_name=experiment_name)
#     else:
#         store_results_obj = store_results
#
#     if store_results_obj:
#         store_results_obj.save(episodes[last_log_step:],
#                                steps_list[last_log_step:],
#                                states[last_log_step:],
#                                actions[last_log_step:],
#                                rewards[last_log_step:],
#                                dones[last_log_step:])
#         store_results_obj.finalize()

