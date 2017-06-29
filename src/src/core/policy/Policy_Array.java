package src.core.policy;

import src.core.Action;
import src.core.State;

public abstract class Policy_Array extends Policy{


	protected abstract int indexOfState(State state);
	
	protected abstract Action get(int i);
	
	protected abstract void set(int i, Action a);
	
	@Override
	public Action pi(State state, Action[] actions) {
		return get(indexOfState(state));
	}

	@Override
	public void setActionForState(Action action, State state) {
		set(indexOfState(state), action);
	}
	

}
