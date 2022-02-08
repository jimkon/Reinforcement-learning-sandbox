import cProfile

from rl.src.core.engine import run_episodes
from rl.src.core.logging import logger, save_loggers

from experiments.simple_2d.simple_env import SimpleEnv
from experiments.simple_2d.random_walk_agent import RandomWalkAgent
from experiments.simple_2d.my_agent import *


def run_experiment():
    # agent = RandomWalkAgent()
    # agent = MyAgent_Greedy_SE_HC()
    agent = MyAgent_ShortestPath_SE_HC()
    env = SimpleEnv()
    experiment_name = 'simple_experiment_test'
    # logger(experiment_name)
    # run_and_store_episodes(env, agent, 3, experiment_name, store_results_func='database', verbosity='step')
    run_episodes(env, agent, 1, verbosity='step', render=False)
    # logger.save()
    save_loggers()

if __name__ == "__main__":
    import cProfile, pstats, io
    from pstats import SortKey

    pr = cProfile.Profile()
    pr.enable()
    run_experiment()
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    # sortby = SortKey.TIME
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
    # prof = cProfile.Profile()
    # prof.enable()
    # # run_experiment()
    # prof.disable()
    # cProfile.run('run_experiment()',
    #              # filename=r"C:\Users\jim\PycharmProjects\Reinforcement-learning-sandbox\experiments\simple_2d\files\logs\performance_monitoring\cprofile.txt",
    #              )
