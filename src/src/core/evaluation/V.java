package src.core.evaluation;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.ConcurrentModificationException;

import src.core.State;
import toolkit.display.Screen;

public abstract class V extends ValueFunction{
	
	
	public abstract double v(State state); // v(s)
	
	public abstract void updateV(State state, double value); // set v(s)
	
	public void print(){
		System.out.println("Value function V  size "+getStates().length);
		for(State state:getStates()){
			System.out.println(String.format("  V%s = %f", state, v(state)));
		}
	}
	
	// calculate ||V1-V2|| 
	public double euclidean_norm(V v){
		if(v == null)
			return -1;
		
		double res = 0;
		for(State state:getStates()){
			res += Math.pow(v(state)-v.v(state), 2);
		}
		return Math.sqrt(res);
	}
	
	// showing grid world 
	private VL_Show vl = null;
	public void show(boolean auto){
		if(vl == null){
			vl = new VL_Show();
		}
		vl.refresh(auto);
	}
	
	@SuppressWarnings("serial")
	private class VL_Show extends Screen{

		private volatile boolean flag = true;
		
		public VL_Show() {
			super("V", 440, 330);
			setBackground(100, 100, 100);
			addMouseListener(new MouseAdapter() {
				@Override
				public void mouseClicked(MouseEvent e) {
					// TODO Auto-generated method stub
					super.mouseClicked(e);
					flag = false;
				}
			});
		}

		@Override
		public void onEachFrame(Graphics g) {
			try{
				for(State s:V.this.getStates()){
					printEntry(g, s);
				}
			}catch(ConcurrentModificationException e){
				
			}
			
		}
		
		public void printEntry(Graphics g, State s){
			final int size = 100;
			final int id = s.getID()>=5?s.getID()+1:s.getID();
			final int i = (id%4), j = (id/4);
			final int x = size*i+3*i, y = size*j+3*j;
			//System.out.println(x+"   "+y);
			if(s.isTerminal())
				g.setColor(Color.BLACK);
			else
				g.setColor(Color.DARK_GRAY);
			g.fillRect(x, y, size, size);
			
			g.setColor(Color.white);
			g.setFont(new Font("Arial", Font.BOLD, 20));
			g.drawString(String.format("%.4f", V.this.v(s)), x+20, y+size/2);
		}
		
		public void refresh(boolean auto){
			repaint();
			if(auto){
				try {
					Thread.sleep(10);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
			else{
				while(flag){
					continue;
				};
				flag = true;
			}	
		}
		
	}

}
