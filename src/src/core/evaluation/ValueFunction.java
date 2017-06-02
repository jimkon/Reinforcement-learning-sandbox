package src.core.evaluation;

import src.core.State;

public abstract class ValueFunction {
	
	public abstract void print();
	
	public abstract ValueFunction copy();
	
	protected abstract State[] getStates();// known states

}
