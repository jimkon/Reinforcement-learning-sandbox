import time
from tqdm import tqdm

import numpy as np

# import agents
# import custom_envs


class Agent:
    def act(self, state):
        return np.random.random(1)

    def observe(self, *args):
        pass

    def name(self):
        return 'test'


class Env:
    def reset(self):
        pass

    def step(self, action):
        return np.random.random(3), np.random.random(1)[0], np.random.random(1)[0]>0.5, None

    def render(self):
        pass


def run_episodes(env, agent, n_episodes, render=False, verbosity='progress'):
    """
    verbosity: None or 0, 'progress' or 1, 'total' or 2, 'episode' or 3, 'episode_step' or 4
    """
    if isinstance(verbosity, str):
        verbosity = {
            'progress': 1,
            'total': 2,
            'episode': 3,
            'episode_step': 4
        }[verbosity]
    else:
        verbosity = 0

    start_time = time.time()
    total_reward, total_steps = 0, 0

    if verbosity == 1:
        iter_ = tqdm(range(n_episodes))
    else:
        iter_ = range(n_episodes)

    for episode in iter_:
        episode_reward = 0
        step = 0
        done = False

        state = env.reset()
        while not done:

            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)

            agent.observe(state, action, reward, next_state, done)
            if verbosity >= 4:
                print(f"Episode:{episode}, Step:{step}, state:{state}, action:{action}, reward:{reward}, next state:{next_state}, done:{done}")
            state = next_state
            episode_reward += reward
            step += 1
            if render:
                env.render()

        total_reward += episode_reward
        total_steps += step
        if verbosity >= 3:
            print(f"Agent {agent.name()} completed the {episode} episode. Total reward {episode_reward}, Steps {step}")

    elapsed_time = time.time()-start_time
    if verbosity >= 2:
        episode += 1
        print(f"Agent {agent.name()} completed {episode} episodes in {elapsed_time}. Total reward {total_reward} ({total_reward/episode} avg episode reward). Steps {total_steps}")


agent = Agent()
env = Env()
run_episodes(env, agent, 1000, verbosity='episode')
