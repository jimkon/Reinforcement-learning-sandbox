
def get_agent(agent_name):
    for agent in AbstractAgent.agents:
        if agent.name() == agent_name:
            return agent


class AbstractAgent:

    agents = []

    def set_env(self, env):
        pass

    def act(self, state):
        raise NotImplementedError

    def observe(self, state, action, reward, next_state, done):
        pass

    def name(self):
        return 'default_agent'
