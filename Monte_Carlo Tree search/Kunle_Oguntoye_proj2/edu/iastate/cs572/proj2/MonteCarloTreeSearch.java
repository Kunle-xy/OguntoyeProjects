package edu.iastate.cs572.proj2;

import java.util.ArrayList;
import java.util.Random;

/**
 * 
 * @author 
 *
 */
/**
 * This class implements the Monte Carlo Tree Search method to find the best
 * move at the current state for a checkers game.
 */
public class MonteCarloTreeSearch extends AdversarialSearch {

    private final int SIMULATION_LIMIT = 50; // Limit for MCTS simulations
    private final Random random = new Random();

    @Override
    public CheckersMove makeMove(CheckersMove[] legalMoves) {
        System.out.println("Monte Carlo Tree Search initiated...");

        // Create the root node with the current board state
        MCNode<CheckersMove> root = new MCNode<>(null, null, board);

        // Run simulations up to the specified limit
        for (int i = 0; i < SIMULATION_LIMIT; i++) {
            MCNode<CheckersMove> selectedNode = selection(root);
            MCNode<CheckersMove> expandedNode = expansion(selectedNode);
            double simulationResult = simulation(expandedNode);
            backpropagation(expandedNode, simulationResult);
        }

        // Select the best child node based on visit count (exploration)
        MCNode<CheckersMove> bestChild = root.getBestChildByVisits();
        if (bestChild == null || bestChild.getMove() == null) {
            System.out.println("No valid AI move found.");
            return legalMoves[0]; // Fallback to the first legal move if no move is found
        } else {
            System.out.println("AI selected best move for Black: " + bestChild.getMove());
            return bestChild.getMove();
        }
    }

    /**
     * Selection phase: Traverse the tree by selecting child nodes based on UCT value.
     */
    private MCNode<CheckersMove> selection(MCNode<CheckersMove> node) {
        while (!node.isLeaf()) {
            node = node.getBestChildByUCT();
        }
        System.out.println("Selection step complete.");
        return node;
    }

    /**
     * Expansion phase: Expand the tree by adding one of the unexplored moves as a child node.
     */
    private MCNode<CheckersMove> expansion(MCNode<CheckersMove> node) {
        ArrayList<CheckersMove> unexploredMoves = node.getUnexploredMoves();
        if (!unexploredMoves.isEmpty()) {
            CheckersMove move = unexploredMoves.get(random.nextInt(unexploredMoves.size()));
            CheckersData newState = node.getStateAfterMove(move);
            MCNode<CheckersMove> childNode = new MCNode<>(move, node, newState);
            node.addChild(childNode);
            System.out.println("Expanded with move: " + move);
            return childNode;
        }
        System.out.println("No unexplored moves available for expansion.");
        return node; // If no moves to explore, return the current node
    }

    /**
     * Simulation phase: Perform a random playout from the current state to estimate the reward.
     */
    private double simulation(MCNode<CheckersMove> node) {
        CheckersData simulationState = node.getState().copy();
        int depth = 0;
    
        // Simulate random moves until the game is over or a depth limit is reached
        while (!simulationState.isTerminal() && depth < 20) {
            CheckersMove[] moves = simulationState.getLegalMoves(simulationState.getCurrentPlayer());
            if (moves == null || moves.length == 0) break;
            
            CheckersMove randomMove = moves[random.nextInt(moves.length)];
            simulationState.makeMove(randomMove);
            
            // Switch player after each move
            simulationState.switchPlayer();
            
            depth++;
        }
    
        // Define reward based on the simulation result (difference in pieces)
        int redPieces = simulationState.countPieces(CheckersData.RED);
        int blackPieces = simulationState.countPieces(CheckersData.BLACK);
    
        if (blackPieces > redPieces) {
            return 1.0; // Win for Black (AI)
        } else if (redPieces > blackPieces) {
            return 0.0; // Win for Red (opponent)
        } else {
            return 0.5; // Draw
        }
    }
    

    /**
     * Backpropagation phase: Update the visit count and reward of each node in the path.
     */
    private void backpropagation(MCNode<CheckersMove> node, double reward) {
        while (node != null) {
            node.incrementVisits(); // Increase the visit count for the node
            node.addReward(reward); // Update the reward with the simulation result
            System.out.println("Backpropagation at node: " + node + " Reward: " + reward);
            node = node.getParent();
        }
    }
}
