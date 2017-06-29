package src.core.evaluation;

import src.core.State;
import src.core.misc.DynamicArray;

public class V_List extends V_Array{
	
	private DynamicArray<Double> list = new DynamicArray<Double>(1);

	@Override
	protected int indexOfState(State state) {
		return list.find_or_add(state);
	}

	@Override
	protected double get(int i) {
		if(list.get(i, 0)==null){
			list.set(i, 0, new Double(0));
		}
		return list.get(i, 0);
	}

	@Override
	protected void set(int i, double v) {
		list.set(i, 0, new Double(v));
	}

	@Override
	public ValueFunction copy() {
		V_List res = new V_List();
		for(State state:getStates()){
			res.updateV(state, v(state));
		}
		return res;
	}

	@Override
	protected State[] getStates() {
		return list.getStates();
	}
	

}
