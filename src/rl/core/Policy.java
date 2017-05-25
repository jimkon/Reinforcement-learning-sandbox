package rl.core;

public abstract class Policy {
	
	protected MDP mdp;
	
	public Policy(MDP mdp){
		this.mdp = mdp;
	}
	
	public abstract Action pi(State state, Action[] actions);

	public void print(){
		System.out.println("Policy "+this+" for MDP "+mdp);
		for(State state:mdp.getStates()){
			System.out.println(String.format("State %s\tPolicy action %s", state, pi(state, null)));
		}
	}
	
	public abstract void setActionForState(Action action, State state);
	
	public void policy_iteration(){
		Policy p_old = copy();
		V_ValueFunction vf = null;
		do{
			vf = getV();
			for(State state:mdp.getStates()){
				if(state.isFinal()){
					setActionForState(null, state);
					continue;
				}
				
				Action max = null;
				double max_v = 0;
				//System.out.print("For action "+state+"     ");//TODO
				for(Action action:mdp.getAvailableActionsFor(state)){
					double v = 0;
					for(State next_state:mdp.getAvailableNextStatesFor(state)){
						v += mdp.transitionModel(next_state, state, action)*vf.V(next_state);
					}
					v = mdp.reward(state, action)+mdp.discountFactor()*v;
					//System.out.print(v+"   for   action "+action);//TODO
					if(max == null || max_v < v){
						max = action;
						max_v = v;
					}
				}
				//System.out.println("   max   action "+max);//TODO	
				setActionForState(max, state);
				//print();
			}
		}while(p_old.equals(this));
		System.out.println("Policy iteration finished");
		vf.print();
	}
	
	public boolean equals(Policy p){
		for(State state:mdp.getStates()){
			if(!pi(state, mdp.getActions()).equals(p.pi(state, mdp.getActions()))){
				return false;
			}
		}
		return true;
	}
	
	public abstract Policy copy();
	
	public V_ValueFunction getV(){
		V_ValueFunction vf = new V_ValueFunction(mdp);
		vf.solveForV(this);
		return vf;
	}
	
}
