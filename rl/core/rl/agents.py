from rl.experiments.simple_2d.my_agent import *

AGENTS = {
    MyAgent_Greedy_SE_POC
}


def get_agent(agent_name):
    for agent in AGENTS:
        if agent.name == agent_name:
            return agent
