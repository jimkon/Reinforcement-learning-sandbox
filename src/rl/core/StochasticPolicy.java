package rl.core;

import java.util.Random;

public abstract class StochasticPolicy extends Policy{
	
	public StochasticPolicy(MDP mdp) {
		super(mdp);
	}

	static final Random RANDOM = new Random();
	
	public Action pi(State state, Action[] actions) {
		double random_value = RANDOM.nextDouble();
		double sum = 0;
		for(int i=0; i<actions.length; i++){
			sum += p(actions[i], state);
			if(random_value<sum){
				return actions[i];
			}
		}
		return null;
	}
	
	public abstract double p(Action action, State state);

}
