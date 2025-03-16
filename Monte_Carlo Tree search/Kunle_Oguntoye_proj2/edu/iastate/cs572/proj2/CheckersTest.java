package edu.iastate.cs572.proj2;

import java.util.ArrayList;
import java.util.Arrays;

public class CheckersTest {

    public static void main(String[] args) {
        CheckersData game = new CheckersData();

        // Clear the board for testing
        for (int row = 0; row < 8; row++) {
            Arrays.fill(game.board[row], CheckersData.EMPTY);
        }

        // Set up a multi-jump scenario
        game.board[2][3] = CheckersData.BLACK; // Black piece
        game.board[3][4] = CheckersData.RED;   // Red piece 1 (to be captured)
        game.board[5][4] = CheckersData.RED;   // Red piece 2 (to be captured)

        System.out.println("Initial Board:");
        System.out.println(game);

        // Multi-step jump
        ArrayList<Integer> rows = new ArrayList<>(Arrays.asList(2, 4, 6));
        ArrayList<Integer> cols = new ArrayList<>(Arrays.asList(3, 5, 3));
        CheckersMove multiJumpMove = new CheckersMove(rows, cols);

        // Perform the multi-jump
        game.makeMove(multiJumpMove);

        System.out.println("Final Board:");
        System.out.println(game);
    }
}
