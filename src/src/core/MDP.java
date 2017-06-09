package src.core;

import java.util.Random;

import src.core.policy.Policy;

//model free markov decision process
public abstract class MDP{
	
	private static final Random RANDOM = new Random();
	
	private State current_state = null;

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
		while(!state.isTerminal()){
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
	
	public State getCurrentState(){
		if(current_state == null){
			current_state = initialState();
		}
		return current_state;
	}
	
	public double makeAction(Action action){
		State temp = current_state;
		current_state = transition(current_state, action);
		return reward(temp, action);//+((current_state!=null)?reward(current_state, null):0);
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
