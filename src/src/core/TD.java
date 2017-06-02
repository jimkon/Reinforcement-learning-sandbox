package src.core;

import src.core.evaluation.V;
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
	
//	public V computeV(int number_of_samples){
//		V v = new V();
//		double a = a_init;
//		int t = 0;
//		while(t<number_of_samples){
//			
//		}
//		
//		return v;
//	}
}
