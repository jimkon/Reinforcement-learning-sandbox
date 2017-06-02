package src.core.evaluation;

import src.core.Action;
import src.core.State;

public abstract class Q extends ValueFunction{
	
	public abstract double q(State state, Action action);
	
	public abstract void updateQ(State state, Action action, double value);
	
	protected abstract Action[] getActions();// known states
	
	public void print(){
		System.out.println("Value function Q");
		for(State state:getStates()){
			for(Action action:getActions()){
				System.out.println(String.format("State %s\tPolicy q(s) = %s", state, q(state, action)));
			}
		}
	}
		

}
