import agents
import custom_envs


def run_episode(env, agent, render=False):
    
    total_reward = 0
    step = 0
    done = False

    state = env.reset()
    while not done:

        state, reward, done, _ = env.step(agent.act(state))

        total_reward += reward
        step += 1
        if render:
            env.render()

    print("Agent {} completed the episode. Total reward {}, Steps {}".format(agent.name(), total_reward, step))

    return total_reward
