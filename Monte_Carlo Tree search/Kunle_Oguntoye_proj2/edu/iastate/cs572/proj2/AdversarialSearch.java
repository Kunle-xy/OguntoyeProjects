package edu.iastate.cs572.proj2;

/**
 * 
 * @author
 *
 */

/**
 * This class is to be extended by the class MonteCarloTreeSearch.
 */
public abstract class AdversarialSearch {
    protected CheckersData board;

    // An instance of this class will be created in the Checkers.Board
    // It would be better to keep the default constructor.

    protected void setCheckersData(CheckersData board) {
        this.board = board;
    }
    
    /** 
     * 
     * @return an array of valid moves
     */
    protected CheckersMove[] legalMoves() {
    	// TODO
    	return board.getLegalMoves(board.getCurrentPlayer()); 
    }
	
    /**
     * Return a move returned from the Monte Carlo tree search.
     * 
     * @param legalMoves
     * @return CheckersMove 
     */
    public abstract CheckersMove makeMove(CheckersMove[] legalMoves);
}
