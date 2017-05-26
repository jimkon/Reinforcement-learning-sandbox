package rl.core;

import org.ejml.simple.SimpleMatrix;



public class V_ValueFunction extends ValueFunction{
	
	
	
	private SimpleMatrix V;
	
	public V_ValueFunction(MDP mdp){
		super(mdp);
	}
	
	public double V(State state){
		return V.get(state.getIndex());
	}
	
	public void updateV(State state, double value){
		V.set(state.getIndex(), 0, value);
	}
	
	// solving the linear equation V = R + gamma*P*V;
	@Override
	public void solve(Policy policy){
		int sl = mdp.getStates().length;
		SimpleMatrix r = new SimpleMatrix(sl, 1);
		SimpleMatrix p = new SimpleMatrix(sl, sl);
		State[] states = mdp.getStates();
		for(int i=0; i<states.length; i++){
			r.set(i, 0, mdp.reward(states[i], policy.pi(states[i], mdp.getActions())));
			for(int j=0; j<states.length; j++){
				p.set(i, j, mdp.transitionModel(states[j], states[i], policy.pi(states[i], mdp.getActions())));
			}
		}
		V = (SimpleMatrix.identity(sl).minus(p.scale(mdp.discountFactor()))).invert().mult(r);
		//V.print(); 
		
//		//TODO
//		System.out.println("\nlinear system");
//		for(int i=0; i<11; i++){
//			//System.out.print("V("+i+") = "+r.get(i, 0)+" ");
//			System.out.print(String.format("%.3f", V.get(i, 0))+" = "+r.get(i, 0)+" ");
//			for(int j=0; j<11; j++){
//				if(p.get(i, j)!=0){
//					//System.out.print(" + "+p.get(i, j)+" V("+j+")");
//					System.out.print(" + "+p.get(i, j)+" "+String.format("%.3f", V.get(j, 0)));
//				}
//			}
//			System.out.println("");
//		}
//		
//		System.out.println("\n");
//		for(int i=0; i<11; i++){
//			System.out.print("V("+i+") = "+r.get(i, 0)+" ");
//			//System.out.print(String.format("%.3f", V.get(i, 0))+" = "+r.get(i, 0)+" ");
//			for(int j=0; j<11; j++){
//				if(p.get(i, j)!=0){
//					System.out.print(" + "+p.get(i, j)+" V("+j+")");
//					//System.out.print(" + "+p.get(i, j)+" "+String.format("%.3f", V.get(j, 0)));
//				}
//			}
//			System.out.println("");
//		}
	}
	
	// implement Value Iteration argorithm
	@Override
	public int valueIteration(double e, Policy p){
		V = new SimpleMatrix(mdp.getStates().length, 1);
		SimpleMatrix V_old;
		int steps = 0;
		do{
			V_old = V.copy();
			
			// for each state
			for(State state:mdp.getStates()){
				if(state.isFinal()){
					updateV(state, mdp.reward(state, null));
					//V.set(state.getIndex(), 0, mdp.reward(state, null));
					continue;
				}
				double max = Double.NEGATIVE_INFINITY;
				for(Action action:mdp.getActions()){
					double sum = 0;
					for(State next_state:mdp.getAvailableNextStatesFor(state)){
						sum += mdp.transitionModel(next_state, state, action)*V(next_state);
					}
					sum = mdp.reward(state, action)+mdp.discountFactor()*sum;
					if(max<sum){
						p.setActionForState(action, state);
						max = sum;
					}
				}
				updateV(state, max);
				//V.set(state.getIndex(), 0, max);
			}
			steps++;
		}while(V.minus(V_old).normF()>e);

		return steps;
	}
	
	@Override
	public void print() {
		if(V!=null){
			V.print();
		}
		else{
			System.out.println("V value not calculated");
		}
		
	}

}
