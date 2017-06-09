package src.core;

import src.core.evaluation.V_List;
import src.core.policy.Policy;

public class TD {

	private MDP mdp;
	private Policy policy;
	private double a_init;
	
	public TD(MDP mdp, Policy policy, double a){
		this.mdp = mdp;
		this.policy = policy;
		a_init = a;
	}
	
	public V_List computeV(int number_of_samples){
		V_List vl = new V_List();
		double a = a_init;
		int t = 0;
		while(t<number_of_samples){
			// S = state, A = policy.pi(state, null), R = r, S' = mdp.getCurrentState()
			State state = mdp.getCurrentState();
			double r = mdp.makeAction(policy.pi(state, null));
			
			t++;
			double v = vl.v(state);
			if(state.isTerminal()){
				System.out.print(String.format("%.3f + %.1f ( %.3f - %.3f )", v, a, r, vl.v(state)));
				v +=  a*(r-vl.v(state));
			}
			else{
				System.out.print(String.format("%.3f + %.1f ( %.3f + %.1f*%.3f - %.3f )", v, a, r, mdp.discountFactor(), vl.v(mdp.getCurrentState()), vl.v(state)));
				v += a*(r+mdp.discountFactor()*vl.v(mdp.getCurrentState())-vl.v(state));
			}
			vl.updateV(state, v);
			System.out.println(String.format("= %.4f", v)+"\tWent from "+state+" to "+mdp.getCurrentState()+" with action "+policy.pi(state, null)+" and took reward "+r+"   V"+state+"="+v);
			vl.show(true);
		}
		vl.print();
		return vl;
	}
}
