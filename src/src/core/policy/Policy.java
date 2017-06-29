package src.core.policy;

import src.core.Action;
import src.core.DidNotConvergeException;
import src.core.MB_MDP;
import src.core.State;
import src.core.evaluation.V;
import src.core.evaluation.V_Table;

public abstract class Policy {
	
	private final static int MAX_ITERATIONS = 100;
	
//	public Policy(){}
//	
//	// create optimal policy using policy iteration algorithm
//	public Policy(MB_MDP mdp){
//		policy_iteration(mdp);
//	}
//	
//	// create optimal policy using value iteration algorithm
//	public Policy(MB_MDP mdp, double e){
//		valueIteration(mdp, e);
//	}
	
	private MB_MDP mdp = null;
	
	public Policy(){}
	
	public Policy(MB_MDP mdp){
		this.mdp = mdp;
	}
	
	public abstract Action pi(State state, Action[] actions); // p(s)
	
	public abstract void setActionForState(Action action, State state); // set p(s)
	
	public abstract Policy copy();
	
	public abstract State[] getStates(); // get known states

	public void print(){
		V v = getV();
		System.out.println("Policy "+this);
		if(v == null){
			for(State state:getStates()){
				System.out.println(String.format("State %s\tPolicy action %s", state, pi(state, null)));
			}
		}
		else{
			for(State state:getStates()){
				System.out.println(String.format("State %s\tPolicy action %s  \tV = %f", state, pi(state, null), v.v(state)));
			}
		}
	}
	
	public boolean equals(Policy p){
		for(State state:getStates()){
			Action a1 = pi(state, null), a2 = p.pi(state, null);
			if(!((a1 == a2) || (a1!=null && a1.equals(a2)))){
				return false;
			}
		}
		return true;
	}

	public int policy_iteration(){
		int steps = 0;
		Policy p_old = null;
		V_Table vf = null;
		do{
			p_old = copy();
			vf = getV();
			for(State state:mdp.getStates()){
				if(state.isTerminal()){
					setActionForState(null, state);
					continue;
				}
				
				Action max = null;
				double max_v = 0;
				for(Action action:mdp.getAvailableActionsFor(state)){
					double v = 0;
					for(State next_state:mdp.getAvailableNextStatesFor(state)){
						v += mdp.transitionModel(next_state, state, action)*vf.v(next_state);
					}
					v = mdp.reward(state, action)+mdp.discountFactor()*v;
					if(max == null || max_v < v){
						max = action;
						max_v = v;
					}
				}
				setActionForState(max, state);
			}
			steps++;
			if(steps==MAX_ITERATIONS){
				throw new DidNotConvergeException("Policy iteration did not converge after "+MAX_ITERATIONS+" iterations");
			}
		}while(!equals(p_old));
		return steps;
	}
	
	public V_Table getV(){
		if(mdp == null)
			return null;
		return new V_Table(mdp, this);
	}
	
	// implement Value Iteration algorithm
	public int value_iteration( double e){
		int steps = 0;
		V V_old = null, v = new V_Table(mdp);
		do{
			V_old = (V)v.copy();
			
			// for each state
			for(State state:mdp.getStates()){
				if(state.isTerminal()){
					v.updateV(state, mdp.reward(state, null));
					continue;
				}
				double max = Double.NEGATIVE_INFINITY;
				for(Action action:mdp.getActions()){
					double sum = 0;
					for(State next_state:mdp.getAvailableNextStatesFor(state)){
						sum += mdp.transitionModel(next_state, state, action)*v.v(next_state);
					}
					sum = mdp.reward(state, action)+mdp.discountFactor()*sum;
					if(max<sum){
						setActionForState(action, state);
						max = sum;
					}
				}
				v.updateV(state, max);
			}
			steps++;
		}while(v.euclidean_norm(V_old)>e);

		return steps;
	}
	
}
