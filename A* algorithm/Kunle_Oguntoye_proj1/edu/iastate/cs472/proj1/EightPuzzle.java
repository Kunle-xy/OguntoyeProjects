package edu.iastate.cs472.proj1;

import java.io.FileNotFoundException;

/**
 * EightPuzzle solver using A* algorithm with multiple heuristics.
 *
 * @author Kunle Oguntoye
 */
public class EightPuzzle 
{
	/**
	 * This static method solves an 8-puzzle with a given initial state using three heuristics. The
	 * first two, allowing single moves only, compare the board configuration with the goal configuration
	 * by the number of mismatched tiles, and by the Manhattan distance, respectively.  The third
	 * heuristic allows double moves and uses an admissible heuristic.  The goal
	 * configuration set for all puzzles is
	 *
	 * 			1 2 3
	 * 			8   4
	 * 			7 6 5
	 *
	 * @param s0 initial state
	 * @return a string containing the solution paths for all three heuristics
	 */
	public static String solve8Puzzle(State s0)
	{
		// If there exists no solution, return a message
		if (!s0.solvable()) {
			return "No solution exists for the following initial state:\n\n" + s0.toString();
		}

		// Solve the puzzle with the three heuristics
		Heuristic h[] = {Heuristic.TileMismatch, Heuristic.ManhattanDist, Heuristic.DoubleMoveHeuristic };
		String [] moves = new String[3];

		for (int i = 0; i < 3; i++)
		{
			moves[i] = AStar(s0, h[i]);
		}

		// Combine the three solution strings into one
		StringBuilder result = new StringBuilder();
		for (int i = 0; i < 3; i++) {
			result.append("Solution ").append(i + 1).append(" using heuristic: ")
				  .append(h[i].toString())  // Append the name of the heuristic
				  .append("\n")
				  .append(moves[i])  // Append the actual solution path
				  .append("\n\n");
		}
	
		return result.toString();
	}

	
	/**
	 * This method implements the A* algorithm to solve the 8-puzzle with an input initial state s0.
	 *
	 * Precondition: the puzzle is solvable with the initial state s0.
	 *
	 * @param s0  initial state
	 * @param h   heuristic to use for the search
	 * @return    solution string showing the path from initial state to goal
	 */
	public static String AStar(State s0, Heuristic h) {

		// Initialize the two lists used by the algorithm. 
		OrderedStateList OPEN = new OrderedStateList(h, true); 
		OrderedStateList CLOSE = new OrderedStateList(h, false);
		
		// Add initial state to OPEN
		OPEN.addState(s0);

		// Main A* search loop
		while (OPEN.size() > 0) {
	
			// Remove the state with the lowest cost (f = g + h) from OPEN
			State current = OPEN.remove();
			// System.out.println("Current State:");
			// System.out.println(current.toString());
	
			// If the current state is the goal, return the solution path
			if (current.isGoalState()) {
				return solutionPath(current);
			}
	
			// Add current state to CLOSED list
			CLOSE.addState(current);
	
			// Generate successors (neighbors) by trying all moves
			for (Move move : Move.values()) {
				// Skip double moves for non-double-move heuristics
				if (h != Heuristic.DoubleMoveHeuristic) {
					if (move == Move.DBL_LEFT || move == Move.DBL_RIGHT || move == Move.DBL_UP || move == Move.DBL_DOWN) {
						continue;  // Skip double moves for non-double-move heuristics
					}
				}
	
				try {
					// Generate a successor state for each move
					State successor = current.successorState(move);
	
					if (successor == null) {
						continue;  // Skip if successor equals predecessor
					}
	
					// Check if the successor is already on the CLOSED list
					State closedState = CLOSE.findState(successor);
					if (closedState != null) {
						// If successor is on CLOSED and its new cost is better, reprocess it
						if (successor.cost() < closedState.cost()) {
							// Remove from CLOSED and put it back on OPEN
							CLOSE.removeState(closedState);
							OPEN.addState(successor);
						}
						continue;  // If it's on CLOSED and not better, skip it
					}
	
					// Check if the successor is already in OPEN
					State openState = OPEN.findState(successor);
					if (openState == null) {
						// If not in OPEN, add it
						OPEN.addState(successor);
					} else if (successor.cost() < openState.cost()) {
						// If it's in OPEN but the new path is better, update the state
						OPEN.removeState(openState);  // Remove the old state
						OPEN.addState(successor);     // Add the new state with the better cost
					}
				} catch (IllegalArgumentException e) {
					continue;  // Ignore invalid moves
				}
			}
		}
	
		return "No solution found."; 
	}
	
	
	
	
	
	/**
	 * From a goal state, follow the predecessor link to trace all the way back to the initial state.
	 * Meanwhile, generate a string to represent board configurations in the reverse order, with
	 * the initial configuration appearing first. Between every two consecutive configurations
	 * is the move that causes their transition. A blank line separates a move and a configuration.
	 * In the string, the sequence is preceded by the total number of moves and a blank line.
	 *
	 * @param goal the goal state from which to trace back
	 * @return string representation of the solution path
	 */
	private static String solutionPath(State goal) {
    
		StringBuilder path = new StringBuilder();
		State current = goal;
		int moveCount = -1;
	
		// Trace the path from the goal state to the initial state
		while (current != null) {
			// Add the current state first
			path.insert(0, current.toString() + "\n\n");
			
			// Then add the move that led to this state (if any)
			if (current.move != null) {
				path.insert(0, "Move: " + current.move.toString() + "\n");
			}
	
			current = current.predecessor;
			moveCount++;
		}
	
		// Prepend the number of moves to the path
		return moveCount + " moves to the solution:\n\n" + path.toString();
	}
	
	
	
}

