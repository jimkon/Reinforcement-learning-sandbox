from rl.src.core.rl.engine import run_and_store_episodes

from rl.src.core.rl.env import AbstractEnv


def cnt():
    i = 0
    while True:
        yield i
        i += 1


cnt_gen = cnt()


class TestEnv(AbstractEnv):
    def __init__(self):
        self.ep = -1
        self.n_step = 0

    def reset(self):
        self.ep += 1
        self.n_step = 0
        res = [next(cnt_gen), next(cnt_gen)]
        # row_num_obj[0] += 1
        return res

    def step(self, action):
        self.n_step += 1
        # print('step', row_num_obj[0])
        res = [next(cnt_gen), next(cnt_gen)]
        done = self.n_step >= 3**self.ep
        reward = next(cnt_gen)
        # row_num_obj[0] += 1
        return res, reward, done, None

    def __repr__(self):
        return 'test_env'


class TestAgent:
    def __init__(self):
        pass
        # self.df = df
        # self.row_num = 0

    def act(self, state):
        res = next(cnt_gen)
        # self.row_num += 1
        return res

    def set_env(self, env):
        pass

    def observe(self, *args):
        pass

    def name(self):
        return 'test_agent'


def experiment_args():
    agent = TestAgent()
    env = TestEnv()
    experiment_name = 'test_experiment'
    res = {
        'env': env,
        'agent': agent,
        'n_episodes': 3,
        'experiment_name': experiment_name,
        'verbosity': 'episode_step'
    }

    return res


def run_experiment():
    agent = TestAgent()
    env = TestEnv()
    experiment_name = 'test_experiment'

    run_and_store_episodes(env, agent, 3, experiment_name, store_results_func='database', verbosity='step')


if __name__ == "__main__":
    run_experiment()
