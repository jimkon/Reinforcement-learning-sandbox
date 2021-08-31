import time
from tqdm import tqdm

import numpy as np

from rl.core.files import StoreResultsInDataframe, StoreResultsInDatabase


def run_episodes(env, agent, n_episodes, experiment_name=None, store_results='dataframe', log_frequency=-1,
                 render=False, verbosity='progress'):
    """
    verbosity: None or 0, 'progress' or 1, 'total' or 2, 'episode' or 3, 'episode_step' or 4
    """

    if store_results == 'database':
        store_results_obj = StoreResultsInDatabase()
    elif store_results == 'dataframe':
        store_results_obj = StoreResultsInDataframe(experiment_name=experiment_name)
    else:
        store_results_obj = store_results

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

    log_frequency = -1 if log_frequency == 0 else log_frequency

    episodes, steps_list, states, actions, rewards, dones = [], [], [], [], [], []

    last_log_step = 0

    total_reward, total_steps = 0, 0

    n_actions = None

    if verbosity == 1:
        iter_ = tqdm(range(n_episodes), f"Agent {agent.name()} execution in {str(env)} environment")
    else:
        iter_ = range(n_episodes)

    episode = 0
    for episode in iter_:
        episode_reward = 0
        step = 0
        state = None
        done = False

        while not done:

            if not state:
                state = env.reset()

            action = agent.act(state)

            if not n_actions:
                print(action)
                n_actions = len(np.atleast_1d(action))

            next_state, reward, done, _ = env.step(action)

            agent.observe(state, action, reward, next_state, done)

            if verbosity >= 4:
                print(
                    f"Episode:{episode}, Step:{step}, state:{state}, action:{action}, reward:{reward}, next state:{next_state}, done:{done}")

            action = np.atleast_1d(action)

            episodes.append(episode), steps_list.append(step), states.append(state), actions.append(
                action), rewards.append(reward), dones.append(done)

            if done:
                state = None
                episodes.append(episode), steps_list.append(step + 1), states.append(next_state), actions.append(
                    ['null'] * n_actions), rewards.append(.0), dones.append(-1)
                step += 1
            else:
                state = next_state
                episode_reward += reward
                step += 1

            if render:
                env.render()

        total_reward += episode_reward
        total_steps += step + 1
        if verbosity >= 3:
            print(
                f"Agent {agent.name()} completed the {episode} episode. Total reward {episode_reward}, Steps {step + 1}")

        if store_results_obj and episode % log_frequency == log_frequency - 1:
            store_results_obj.save(episodes[last_log_step:],
                                   steps_list[last_log_step:],
                                   states[last_log_step:],
                                   actions[last_log_step:],
                                   rewards[last_log_step:],
                                   dones[last_log_step:])
            last_log_step = total_steps

    elapsed_time = time.time() - start_time
    if verbosity >= 2:
        episode += 1
        print(
            f"Agent {agent.name()} completed {episode} episodes in {elapsed_time:.02f} seconds in {str(env)}. Total reward {total_reward} ({total_reward / episode} avg episode reward). Steps {total_steps}")

    if store_results_obj:
        store_results_obj.save(episodes[last_log_step:],
                               steps_list[last_log_step:],
                               states[last_log_step:],
                               actions[last_log_step:],
                               rewards[last_log_step:],
                               dones[last_log_step:])
        store_results_obj.finalize()

    return states, actions, rewards, dones
