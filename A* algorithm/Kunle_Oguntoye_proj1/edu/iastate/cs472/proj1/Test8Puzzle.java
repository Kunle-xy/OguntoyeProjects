package edu.iastate.cs472.proj1;
import java.io.File;
import java.io.FileNotFoundException;

public class Test8Puzzle {

    public static void main(String[] args) {
        try {
            // Step 1: Read the puzzle from the file
            State initialState = new State("8Puzzle.txt");
            System.out.println("Initial Board:");
            printBoard(initialState.board);

            // Step 2: Perform a series of moves and print the result after each move
            State currentState = initialState;

            // Move 1: Perform RIGHT move
            currentState = performMove(currentState, Move.RIGHT);

            // Move 2: Perform DOWN move
            currentState = performMove(currentState, Move.DOWN);

            // Move 3: Perform LEFT move
            currentState = performMove(currentState, Move.LEFT);

            // Move 4: Perform UP move
            currentState = performMove(currentState, Move.UP);

            // Move 5: Perform DBL_LEFT move
            currentState = performMove(currentState, Move.DBL_LEFT);

            // Move 6: Perform DBL_RIGHT move
            currentState = performMove(currentState, Move.DBL_RIGHT);

            // Move 7: Perform DBL_UP move
            currentState = performMove(currentState, Move.DBL_UP);

            // Move 8: Perform DBL_DOWN move
            currentState = performMove(currentState, Move.DBL_DOWN);

            // Add more moves as needed for testing...
            
        } catch (FileNotFoundException e) {
            System.err.println("Error: File not found.");
        } catch (IllegalArgumentException e) {
            System.err.println("Invalid move: " + e.getMessage());
        }
    }

    // Helper function to perform a move and print the board
    private static State performMove(State state, Move move) {
        try {
            State newState = state.successorState(move);
            if (newState != null) {
                System.out.println("After " + move + " move:");
                printBoard(newState.board);
                return newState;
            } else {
                System.out.println("Move " + move + " leads to the predecessor state, no change.");
                return state;
            }
        } catch (IllegalArgumentException e) {
            System.err.println("Invalid move: " + move + " - " + e.getMessage());
            return state;
        }
    }

    // Helper function to print the board
    private static void printBoard(int[][] board) {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
        System.out.println();
    }
}


