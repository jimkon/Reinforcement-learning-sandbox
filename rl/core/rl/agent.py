class AbstractAgent:

    name = None

    def set_env(self, env):
        pass

    def act(self, state):
        raise NotImplementedError

    def observe(self, state, action, reward, next_state, done):
        pass
