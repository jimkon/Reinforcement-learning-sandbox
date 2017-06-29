package src.core.policy;

import src.core.Action;
import src.core.State;
import src.core.misc.DynamicArray;

public class Policy_List extends Policy_Array{
	
	private DynamicArray<Action> list;
	private Action[] actions;
	
	public Policy_List(Action[] a) {
		actions = a;
		list = new DynamicArray<Action>(actions.length);
	}

	@Override
	protected int indexOfState(State state) {
		return list.find_or_add(state);
	}

	@Override
	protected Action get(int i) {
			return list.get(i, 0);
	}

	@Override
	protected void set(int i, Action a) {
		list.set(i, 0, a);
	}

	@Override
	public Policy copy() {
		Policy_List res = new Policy_List(getActions());
		for(State state:getStates()){
			res.setActionForState(pi(state, getActions()), state);
		}
		return res;
	}

	@Override
	public State[] getStates() {
		return list.getStates();
	}
	
	public Action[] getActions(){
		return actions;
	}

}
