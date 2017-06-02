package src.core;

import java.util.Random;

import src.core.policy.Policy;

public abstract class MDP{
	
	private static final Random RANDOM = new Random();

	protected abstract State[] getStates();
	
	protected abstract Action[] getActions();
	
	protected abstract double transitionModel(State next, State state, Action action);
	
	protected abstract double reward(State state, Action action);
	
	public abstract double discountFactor();
	
	protected abstract State initialState();
	
	public final double sampleEpisode(Policy p){
		double r = 0;
		int step = 0;
		State state = initialState(), nextState;
		while(!state.isFinal()){
			Action action = p.pi(state, getActions());
			nextState  = transition(state, action);
			r += reward(state, action)*discountFactor(step);
			state = nextState;
			step ++;
		}
		r += reward(state, null)*discountFactor(step);
		System.out.println("Reward :"+r+"    after "+step+" steps");
		return r;
	}
	
	private final State transition(State state, Action action){
		State[] next_states = getAvailableNextStatesFor(state);
		double random_value = RANDOM.nextDouble();
		double sum = 0;
		for(int i=0; i<next_states.length; i++){
			sum += transitionModel(next_states[i], state, action);
			if(random_value<sum){
				return next_states[i];
			}
		}
		return null;
	}
	
	protected State[] getAvailableNextStatesFor(State state){
		return getStates();
	}
	
	protected Action[] getAvailableActionsFor(State state){
		return getActions();
	}
	
	protected double discountFactor(int step){
		return Math.pow(discountFactor(), step);
	}
	
}
