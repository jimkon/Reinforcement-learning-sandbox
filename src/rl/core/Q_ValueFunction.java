package rl.core;

import org.ejml.simple.SimpleMatrix;

public class Q_ValueFunction extends ValueFunction{
	
	private SimpleMatrix Q;
	
	public Q_ValueFunction(MDP mdp){
		super(mdp);
		Q = new SimpleMatrix(mdp.getStates().length, mdp.getActions().length);
		//valueIteration(0.0001);
		
	}
	
	public double Q(State state, Action action){
		return Q.get(state.getIndex(), action.getIndex());
	}
	
	public int valueIteration(double e, Policy p){
		SimpleMatrix Q_old;
		int steps = 0;
		do{
			Q_old = Q.copy();
			
			// for each state
			for(State state:mdp.getStates()){
				for(Action action:mdp.getActions()){
					if(state.isFinal()){
						Q.set(state.getIndex(), action.getIndex(), mdp.reward(state, null));
						continue;
					}
					double sum = 0;
					for(State next_state:mdp.getAvailableNextStatesFor(state)){
						double max = Double.NEGATIVE_INFINITY;
						for(Action next_action:mdp.getActions()){
							double q_next = Q.get(next_state.getIndex(), next_action.getIndex());
							if(max<q_next){
								max = q_next;
							}
						}
						sum += mdp.transitionModel(next_state, state, action)*max;
					}
					Q.set(state.getIndex(), action.getIndex(), mdp.reward(state, action)+mdp.discountFactor()*sum);
				}
				
			}
			
			steps++;
		}while(Q.minus(Q_old).normF()>e);

		for(State state:mdp.getStates()){
			if(state.isFinal()){
				continue;
			}
			double qmax = Double.NEGATIVE_INFINITY;
			for(Action action:mdp.getActions()){
				if(qmax< Q(state, action)){
					qmax = Q(state, action);
					p.setActionForState(action, state);
				}
			}
		}
		
		return steps;
	}

	@Override
	public void print() {
		if(Q!=null){
			Q.print();
		}
		else{
			System.out.println("Q value not calculated");
		}
		
	}
	
	

}
