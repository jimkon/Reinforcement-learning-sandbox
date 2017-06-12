package src.core.evaluation;

import java.util.ArrayList;
import src.core.State;

public class V_List extends V_Array{
	
	private ArrayList<Entry> list = new ArrayList<Entry>();
	private State[] states = null;

	@Override
	protected int indexOfState(State state) {
		int res = search(state, 0, list.size()-1);
		if(res == -1){
			for(res=0; res<list.size(); res++){
				if(state.getID()<list.get(res).state.getID()){
					break;
				}
			}
			list.add(res , new Entry(state, 0));
			states = null;
		}
		return res;
	}

	@Override
	protected double get(int i) {
		return list.get(i).value;
	}

	@Override
	protected void set(int i, double v) {
		list.get(i).value = v;
	}

	@Override
	public ValueFunction copy() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	protected State[] getStates() {
		if(states == null){
			states = new State[list.size()];
			for(int i=0; i<states.length; i++){
				states[i] = list.get(i).state;
			}
		}
		return states;
	}
	
	private int search(State state, int s, int e){
		if( list.size() == 0){
			return -1;
		}
		if(s == e){
			if(state.getID() == list.get(s).state.getID()){
				return s;
			}
			return -1;
		}
		int m = s+(e-s)/2;
		if(state.getID()<=list.get(m).state.getID()){
			return search(state, s, m);
		}
		else{
			return search(state, m+1, e);
		}
	}
	
	private class Entry{
		double value;
		State state;
		
		Entry(State state, double value){
			this.state = state;
			this.value = value;
		}
	}
	
	
	
	

}
