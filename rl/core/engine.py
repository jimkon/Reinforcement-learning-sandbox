import time
from tqdm import tqdm
from rl.core.db import default_db

import numpy as np

# import agents
# import custom_envs

#
class Agent:
    def act(self, state):
        return [state[0], state[0]]

    def observe(self, *args):
        pass

    def name(self):
        return 'test_agent'


class Env:
    def __init__(self):
        self.cnt = 0.

    def reset(self):
        self.cnt = 0.
        return [self.cnt+0.1, self.cnt+0.2, self.cnt+0.3]

    def step(self, action):
        self.cnt += 1
        return [self.cnt+0.1, self.cnt+0.2, self.cnt+0.3], self.cnt, np.random.random(1)[0]>0.5, None

    def render(self):
        pass

    def __repr__(self):
        return 'test_env'


# class DB:
#     def __init__(self, dbname):
#         pass
#
#     def execute(self, query):
#         print('mocked DB:\n', query)


def store_results_to_database(db, data, to_table, agent_id='unknown_agent_id', experiment_id=None):
    if not experiment_id:
        experiment_id = f'{to_table}:{agent_id}:{time.strftime("%Y-%m-%d:%H-%M-%S")}'

    experiment_id = f'"{experiment_id}"'
    agent_id = f'"{agent_id}"'

    episodes, steps_list, states, actions, rewards, dones = data

    states_dim, actions_dim = len(states[0]), len(actions[0])

    dones = list(map(int, dones))
    states = list(map(list, zip(*states)))
    # print(actions)
    # actions = list(map(list, zip(*[a if a else ['null']*actions_dim for a in actions])))
    print(actions)

    db.execute(f"""CREATE TABLE IF NOT EXISTS {to_table}
                   (exp_id text NOT NULL,
                    agent_id text NOT NULL,
                    episode integer NOT NULL,
                    step integer NOT NULL,
                    {' '.join([f'state_{i} double precision NOT NULL,' for i in range(states_dim)])}
                    {' '.join([f'action_{i} double precision,' for i in range(actions_dim)])}
                    reward double precision NOT NULL,
                    done integer NOT NULL)
                """)

    insert_str = f"""INSERT INTO {to_table}
                    (exp_id, agent_id, episode, step,
                    {' '.join([f'state_{i},' for i in range(states_dim)])}
                    {' '.join([f'action_{i},' for i in range(actions_dim)])}
                    reward, done)
                    VALUES """ +\
                 ',\n'.join(map(str, zip([experiment_id] * len(episodes),
                                         [agent_id] * len(episodes),
                                         episodes,
                                         steps_list,
                                         *states,
                                         *actions,
                                         rewards,
                                         dones)))
    db.execute(insert_str.replace("'" , " "))


def run_episodes(env, agent, n_episodes, log_database='default', log_frequency=-1, render=False, verbosity='progress'):
    """
    log_database: database object, if 'default' the dbs/rl.db will be used.
    verbosity: None or 0, 'progress' or 1, 'total' or 2, 'episode' or 3, 'episode_step' or 4
    """

    if log_database=='default':
        log_database = default_db()

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
                print(f"Episode:{episode}, Step:{step}, state:{state}, action:{action}, reward:{reward}, next state:{next_state}, done:{done}")

            action = np.atleast_1d(action)

            episodes.append(episode), steps_list.append(step), states.append(state), actions.append(action), rewards.append(reward), dones.append(done)

            if done:
                state = None
                episodes.append(episode), steps_list.append(step+1), states.append(next_state), actions.append(['null']*n_actions), rewards.append(.0), dones.append(-1)
            else:
                state = next_state
                episode_reward += reward
                step += 1

            if render:
                env.render()

        total_reward += episode_reward
        total_steps += step+1
        if verbosity >= 3:
            print(f"Agent {agent.name()} completed the {episode} episode. Total reward {episode_reward}, Steps {step+1}")

        if log_database and episode % log_frequency == log_frequency-1:
            store_results_to_database(log_database, (episodes[last_log_step:],
                                                     steps_list[last_log_step:],
                                                     states[last_log_step:],
                                                     actions[last_log_step:],
                                                     rewards[last_log_step:],
                                                     dones[last_log_step:]),
                                  to_table=str(env),
                                  agent_id=agent.name())
            last_log_step = total_steps

    elapsed_time = time.time()-start_time
    if verbosity >= 2:
        episode += 1
        print(f"Agent {agent.name()} completed {episode} episodes in {elapsed_time:.02f} seconds in {str(env)}. Total reward {total_reward} ({total_reward/episode} avg episode reward). Steps {total_steps}")

    if log_database:
        store_results_to_database(log_database,
                                  (episodes[last_log_step:],
                                                 steps_list[last_log_step:],
                                                 states[last_log_step:],
                                                 actions[last_log_step:],
                                                 rewards[last_log_step:],
                                                 dones[last_log_step:]),
                                  to_table=str(env),
                                  agent_id=agent.name())

    return states, actions, rewards, dones


agent = Agent()
env = Env()
# db = DB()
run_episodes(env, agent, 2, log_database='default', log_frequency=-1, verbosity='episode_step')
