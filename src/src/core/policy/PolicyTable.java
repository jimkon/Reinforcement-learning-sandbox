package src.core.policy;

import src.core.Action;
import src.core.MB_MDP;
import src.core.State;
import src.core.policy.PolicyTable;

public class PolicyTable extends Policy{

	private Action[] policy_actions;
	private State[] states;
	
	// empty policy table
	public PolicyTable(int n) {
		policy_actions = new Action[n];
		states = new State[n];
	}
	
	
	public PolicyTable(MB_MDP mdp) {
		policy_actions = new Action[mdp.getStates().length];
		states = mdp.getStates();
		policy_iteration(mdp);
	}
	
	public PolicyTable(MB_MDP mdp, double e) {
		policy_actions = new Action[mdp.getStates().length];
		states = mdp.getStates();
		valueIteration(mdp, e);
	}

	public void setActionForState(Action action, State state){
		policy_actions[state.getIndex()] = action;
		states[state.getIndex()] = state;
	}
	
	@Override
	public Action pi(State state, Action[] actions) {
		return policy_actions[state.getIndex()];
	}
	
	@Override
	public Policy copy() {
		PolicyTable copy = new PolicyTable(policy_actions.length);
		for(State state:getStates()){
			copy.setActionForState(pi(state, null), state);
			copy.states[state.getIndex()] = state;
		}
		return  copy;
	}

	@Override
	public State[] getStates() {
		return states;
	}
	

}
