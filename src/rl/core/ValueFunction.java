package rl.core;

public abstract class ValueFunction {
	
	protected MDP mdp;
	
	public ValueFunction(MDP mdp){
		this.mdp = mdp;
	}
	
	public abstract void solve(Policy p);
	
	public abstract int valueIteration(double e, Policy p);
	
	public abstract void print();

}
