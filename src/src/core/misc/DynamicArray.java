package src.core.misc;

import java.util.ArrayList;

import src.core.State;


public class DynamicArray<E> {
	
	private ArrayList<Entry<E>> list = new ArrayList<Entry<E>>();
	private State[] states = null;
	private int width;
	
	public DynamicArray(int w){
		width = w;
	}
	
	public E get(int i, int j){		
		return list.get(i).getValue(j);
	}
	
	public void set(int i, int j, E e){
		list.get(i).setValue(e, j);
	}
	
	public int find_or_add(State state){
		int res = search(state, 0, list.size()-1);
		if(res == -1){
			for(res=0; res<list.size(); res++){
				if(state.getID()<list.get(res).getID()){
					break;
				}
			}
			list.add(res , new Entry<E>(state, width));
			states = null;
		}
		return res;
	}
	
	private int search(State state, int s, int e){
		if( list.size() == 0){
			return -1;
		}
		if(s == e){
			if(state.getID() == list.get(s).getID()){
				return s;
			}
			return -1;
		}
		int m = s+(e-s)/2;
		if(state.getID()<=list.get(m).getID()){
			return search(state, s, m);
		}
		else{
			return search(state, m+1, e);
		}
	}
	
	public State[] getStates(){
		if(states == null){
			states = new State[list.size()];
			for(int i=0; i<list.size(); i++){
				states[i] = list.get(i).getState();
			}
		}
		return states;
	}
}
