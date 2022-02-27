from rl.experiments.simple_2d.simple_env import SimpleEnv

ENVS = {
    SimpleEnv
}


def get_env(env_name):
    for env in ENVS:
        if env.name == env_name:
            return env
