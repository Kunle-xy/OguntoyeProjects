package edu.iastate.cs572.proj2;

import java.util.ArrayList;
import java.util.Arrays;

/**
 * An object of this class holds data about a game of checkers.
 * It knows what kind of piece is on each square of the checkerboard.
 * Note that RED moves "up" the board (i.e. row number decreases)
 * while BLACK moves "down" the board (i.e. row number increases).
 * Methods are provided to return lists of available legal moves.
 */
public class CheckersData {

    static final int EMPTY = 0, RED = 1, RED_KING = 2, BLACK = 3, BLACK_KING = 4;

    int[][] board;  // board[r][c] is the contents of row r, column c.
    private int currentPlayer = RED; // RED starts the game by default.

    /**
     * Constructor. Create the board and set it up for a new game.
     */
    CheckersData() {
        board = new int[8][8];
        setUpGame();
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < board.length; i++) {
            int[] row = board[i];
            sb.append(8 - i).append(" ");
            for (int n : row) {
                if (n == 0) {
                    sb.append(" ");
                } else if (n == 1) {
                    sb.append("R");
                } else if (n == 2) {
                    sb.append("RK");
                } else if (n == 3) {
                    sb.append("B");
                } else if (n == 4) {
                    sb.append("BK");
                }
                sb.append(" ");
            }
            sb.append(System.lineSeparator());
        }
        sb.append("  a b c d e f g h");

        return sb.toString();
    }

    /**
     * Set up the board with checkers in position for the beginning of a game.
     */
    public void setUpGame() {
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                if (row < 3 && (row + col) % 2 == 1) {
                    board[row][col] = BLACK; // Place black pieces in top rows
                } else if (row > 4 && (row + col) % 2 == 1) {
                    board[row][col] = RED; // Place red pieces in bottom rows
                } else {
                    board[row][col] = EMPTY; // Ensure other cells are empty
                }
            }
        }
    }
    //DEBUG
    // public static void main(String[] args) {
    //     CheckersData game = new CheckersData();
    //     System.out.println("Initial Board Setup:");
    //     System.out.println(game);
    // }

    public void switchPlayer() {
        if (currentPlayer == RED) {
            currentPlayer = BLACK;
        } else {
            currentPlayer = RED;
        }
    }
    public int countPieces(int player) {
        int count = 0;
        for (int[] row : board) {
            for (int piece : row) {
                if (piece == player || (player == RED && piece == RED_KING) || (player == BLACK && piece == BLACK_KING)) {
                    count++;
                }
            }
        }
        return count;
    }

    /**
     * Return the contents of the square in the specified row and column.
     */
    int pieceAt(int row, int col) {
        return board[row][col];
    }

    /**
     * Make the specified move. It is assumed that move is non-null and that
     * the move it represents is legal.
     */
    public void makeMove(CheckersMove move) {
        if (move.rows.size() == 2) {
            // Single move case
            int fromRow = move.rows.get(0);
            int fromCol = move.cols.get(0);
            int toRow = move.rows.get(1);
            int toCol = move.cols.get(1);
    
            // Make a single move
            makeMove(fromRow, fromCol, toRow, toCol);
        } else {
            // Multi-jump case
            for (int i = 0; i < move.rows.size() - 1; i++) {
                int fromRow = move.rows.get(i);
                int fromCol = move.cols.get(i);
                int toRow = move.rows.get(i + 1);
                int toCol = move.cols.get(i + 1);
    
                // Perform each jump
                System.out.println("Performing jump from (" + fromRow + ", " + fromCol + ") to (" + toRow + ", " + toCol + ")");
                makeMove(fromRow, fromCol, toRow, toCol);
    
                // Print intermediate board state
                System.out.println("Board after jump " + (i + 1) + ":");
                System.out.println(this);
            }
            // Explicitly place the capturing piece at the final position
            // Define the final row and column
            int finalRow = move.rows.get(move.rows.size() - 1);
            int finalCol = move.cols.get(move.cols.size() - 1);

            // Place the capturing piece at the final position
            int finalPiece = board[move.rows.get(0)][move.cols.get(0)];
            board[finalRow][finalCol] = finalPiece;

            // Clear the initial position
            board[move.rows.get(0)][move.cols.get(0)] = EMPTY;

        }
    
        // Print the final board state after the entire move
        System.out.println("Final board state after move:");
        System.out.println(this);
    
        // Switch the player
        switchPlayer();
    }
    
    void makeMove(int fromRow, int fromCol, int toRow, int toCol) {
        // Move the piece to the new location
        board[toRow][toCol] = board[fromRow][fromCol];
        board[fromRow][fromCol] = EMPTY;
    
        // Handle capturing logic for jumps
        if (Math.abs(fromRow - toRow) == 2) {
            int midRow = (fromRow + toRow) / 2;
            int midCol = (fromCol + toCol) / 2;
    
            // Remove the captured piece
            System.out.println("Captured piece at (" + midRow + ", " + midCol + ")");
            board[midRow][midCol] = EMPTY; // Clear the captured square
        }
    
        // Promote to king if the piece reaches the end row
        if (toRow == 0 && board[toRow][toCol] == RED) {
            board[toRow][toCol] = RED_KING;
            System.out.println("Promoting RED piece to KING at (" + toRow + ", " + toCol + ")");
        } else if (toRow == 7 && board[toRow][toCol] == BLACK) {
            board[toRow][toCol] = BLACK_KING;
            System.out.println("Promoting BLACK piece to KING at (" + toRow + ", " + toCol + ")");
        }
    }
    
    /**
     * Return an array containing all the legal CheckersMoves for the specified player.
     */
    public CheckersMove[] getLegalMoves(int player) {
        ArrayList<CheckersMove> capturingMoves = new ArrayList<>();
        ArrayList<CheckersMove> regularMoves = new ArrayList<>();
    
        System.out.println("Generating legal moves for player: " + (player == RED ? "RED" : "BLACK"));
        System.out.println("Current board state:");
        System.out.println(this);
        
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                int piece = board[row][col];
                
                // Check if the piece belongs to the player or is a king of the player's color
                if (piece == player || (piece == RED_KING && player == RED) || (piece == BLACK_KING && player == BLACK)) {
                    
                    // First, check for capturing moves (jumps) from this piece
                    CheckersMove[] jumps = getLegalJumpsFrom(player, row, col);
                    if (jumps != null) {
                        capturingMoves.addAll(Arrays.asList(jumps));
                    }
                    
                    // Only add regular moves if there are no capturing moves
                    if (capturingMoves.isEmpty()) {
                        int[] directions = (piece == RED || piece == BLACK) ? new int[]{(player == RED ? -1 : 1)} : new int[]{-1, 1};
                        for (int dRow : directions) {
                            if (isValidMove(row, col, row + dRow, col + 1)) {
                                regularMoves.add(new CheckersMove(row, col, row + dRow, col + 1));
                            }
                            if (isValidMove(row, col, row + dRow, col - 1)) {
                                regularMoves.add(new CheckersMove(row, col, row + dRow, col - 1));
                            }
                        }
                    }
                }
            }
        }
    
        // Return capturing moves if any, else return regular moves
        if (!capturingMoves.isEmpty()) {
            System.out.println("Returning capturing moves for player: " + (player == RED ? "RED" : "BLACK"));
            return capturingMoves.toArray(new CheckersMove[0]);
        } else if (!regularMoves.isEmpty()) {
            System.out.println("Returning regular moves for player: " + (player == RED ? "RED" : "BLACK"));
            return regularMoves.toArray(new CheckersMove[0]);
        } else {
            System.out.println("No legal moves found for player: " + (player == RED ? "RED" : "BLACK"));
            return null;
        }
    }
    

    private CheckersMove[] getLegalJumpsFrom(int player, int row, int col) {
        ArrayList<CheckersMove> jumps = new ArrayList<>();
        exploreAllJumps(player, row, col, new ArrayList<>(), new ArrayList<>(), jumps);
        return jumps.isEmpty() ? null : jumps.toArray(new CheckersMove[0]);
    }
    
    /**
     * Helper method to recursively explore all possible jump sequences from a given position.
     * 
     * @param player The player making the move (RED or BLACK).
     * @param row The starting row of the piece.
     * @param col The starting column of the piece.
     * @param currentRows A list to track the sequence of rows in the current jump chain.
     * @param currentCols A list to track the sequence of columns in the current jump chain.
     * @param jumps The list to store all possible jump sequences as CheckersMove objects.
     */
    private void exploreAllJumps(int player, int row, int col, ArrayList<Integer> currentRows, ArrayList<Integer> currentCols, ArrayList<CheckersMove> jumps) {
        int[] directions = (board[row][col] == RED_KING || board[row][col] == BLACK_KING) ? new int[]{-2, 2} : new int[]{(player == RED ? -2 : 2)};
        boolean foundJump = false;
    
        for (int d : directions) {
            for (int dCol : new int[]{-2, 2}) {
                int jumpRow = row + d;
                int jumpCol = col + dCol;
                int midRow = (row + jumpRow) / 2;
                int midCol = (col + jumpCol) / 2;
    
                if (isValidJump(player, row, col, jumpRow, jumpCol)) {
                    foundJump = true;
    
                    // Save the current board state
                    int capturedPiece = board[midRow][midCol];
                    int movingPiece = board[row][col];
    
                    // Update the board for this jump
                    board[row][col] = EMPTY;         // The piece leaves its current square
                    board[midRow][midCol] = EMPTY;   // The captured piece is removed
                    board[jumpRow][jumpCol] = movingPiece; // The piece moves to the new square
    
                    // Add the move to the current path
                    ArrayList<Integer> newRows = new ArrayList<>(currentRows);
                    ArrayList<Integer> newCols = new ArrayList<>(currentCols);
                    newRows.add(row);
                    newCols.add(col);
                    newRows.add(jumpRow);
                    newCols.add(jumpCol);
    
                    // Recursively explore further jumps from the new position
                    exploreAllJumps(player, jumpRow, jumpCol, newRows, newCols, jumps);
    
                    // Restore the board state after recursion
                    board[row][col] = movingPiece;         // Restore the piece to its original square
                    board[midRow][midCol] = capturedPiece; // Restore the captured piece
                    board[jumpRow][jumpCol] = EMPTY;       // Clear the jump destination
                }
            }
        }
    
        // If no further jumps were found, add the move sequence
        if (!foundJump && !currentRows.isEmpty()) {
            jumps.add(new CheckersMove(new ArrayList<>(currentRows), new ArrayList<>(currentCols)));
        }
    }
    
    
    
    

    private boolean isValidMove(int fromRow, int fromCol, int toRow, int toCol) {
        return inBounds(toRow, toCol) && board[toRow][toCol] == EMPTY;
    }

    private boolean isValidJump(int player, int fromRow, int fromCol, int toRow, int toCol) {
        if (!inBounds(toRow, toCol) || board[toRow][toCol] != EMPTY) return false;
        
        int midRow = (fromRow + toRow) / 2;
        int midCol = (fromCol + toCol) / 2;
        int opponent = (player == RED) ? BLACK : RED;

        boolean isValid = board[midRow][midCol] == opponent || board[midRow][midCol] == opponent + 1;
        System.out.println("Checking jump from (" + fromRow + "," + fromCol + ") to (" + toRow + "," + toCol + "): " + (isValid ? "Valid" : "Invalid"));
        
        return isValid;
    }

    private boolean inBounds(int row, int col) {
        return row >= 0 && row < 8 && col >= 0 && col < 8;
    }

    public int getCurrentPlayer() {
        return currentPlayer;
    }

    public void setCurrentPlayer(int player) {
        currentPlayer = player;
    }

    public CheckersData copy() {
        CheckersData newState = new CheckersData();
        for (int i = 0; i < board.length; i++) {
            newState.board[i] = board[i].clone();
        }
        return newState;
    }

    public boolean isTerminal() {
        return getLegalMoves(RED) == null && getLegalMoves(BLACK) == null;
    }

    public double getReward() {
        int redPieces = 0, blackPieces = 0;
        for (int[] row : board) {
            for (int piece : row) {
                if (piece == RED || piece == RED_KING) redPieces++;
                else if (piece == BLACK || piece == BLACK_KING) blackPieces++;
            }
        }
        return redPieces - blackPieces;
    }
}