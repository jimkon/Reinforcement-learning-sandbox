This project contains a core framework for experimentation with different agents on openai-gym environments (or similar). 
The goal is to make it simple and easy to run experiments and collect data. There is the option to store the results on dataframes
or a database for post-experiment analysis. Some general RL architectures will be implemented
also for the proof of concept.

## How it works

A complete example can be found in *experiments/qlearning_pendulum_v0/run_experiment.py*
file, where an implementation of a tabular QLearning agent is tested on the
Pendulum-v0 openai-gym environment for 2000 episodes.

The core function is ***run_experiment( environment, agent, number_of_episodes, args)***.
    
    from rl.core.engine import run_episodes
    
    agent = ...
    environment = gym.make('Pendulum-v0') # expample 
    
    run_episodes(environment,
                 agent,
                 n_episodes=2000,   
                 experiment_name="agent_learning_to_solve_Pendulum", # it helps naming or identifying the reuslts
                 store_results=None,    # None or 'dataframe' or 'database' or a StoreResultsAbstract object 
                 log_frequency=-1,      # store result every log_frequency episodes, -1 to store them all in the end
                 render=False,          # whether to render the execution or not
                 verbosity='progress'   # verbosity: None or 0, 'progress' or 1, 'total' or 2, 'episode' or 3, 'episode_step' or 4

## Storing the results
The results of the execution are _n_episode_ rows of:     
* episode                     
* step                        
* state_0, state_1, ... , state_n  (for n-dimension environment's state space)
* action_0, action_1, ... , action_m (for m-dimension environment's action space)
* reward
* next_state_0,next_state_1, ... , next_state_n, (for n-dimension environment's state space)
* done
* experiment_id

experiment_id is the experiment_name parameter on the *run_episodes* function.
 
There are three options. Store nothing, or store the results in a dataframe or a database.

### Dataframe
The default *'dataframe'* option is to store a dateframe named *<experiment_name>.csv*
in the *files/results/dateframes/* directory. 

If *log_frequency* is greater than -1, then multiple datafrmaes will be stored temporarily in the 
*files/results/dateframes/temp_<experiment_name>/* directory until the execution finishes. Then They will be merged and
stored in the main *<experiment_name>.csv* file.

*if two experiments have the same *experiment_name*, the last experiment will overwrite
the dataframe with the same name.

### Database
The default *'database'* option is to store the results in a table in the default **SQLite** database located in 
*files/results/databeses/rl.db*.

The *n_episode* rows will be stored in a table named after the environments name (somewhat
converted in order to be a valid DB tablename). For example, for 'Pendulum-v0' environment,
the table will be named 'Pendulum_v0'. If the table does not already exist, it will be created.

Also, there will be one entry on the *experiments* table with the infromation about the:
* experiment_id
* agent_id
* env_id
* total_reward
* total_steps
* start_time
* end_time

*if two experiments have the same *experiment_name*, an exception will be raised:   

    raise ValueError(f"{experiment_name} has to be unique in the experiments table")
