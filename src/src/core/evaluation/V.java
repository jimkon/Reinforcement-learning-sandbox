package src.core.evaluation;

import src.core.State;

public abstract class V extends ValueFunction{
	
	
	public abstract double v(State state); // v(s)
	
	public abstract void updateV(State state, double value); // set v(s)
	
	public void print(){
		System.out.println("Value function V");
		for(State state:getStates()){
			System.out.println(String.format("\tPolicy V(%s) = %f", state, v(state)));
		}
	}
	
	// calculate ||V1-V2|| 
	public double euclidean_norm(V v){
		if(v == null)
			return -1;
		
		double res = 0;
		for(State state:getStates()){
			res += Math.pow(v(state)-v.v(state), 2);
		}
		return Math.sqrt(res);
	}
	
	

}
