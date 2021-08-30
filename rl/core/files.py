import time


def store_results_to_database(db, data, env, agent=None, experiment_id=None):
    to_table = str(env)
    agent_id = 'unknown_agent_id' if not agent else agent.name()

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
                    VALUES """ + \
                 ',\n'.join(map(str, zip([experiment_id] * len(episodes),
                                         [agent_id] * len(episodes),
                                         episodes,
                                         steps_list,
                                         *states,
                                         *actions,
                                         rewards,
                                         dones)))
    db.execute(insert_str.replace("'", " "))


class StoreResultsAbstract:
    def save(self, data, env, agent, experiment_id=None):
        raise NotImplementedError


class StoreResultsInDataframe(StoreResultsAbstract):
    pass


class StoreResultsInDatabase(StoreResultsAbstract):
    pass

