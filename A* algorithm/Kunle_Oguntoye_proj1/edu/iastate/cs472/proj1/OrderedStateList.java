package edu.iastate.cs472.proj1;

import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * This class describes a circular doubly-linked list of states to represent both the OPEN and CLOSED lists
 * used by the A* algorithm.  The states on the list are sorted in the
 *
 *     a) order of non-decreasing cost estimate for the state if the list is OPEN, or
 *     b) lexicographic order of the state if the list is CLOSED.
 *
 * @author Kunle Oguntoye
 */
public class OrderedStateList 
{

	/**
	 * Implementation of a circular doubly-linked list with a dummy head node.
	 */
	  private State head;           // dummy node as the head of the sorted linked list 
	  private int size = 0;
	  
	  private boolean isOPEN;       // true if this OrderedStateList object is the list OPEN and false 
	                                // if the list CLOSED.

	  /**
	   *  Default constructor constructs an empty list. Initialize heuristic. Set the fields next and 
	   *  previous of head to the node itself. Initialize instance variables size and heuristic. 
	   * 
	   * @param h 
	   * @param isOpen   
	   */

	  public OrderedStateList(Heuristic h, boolean isOpen) {
		// Create a dummy head node for the circular doubly-linked list
		// Cast null to the specific constructor type (e.g., int[][])
		this.head = new State((int[][]) null);  // Cast null explicitly to int[][] type
		// The dummy node does not hold a board
		this.head.next = this.head;   // Circular: head points to itself
		this.head.previous = this.head; // Circular: head points to itself
		this.size = 0;  // Initially, the list is empty
		this.isOPEN = isOpen;  // Set whether it's an OPEN or CLOSED list
		State.heu = h;  // Set the heuristic to be used
	}

	  
	  public int size()
	  {
		  return size; 
	  }
	  
	  
	  /**
	   * A new state is added to the sorted list.  Traverse the list starting at head.  Stop 
	   * right before the first state t such that compareStates(s, t) <= 0, and add s before t.  
	   * If no such state exists, simply add s to the end of the list. 
	   * 
	   * Precondition: s does not appear on the sorted list. 
	   * 
	   * @param s
	   */
	  public void addState(State s) {
		State current = head.next;
	
		// Traverse to find the correct insertion point
		while (current != head && compareStates(s, current) > 0) {
			current = current.next;
		}
	
		// Insert the new state before the current one
		s.next = current;
		s.previous = current.previous;
		current.previous.next = s;
		current.previous = s;
	
		size++;  // Increment the size of the list
	}
	  
	  
	  /**
	   * Conduct a sequential search on the list for a state that has the same board configuration 
	   * as the argument state s.  
	   * 
	   * Calls equals() from the State class. 
	   * 
	   * @param s
	   * @return the state on the list if found
	   *         null if not found 
	   */
	  public State findState(State s) {
		State current = head.next;
	
		// Iterate through the list to find the state
		while (current != head) {
			if (current.equals(s)) {
				return current;  // Found the state
			}
			current = current.next;
		}
	
		return null;  // Not found
	}
	  
	  
	  /**
	   * Remove the argument state s from the list.  It is used by the A* algorithm in maintaining 
	   * both the OPEN and CLOSED lists. 
	   * 
	   * @param s
	   * @throws IllegalStateException if s is not on the list 
	   */
	  public void removeState(State s) throws IllegalStateException {
		State current = head.next;
	
		// Search for the state to remove
		while (current != head) {
			if (current.equals(s)) {
				// Remove the state by adjusting the pointers
				current.previous.next = current.next;
				current.next.previous = current.previous;
				size--;
				return;
			}
			current = current.next;
		}
	
		throw new IllegalStateException("State not found in the list.");
	}
	  
	  
	  /**
	   * Remove the first state on the list and return it.  This is used by the A* algorithm in maintaining
	   * the OPEN list. 
	   * 
	   * @return  
	   */
	  public State remove() {
		if (size == 0) {
			return null;  // List is empty
		}
	
		State first = head.next;
		head.next = first.next;
		first.next.previous = head;
		size--;
	
		return first;
	}
	  
	  
	  /**
	   * Compare two states depending on whether this OrderedStateList object is the list OPEN 
	   * or the list CLOSE used by the A* algorithm.  More specifically,  
	   * 
	   *     a) call the method compareTo() of the State if isOPEN == true, or 
	   *     b) create a StateComparator object to call its compare() method if isOPEN == false. 
	   * 
	   * @param s1
	   * @param s2
	   * @return -1 if s1 is less than s2 as determined by the corresponding comparison method
	   *         0  if they are equal 
	   *         1  if s1 is greater than s2
	   */
	  private int compareStates(State s1, State s2) {
		if (isOPEN) {
			// Compare based on cost (f = g + h) for OPEN list
			return s1.compareTo(s2);
		} else {
			// Lexicographical comparison for CLOSED list
			StateComparator comparator = new StateComparator();
			return comparator.compare(s1, s2);
		}
	}
}
