package src.core.evaluation;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.ArrayList;
import java.util.ConcurrentModificationException;

import src.core.State;
import toolkit.display.Screen;

public class V_List extends V_Array{
	
	private ArrayList<Entry> list = new ArrayList<Entry>();
	private State[] states = null;

	@Override
	protected int indexOfState(State state) {
		int res = search(state, 0, list.size()-1);
		if(res == -1){
			for(res=0; res<list.size(); res++){
				if(state.getID()<list.get(res).state.getID()){
					break;
				}
			}
			list.add(res , new Entry(state, 0));
			states = null;
		}
		return res;
	}

	@Override
	protected double get(int i) {
		return list.get(i).value;
	}

	@Override
	protected void set(int i, double v) {
		list.get(i).value = v;
	}

	@Override
	public ValueFunction copy() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	protected State[] getStates() {
		if(states == null){
			states = new State[list.size()];
			for(int i=0; i<states.length; i++){
				states[i] = list.get(i).state;
			}
		}
		return states;
	}
	
	private int search(State state, int s, int e){
		if( list.size() == 0){
			return -1;
		}
		if(s == e){
			if(state.getID() == list.get(s).state.getID()){
				return s;
			}
			return -1;
		}
		int m = s+(e-s)/2;
		if(state.getID()<=list.get(m).state.getID()){
			return search(state, s, m);
		}
		else{
			return search(state, m+1, e);
		}
	}
	
	private class Entry{
		double value;
		State state;
		
		Entry(State state, double value){
			this.state = state;
			this.value = value;
		}
	}
	
	private VL_Show vl = null;
	public void show(boolean auto){
		if(vl == null){
			vl = new VL_Show();
		}
		vl.refresh(auto);
	}
	
	private class VL_Show extends Screen{

		private volatile boolean flag = true;
		
		public VL_Show() {
			super("V list", 440, 330);
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
				for(Entry e:list){
					printEntry(g, e);
				}
			}catch(ConcurrentModificationException e){
				
			}
			
		}
		
		public void printEntry(Graphics g, Entry e){
			final int size = 100;
			final int id = e.state.getID()>=5?e.state.getID()+1:e.state.getID();
			final int i = (id%4), j = (id/4);
			final int x = size*i+3*i, y = size*j+3*j;
			//System.out.println(x+"   "+y);
			if(e.state.isTerminal())
				g.setColor(Color.BLACK);
			else
				g.setColor(Color.DARK_GRAY);
			g.fillRect(x, y, size, size);
			
			g.setColor(Color.white);
			g.setFont(new Font("Arial", Font.BOLD, 20));
			g.drawString(String.format("%.4f", e.value), x+20, y+size/2);
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
