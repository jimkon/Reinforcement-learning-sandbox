import importlib
import argparse
from time import time
from configparser import ConfigParser

from src.rl.core.configs.run import RUN_CONFIGS_ABSPATH
from src.rl.core.configs.experiment import STORE_DATABASE_OBJECT_ABSPATH
from src.rl.core.logging import log
from src.rl.core.engine import run_episodes


def read_run_configs():
    configs = ConfigParser()
    configs.read(RUN_CONFIGS_ABSPATH)
    return configs


def read_args():
    parser = argparse.ArgumentParser(description='Execute the experiments defined on the run_configs.ini')
    parser.add_argument('-s', '--source', help='Source of the experiment dir', required=False)
    args = vars(parser.parse_args())
    return args


def process_args(args, configs):
    if args['source'] is not None:
        args['module_source'] = args['source']
    else:
        args['module_source'] = configs['EXPERIMENT']['module']

    args['iters'] = int(configs['EXPERIMENT']['iterations'])

    args['experiments_dir'] = configs['DEFAULTS']['experiments_dir']
    args['experiment_file'] = configs['DEFAULTS']['experiment_file']

    args['module_name'] = f"{args['experiments_dir']}.{args['module_source']}.{args['experiment_file']}"


    return args


def main():
    configs = read_run_configs()

    args = process_args(read_args(), configs)

    module = importlib.import_module(args['module_name'])
    iters = args['iters']

    start_time = time()
    log(f"Execution starts. Iterations {iters}")
    for i in range(iters):
        experiment_kwargs = module.experiment_args()
        experiment_kwargs['render'] = False

        log(f"Experiment {i} starts. Args: {experiment_kwargs}")
        exp_start_time = time()
        run_episodes(**experiment_kwargs)
        exp_end_time = time() - exp_start_time
        log(f"Experiment {i} ended in {exp_end_time} seconds.")

    end_time = time() - start_time
    log(f"Execution ended in {end_time} seconds. Iterations {i + 1}/{iters}")


if __name__ == "__main__":
    main()

