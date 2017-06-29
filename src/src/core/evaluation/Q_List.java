package src.core.evaluation;

import src.core.Action;
import src.core.State;
import src.core.misc.DynamicArray;

public class Q_List extends Q_Array{
	
	private DynamicArray<Double> list;
	private Action[] actions = null;
	
	public Q_List(Action[] actions) {
		this.actions = actions;
		 list = new DynamicArray<Double>(actions.length);
	}

	@Override
	protected int indexOfState(State state) {
		return list.find_or_add(state);
	}

	@Override
	protected int indexOfAction(Action action) {
		return action.getID();
	}

	@Override
	protected double get(int i, int j) {
		if(list.get(i, j)==null){
			list.set(i, j, new Double(0));
		}
		return list.get(i, j);
	}

	@Override
	protected void set(int i, int j, double v) {
		list.set(i, j, v);
	}

	@Override
	protected Action[] getActions() {
		return actions;
	}

	@Override
	public ValueFunction copy() {
		Q_List res = new Q_List(getActions());
		for(State state:getStates()){
			for(Action action:getActions()){
				res.updateQ(state, action, q(state, action));
			}
		}
		return res;
	}

	@Override
	protected State[] getStates() {
		return list.getStates();
	}

}
