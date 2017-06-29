package src.core.evaluation;

import src.core.Action;
import src.core.State;

public abstract class Q_Array extends Q{

	
	protected abstract int indexOfState(State state);
	
	protected abstract int indexOfAction(Action action);
	
	protected abstract double get(int i, int j);
	
	protected abstract void set(int i, int j,  double v);
	
	@Override
	public double q(State state, Action action) {
		return get(indexOfState(state), indexOfAction(action));
	}

	@Override
	public void updateQ(State state, Action action, double value) {
		set(indexOfState(state), indexOfAction(action), value);
	}

}
