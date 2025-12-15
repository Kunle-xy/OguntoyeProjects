package edu.iastate.cs572.proj2;

import java.util.ArrayList;
import java.util.Arrays;

/**
 * Node type for the Monte Carlo search tree.
 */
public class MCNode<E> {
    private final CheckersMove move;
    private final MCNode<E> parent;
    private final ArrayList<MCNode<E>> children = new ArrayList<>();
    private final CheckersData state;
    private int visits = 0;
    private double reward = 0.0;
    private final double explorationConstant;

    public MCNode(CheckersMove move, MCNode<E> parent, CheckersData state) {
        this(move, parent, state, Math.sqrt(5)); // Default exploration constant
    }

    public MCNode(CheckersMove move, MCNode<E> parent, CheckersData state, double explorationConstant) {
        this.move = move;
        this.parent = parent;
        this.state = state;
        this.explorationConstant = explorationConstant;
    }

    public void addChild(MCNode<E> child) {
        children.add(child);
    }

    public MCNode<E> getBestChildByVisits() {
        return children.stream()
                .max((c1, c2) -> Integer.compare(c1.visits, c2.visits))
                .orElse(null);
    }

    public MCNode<E> getBestChildByUCT() {
        return children.stream()
                .max((c1, c2) -> Double.compare(c1.getUCTValue(), c2.getUCTValue()))
                .orElse(null);
    }

    public ArrayList<CheckersMove> getUnexploredMoves() {
        CheckersMove[] legalMoves = state.getLegalMoves(state.getCurrentPlayer());

        if (legalMoves == null) {
            return new ArrayList<>();
        }

        ArrayList<CheckersMove> allMoves = new ArrayList<>(Arrays.asList(legalMoves));
        for (MCNode<E> child : children) {
            allMoves.remove(child.getMove());
        }

        return allMoves;
    }
    

    public CheckersData getStateAfterMove(CheckersMove move) {
        CheckersData newState = state.copy();
        newState.makeMove(move);
        return newState;
    }

    public double getUCTValue() {
        if (visits == 0) return Double.MAX_VALUE; // High UCT for unexplored nodes
        if (parent == null) return Double.MAX_VALUE; // Avoid UCT calculation for root

        double exploitation = reward / visits;
        double exploration = explorationConstant * Math.sqrt(Math.log(parent.getVisits()) / visits);
        return exploitation + exploration;
    }

    public double getExplorationConstant() {
        return explorationConstant;
    }
    

    public void updateStats(double result) {
        visits++;
        reward += result;
    }

    public CheckersMove getMove() {
        return move;
    }

    public MCNode<E> getParent() {
        return parent;
    }

    public boolean isLeaf() {
        return children.isEmpty();
    }

    public CheckersData getState() {
        return state;
    }

    public int getVisits() {
        return visits;
    }

    public void incrementVisits() {
        this.visits++;
    }

    public void addReward(double value) {
        this.reward += value;
    }

    public void backpropagation(double result) {
        MCNode<E> currentNode = this;
        while (currentNode != null) {
            currentNode.incrementVisits();
            currentNode.addReward(result);
            currentNode = currentNode.getParent();
        }
    }

    @Override
    public String toString() {
        return "MCNode{" +
                "move=" + move +
                ", visits=" + visits +
                ", reward=" + reward +
                ", UCTValue=" + getUCTValue() +
                '}';
    }
}
