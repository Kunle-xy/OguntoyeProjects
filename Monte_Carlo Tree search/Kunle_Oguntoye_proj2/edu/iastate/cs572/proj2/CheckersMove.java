package edu.iastate.cs572.proj2;

import java.util.ArrayList;

/**
 * A CheckersMove object represents a move in the game of Checkers.
 * It holds the row and column of the piece that is to be moved
 * and the row and column of the square to which it is to be moved.
 * (This class makes no guarantee that the move is legal.)
 *
 * It represents an action in the game of Checkers.
 * There may be a single move or multiple jumps in an action.
 * It holds a sequence of the rows and columns of the piece
 * that is to be moved, for example:
 * a single move: (2, 0) -> (3, 1)
 * a sequnce of jumps: (2, 0) -> (4, 2) -> (6, 0)
 *
 */
public class CheckersMove {
    
    ArrayList<Integer> rows = new ArrayList<Integer>();
    ArrayList<Integer> cols = new ArrayList<Integer>();
    
    CheckersMove(int r1, int c1, int r2, int c2) {
        // Constructor, a single move from
        //(r1, c1) to (r2, c2)
        
        // move's start
        rows.add(r1);
        cols.add(c1);
        
        // move's destination
        rows.add(r2);
        cols.add(c2);
    }
    
    CheckersMove() {
        // Constructor, create an empty move
    }
    public CheckersMove(ArrayList<Integer> rows, ArrayList<Integer> cols) {
        this.rows = new ArrayList<>(rows);
        this.cols = new ArrayList<>(cols);
    }
    
    boolean isJump() {
        // Test whether this move is a jump.  It is assumed that
        // the move is legal.  In a jump, the piece moves two
        // rows.  (In a regular move, it only moves one row.)
        return (rows.get(0) - rows.get(1) == 2 || rows.get(0) - rows.get(1) == -2);
    }
    
    
    void addMove(int r, int c){
        // add another move (continuous jump), which goes from
        // (last ele in rows, last ele in cols) to (r, c)
        rows.add(r);
        cols.add(c);
    }
    
    //get a copy of this move
    @Override
    public CheckersMove clone() {
        CheckersMove move = new CheckersMove();
        
        move.rows.addAll(this.rows);
        move.cols.addAll(this.cols);
        
        return move;
        
    }
    
}  // end class CheckersMove.
