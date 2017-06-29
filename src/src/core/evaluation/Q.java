package src.core.evaluation;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.ConcurrentModificationException;

import src.core.Action;
import src.core.State;
import toolkit.display.Screen;

public abstract class Q extends ValueFunction{
	
	public abstract double q(State state, Action action);
	
	public abstract void updateQ(State state, Action action, double value);
	
	protected abstract Action[] getActions();// known states
	
	public void print(){
		System.out.println("Value function Q");
		System.out.print("States");
		for(Action action:getActions()){
			System.out.print("\t|\t"+action);
		}
		System.out.println("\n====\t|\t=========\t|\t=========\t|\t=========\t|\t=========");
		for(State state:getStates()){
			System.out.print(state);
			for(Action action:getActions()){
				System.out.print(String.format("\t|\t%.6f", q(state, action)));
				//System.out.println(String.format("Q(%s,\t %s) = %s", state, action, q(state, action)));
			}
			System.out.println("");
		}
	}
		
	// showing grid world 
		private Q_Show v = null;
		public void show(boolean auto){
			if(v == null){
				v = new Q_Show();
			}
			v.refresh(auto);
		}
		
		@SuppressWarnings("serial")
		private class Q_Show extends Screen{

			private volatile boolean flag = true;
			
			public Q_Show() {
				super("Q", 609, 456);
				setBackground(100, 100, 0);
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
					for(State s:Q.this.getStates()){
						printEntry(g, s);
					}
				}catch(ConcurrentModificationException e){
					
				}
				
			}
			
			public void printEntry(Graphics g, State s){
				final int size = 150;
				final int id = s.getID()>=5?s.getID()+1:s.getID();
				final int i = (id%4), j = (id/4);
				final int x = size*i+3*i, y = size*j+3*j;
				//System.out.println(x+"   "+y);
				if(s.isTerminal())
					g.setColor(Color.BLACK);
				else
					g.setColor(Color.DARK_GRAY);
				g.fillRect(x, y, size, size);
				
				if(!s.isTerminal()){
					g.setColor(new Color(150, 150, 0));
					g.drawLine(x, y, x+size, y+size);
					g.drawLine(x, y+size, x+size, y);
				}
				
				g.setColor(Color.white);
				g.setFont(new Font("Arial", Font.BOLD, 15));
				if(s.isTerminal())
					g.drawString(String.format("%.4f", Q.this.q(s, getActions()[0])), x+size/3, y+size/2);
				else{
					g.drawString(String.format("%.4f", Q.this.q(s, getActions()[0])), x+size/3, y+size/5);
					g.drawString(String.format("%.4f", Q.this.q(s, getActions()[1])), x+size/3, y+4*size/5);
					g.drawString(String.format("%.4f", Q.this.q(s, getActions()[2])), x+1*size/10, y+size/2);
					g.drawString(String.format("%.4f", Q.this.q(s, getActions()[3])), x+6*size/10, y+size/2);
				}
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
