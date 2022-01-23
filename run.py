import importlib
import argparse
from time import time
from configparser import ConfigParser

from src.rl.core.configs.run import RUN_CONFIGS_ABSPATH
from src.rl.core.logging import log
from src.rl.core.engine import run_episodes


def main():
    config = ConfigParser()
    config.read(RUN_CONFIGS_ABSPATH)

    parser = argparse.ArgumentParser(description='Execute the experiments defined on the run_configs.ini')
    parser.add_argument('-s', '--source', help='Source of the experiment dir', required=False)
    args = vars(parser.parse_args())

    if args['source'] is not None:
        module_source = args['source']
    else:
        module_source = config['EXPERIMENT']['module']

    experiments_dir = config['DEFAULTS']['experiments_dir']
    experiment_file = config['DEFAULTS']['experiment_file']

    module_name = f"{experiments_dir}.{module_source}.{experiment_file}"

    module = importlib.import_module(module_name)

    iters = int(config['EXPERIMENT']['iterations'])

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

