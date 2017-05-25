package rl.core;

public class PolicyTable extends Policy{

	private Action[] policy_actions;
	
	public PolicyTable(MDP mdp) {
		super(mdp);
		policy_actions = new Action[mdp.getStates().length];
	}
	
	public void setActionForState(Action action, State state){
		policy_actions[state.getIndex()] = action;
	}
	
	@Override
	public Action pi(State state, Action[] actions) {
		return this.policy_actions[state.getIndex()];
	}
	
	@Override
	public Policy copy() {
		PolicyTable copy = new PolicyTable(mdp);
		for(State state:mdp.getStates()){
			copy.setActionForState(pi(state, mdp.getActions()), state);
		}
		return  copy;
	}
	

}
