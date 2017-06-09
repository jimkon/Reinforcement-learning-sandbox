package src.core.evaluation;


import src.core.State;

public abstract class V_Array extends V{
	
	
	protected abstract int indexOfState(State state);
	
	protected abstract double get(int i);
	
	protected abstract void set(int i, double v);
	
	@Override
	public final double v(State state) {
		return get(indexOfState(state));
	}
	
	@Override
	public final void updateV(State state, double value) {
		set(indexOfState(state), value);
	}
	

}
