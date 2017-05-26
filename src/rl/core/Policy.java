package rl.core;

public abstract class Policy {
	
	private final static int MAX_ITERATIONS = 100;
	
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
		int steps = 0;
		Policy p_old = null;
		V_ValueFunction vf = null;
		do{
			p_old = copy();
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
				
				
			}
			steps++;
			if(steps>=MAX_ITERATIONS){
				System.err.println("Policy iteration didnt converge");
				return;
			}
		}while(!p_old.equals(this));
	}
	
	public boolean equals(Policy p){
		for(State state:mdp.getStates()){
			Action a1 = pi(state, mdp.getActions()), a2 = p.pi(state, mdp.getActions());
			if(!((a1 == a2) || (a1!=null && a1.equals(a2)))){
				return false;
			}
		}
		return true;
	}
	
	public abstract Policy copy();
	
	public V_ValueFunction getV(){
		V_ValueFunction vf = new V_ValueFunction(mdp);
		vf.solve(this);
		return vf;
	}
	
}
