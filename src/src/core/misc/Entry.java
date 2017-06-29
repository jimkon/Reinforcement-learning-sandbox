package src.core.misc;

import src.core.State;

public class Entry<E> {

	private State state;
	private Object[] value;
	
	public Entry(State state, int size){
		this.state = state;
		value = new Object[size];
	}
	
	public int getID(){
		return state.getID();
	}
	
	public State getState(){
		return state;
	}
	
	public void setValue(E[] value){
		this.value = value;
	}
	
	public void setValue(E value, int i){
		this.value[i] = value;
	}
	
	@SuppressWarnings("unchecked")
	public E getValue(int i){
		return (E) value[i];
	}
	
}
