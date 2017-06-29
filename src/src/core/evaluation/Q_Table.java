package src.core.evaluation;

import org.ejml.simple.SimpleMatrix;

import src.core.Action;
import src.core.MB_MDP;
import src.core.State;
import src.core.policy.Policy;

public class Q_Table extends Q_Array{

	private SimpleMatrix q_matrix;
	private MB_MDP mdp = null;
	
	// empty v table
	public Q_Table(){}
	
	// solves linear system to init q
	public Q_Table(MB_MDP mdp, Policy policy, double e){
		this.mdp = mdp;
		q_matrix = new SimpleMatrix(getStates().length, getActions().length);
		//solve(policy);
		valueIteration(mdp, e, policy);
	}

	@Override
	protected int indexOfState(State state) {
		return state.getID();
	}

	@Override
	protected int indexOfAction(Action action) {
		return action.getID();
	}

	@Override
	protected double get(int i, int j) {
		return q_matrix.get(i, j);
	}

	@Override
	protected void set(int i, int j, double v) {
		q_matrix.set(i, j, v);
	}
//	@Override
//	public double q(State state, Action action){
//		return q_matrix.get(state.getID(), action.getID());
//	}
//	
//	@Override
//	public void updateQ(State state, Action action, double value){
//		q_matrix.set(state.getID(), action.getID(), value);
//	}
	
//	@Override
//	public void print() {
//		if(q_matrix!=null){
//			System.out.println("Value function Q");
//			q_matrix.print();
//		}
//		else{
//			System.out.println("Q value not calculated");
//		}
//	}

	@Override
	protected State[] getStates() {
		return mdp.getStates();
	}
	
	@Override
	protected Action[] getActions() {
		return mdp.getActions();
	}
	
	@Override
	public Q copy() {
		Q_Table res = new Q_Table();
		res.mdp = mdp;
		res.q_matrix = q_matrix.copy();
		return res;
	}
	
	// solving the linear equation V = R + gamma*P*V;
	@SuppressWarnings("unused")
	@Deprecated
	private void solve(Policy policy){}
	
	private int valueIteration(MB_MDP mdp, double e, Policy p){
		SimpleMatrix Q_old;
		int steps = 0;
		do{
			Q_old = q_matrix.copy();
			
			// for each state
			for(State state:mdp.getStates()){
				for(Action action:mdp.getActions()){
					if(state.isTerminal()){
						updateQ(state, action, mdp.reward(state, null));
						//Q.set(state.getIndex(), action.getIndex(), mdp.reward(state, null));
						continue;
					}
					double sum = 0;
					for(State next_state:mdp.getAvailableNextStatesFor(state)){
						double max = Double.NEGATIVE_INFINITY;
						for(Action next_action:mdp.getActions()){
							double q_next = q_matrix.get(next_state.getID(), next_action.getID());
							if(max<q_next){
								max = q_next;
							}
						}
						sum += mdp.transitionModel(next_state, state, action)*max;
					}
					updateQ(state, action, mdp.reward(state, action)+mdp.discountFactor()*sum);
					//Q.set(state.getIndex(), action.getIndex(), mdp.reward(state, action)+mdp.discountFactor()*sum);
				}
				
			}
			
			steps++;
		}while(q_matrix.minus(Q_old).normF()>e);

		for(State state:mdp.getStates()){
			if(state.isTerminal()){
				continue;
			}
			double qmax = Double.NEGATIVE_INFINITY;
			for(Action action:mdp.getActions()){
				if(qmax< q(state, action)){
					qmax = q(state, action);
					p.setActionForState(action, state);
				}
			}
		}
		
		return steps;
	}

	

	
}
