package src.core.policy;

import src.core.Action;
import src.core.MB_MDP;
import src.core.State;
import src.core.policy.Policy_Table;

public class Policy_Table extends Policy{

	private Action[] policy_actions;
	private State[] states;
	
	// empty policy table
	public Policy_Table(int n) {
		policy_actions = new Action[n];
		states = new State[n];
	}
	
	
	public Policy_Table(MB_MDP mdp) {
		super(mdp);
		policy_actions = new Action[mdp.getStates().length];
		states = mdp.getStates();
	}
	
	public Policy_Table(MB_MDP mdp, double e) {
		super(mdp);
		policy_actions = new Action[mdp.getStates().length];
		states = mdp.getStates();
	}

	public void setActionForState(Action action, State state){
		policy_actions[state.getID()] = action;
		states[state.getID()] = state;
	}
	
	@Override
	public Action pi(State state, Action[] actions) {
		return policy_actions[state.getID()];
	}
	
	@Override
	public Policy copy() {
		Policy_Table copy = new Policy_Table(policy_actions.length);
		for(State state:getStates()){
			copy.setActionForState(pi(state, null), state);
			copy.states[state.getID()] = state;
		}
		return  copy;
	}

	@Override
	public State[] getStates() {
		return states;
	}
	

}
