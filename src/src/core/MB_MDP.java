package src.core;

// model based markov decision process
public abstract class MB_MDP extends MDP{
	
	public abstract State[] getStates();
	
	public abstract Action[] getActions();
	
	public abstract double transitionModel(State next, State state, Action action);
	
	public abstract double reward(State state, Action action);
	
	public abstract State initialState();
	
	public State[] getAvailableNextStatesFor(State state){
		return super.getAvailableNextStatesFor(state);
	}
	
	public Action[] getAvailableActionsFor(State state){
		return super.getAvailableActionsFor(state);
	}


}
