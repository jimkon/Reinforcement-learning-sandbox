package src.core.evaluation;

import org.ejml.simple.SimpleMatrix;

import src.core.MB_MDP;
import src.core.State;
import src.core.policy.Policy;

public final class V_Table extends V{

	private SimpleMatrix v_matrix;
	private MB_MDP mdp = null;
	
	// empty v table
	public V_Table(MB_MDP mdp){
		this.mdp = mdp;
		v_matrix = new SimpleMatrix(mdp.getStates().length, 1);
	}
	
	// solves linear system to init v
	public V_Table(MB_MDP mdp, Policy policy){
		this.mdp = mdp;
		v_matrix = new SimpleMatrix(getStates().length, 1);
		solve(policy);
	}
	
	public double v(State state){
		return v_matrix.get(state.getIndex());
	}
	
	public void updateV(State state, double value){
		v_matrix.set(state.getIndex(), 0, value);
	}
	
	@Override
	public void print() {
		if(v_matrix!=null){
			System.out.println("Value function V");
			v_matrix.print();
		}
		else{
			System.out.println("V value not calculated");
		}
	}

	@Override
	protected State[] getStates() {
		return mdp.getStates();
	}

	@Override
	public V copy() {
		V_Table res = new V_Table(mdp);
		res.mdp = mdp;
		res.v_matrix = v_matrix.copy();
		return res;
	}
	
	// solving the linear equation V = R + gamma*P*V;
	private void solve(Policy policy){
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
		v_matrix = (SimpleMatrix.identity(sl).minus(p.scale(mdp.discountFactor()))).invert().mult(r);
	}
}