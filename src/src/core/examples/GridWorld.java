package src.core.examples;


import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;

import src.core.Action;
import src.core.MB_MDP;
import src.core.State;
import src.core.TD;
import src.core.evaluation.V;
import src.core.evaluation.V_List;
import src.core.policy.PolicyTable;
import toolkit.display.Screen;

public class GridWorld extends MB_MDP{

	public static void main(String[] args) {
		
		GridWorld gw = new GridWorld(); 
		
		class GWPolicy extends PolicyTable{

			public GWPolicy(GridWorld mdp) {
				super(mdp);
			}

			public GWPolicy(GridWorld gw, double e) {
				super(gw, e)	;
			}
		}
		GWPolicy gwp = new GWPolicy(gw);
		gwp.value_iteration(0.01);
		//gwp.print();
		TD td = new TD(gw, gwp, 0.1);
		V_List v = td.computeV(10000);
		gwp.print();
		
		System.out.println("Norm "+gwp.getV().euclidean_norm(v));
		//V_ValueFunction vf = new V_ValueFunction(gw);
		//vf.getPolicyTable().print();
		//Q_ValueFunction qf = new Q_ValueFunction(gw);
		//qf.getPolicyTable().print();
	}
	
	
	
	private final static double STEP_REWARD = -0.04;
	
	public GWState[][] states;
	public GWAction[] actions = new GWAction[]{GWAction.UP, GWAction.DOWN, GWAction.LEFT, GWAction.RIGHT};
	private GWState[] state_array = new GWState[11];
	
	public GridWorld() {
		states = new GWState[4][3];
		int c = 0;
		for(int j=0; j<3; j++){
			for(int i=0; i<4; i++){
				if(i == 1 && j == 1)
					continue;
				states[i][j] = new GWState(i, j); 
				state_array[c++] = states[i][j];
			}
		}
	}

	@Override
	public State[] getStates() {
		// TODO Auto-generated method stub
		return state_array;
	}

	@Override
	public Action[] getActions() {
		// TODO Auto-generated method stub
		return actions;
	}

	/*@Override
	protected State transition(State state, Action action) {
		GWAction[] possibleActions = ((GWAction)action).getAllPossibleActions();
		int l = RANDOM.nextInt(10) - 7;
		l = l>0?l:0;
		//System.out.println("On state "+((GWState) state).x+", "+((GWState) state).y+"  tried action "+possibleActions[0]+"  and applied "+possibleActions[l]);
		return ((GWState)state).applyAction(possibleActions[l]);
		//return ((GWState)state).applyAction((GWAction) action);
	}*/
	
	@Override
	public double transitionModel(State next, State state, Action action) {
		GWState n = (GWState)next, p = (GWState)state;
		GWAction a = (GWAction)action;
		if( a == null ){
			a = (GWAction) getActions()[(int) (Math.random()*4)];
		}
		if(p.isTerminal()){
			return 0;
		}
		if( a == GWAction.NONE ){
			return 0;
		}
		GWAction[] actions = a.getAllPossibleActions();
		GWState[] pos_states = new GWState[]{p.applyAction(actions[0]), p.applyAction(actions[1]), p.applyAction(actions[2])};
		if(n.distance(p)>1)
			return 0;
		double[] pos = new double[]{0.8, 0.1, 0.1};
		double sum = 0;
		for(int i=0; i<pos_states.length; i++){
			if(n.equals(pos_states[i])){
				sum += pos[i];
			}
		}
		return sum;
	}

	@Override
	public double reward(State state, Action action) {
		GWState s = (GWState) state;
		double reward = 0;
		if(s.x == 3 && s.y == 0)
			reward += 1;
		else if(s.x == 3 && s.y == 1)
			reward += -1;
		if(s.x >= 2 && s.y == 1){
			//System.err.println("FAILED");
		}
		//System.out.println("State ("+s.x+" , "+s.y+")  Action "+(action!=null?((GWAction)action):"NONE")+" reward "+reward);
		//System.exit(0);
		if(s.isTerminal() || action == null){
			return reward; 
		}
		return reward+STEP_REWARD;
	}

	@Override
	public double discountFactor() {
		// TODO Auto-generated method stub
		return 1;
	}

	@Override
	public State initialState() {
		// TODO Auto-generated method stub
		return states[0][2];
	}
	
	public void show(V vf){
		double[] v = new double[getStates().length];
		for(State s:getStates()){
			v[s.getID()] = vf.v(s);
		}
		class Show extends Screen{

			public Show() {
				super("Grid Word values", 440, 330);
				setBackground(100, 100, 100);
			}

			@Override
			public void onEachFrame(Graphics g) {
				int padding = 10;
				int width = 100;
				
				for(State state:getStates()){
						GWState s = (GWState)state;
						if(s.x == 1 && s.y == 1)
							continue;
						if(s.isTerminal())
							g.setColor(new Color(200, 200, 0));
						else
							g.setColor(new Color(200, 100, 0));
						g.fillRect(s.x*(width+padding)+padding/2, s.y*(width+padding)+padding/2, width, width);
						g.setColor(new Color(0, 0, 0));
						g.setFont(new Font("Arial", Font.BOLD, 30));
						g.drawString(String.format("%.4f", v[state.getID()]), s.x*(width+padding)+padding/2, s.y*(width+padding)+padding/2+width/2);
					
				}
				
			}
			
		}
		new Show();
	}
	
	
	class GWState extends State{
		
		public int x, y;
		
		public GWState(int x, int y){
			this.x = x;
			this.y = y;
		}

		@Override
		public boolean isTerminal() {
			// TODO Auto-generated method stub
			return x == 3 && y < 2;
		}
		
		public GWState applyAction(GWAction action){
			int temp_x = x + action.x, temp_y = y + action.y;
			if(temp_x<0 || temp_x>3 || temp_y<0 || temp_y>2 || (temp_x==1 && temp_y==1)){
				return this;
			}
			return states[temp_x][temp_y];
		}
		
		public boolean checkAction(GWAction action){
			return !applyAction(action).equals(this);
		}
		
		public double distance(GWState s){
			return Math.sqrt(Math.pow(x-s.x, 2)+Math.pow(y-s.y, 2));
		}
		
		public boolean equals(GWState s){
			return distance(s)==0;
		}
		
		public GWAction actionFor(GWState s){
			return new GWAction(s.x-x, s.y-y);
		}
		
		public String toString(){
			return String.format("(%d, %d)%s", x, y, isTerminal()?"F":"");
		}

		@Override
		public int getID() {
			int index =  x+y*4;
			return index>5?index-1:index;
		}
		
	}
	
	static class GWAction extends Action{
		
		public final static GWAction 	UP = new GWAction(0, -1);

		public final static GWAction DOWN = new GWAction(0, 1);

		public final static GWAction LEFT = new GWAction(-1, 0);

		public final static GWAction RIGHT = new GWAction(1, 0);
		
		public final static GWAction NONE = new GWAction(0, 0);
		
		public final static GWAction RANDOM(){
			int r = (int) (Math.random()*4);
			switch(r){
			case 0:
				return UP;
			case 1:
				return DOWN;
			case 2:
				return LEFT;
			case 3:
				return RIGHT;
			}
			return UP;
		}
		
		
		
		public final int x, y;
		
		public GWAction(int x, int y){
			this.x = x; 
			this.y = y;
		}
		
		public GWAction[] getAllPossibleActions(){
			if(this == UP){
				return new GWAction[]{UP, LEFT, RIGHT};
			}
			if(this == DOWN){
				return new GWAction[]{DOWN, LEFT, RIGHT};
			}
			if(this == LEFT){
				return new GWAction[]{LEFT, UP, DOWN};
			}
			if(this == RIGHT){
				return new GWAction[]{RIGHT, UP, DOWN};
			}
			return  new GWAction[]{this};
		}
		
		public boolean isVertical(GWAction a){
			return (a.x*x+a.y*y)==0;
		}
		
		public int getID(){
			if(this == UP){
				return 0;
			}
			if(this == DOWN){
				return 1;
			}
			if(this == LEFT){
				return 2;
			}
			if(this == RIGHT){
				return 3;
			}
			return -1;
		}
		
		public String toString(){
			String s = String.format("(%d,%d)", x, y);
			if(y>0)
				return "DOWN"+s;
			if(y<0)
				return "UP"+s;
			if(x>0)
				return "RIGHT"+s;
			if(x<0)
				return "LEFT"+s;
			return "NONE"+s;
		}
		
		@Override
		public boolean equals(Action action) {
			// TODO Auto-generated method stub
			return this == action;
		}
		
	}

}
