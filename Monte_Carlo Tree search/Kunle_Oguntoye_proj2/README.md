# Monte Carlo Tree Search for Checkers

A Java implementation of Monte Carlo Tree Search (MCTS) to create an intelligent AI player for the game of Checkers.

![Checkers Game](edu/iastate/cs572/proj2/CHECKERS.png)

## Overview

This project implements an AI opponent for checkers using Monte Carlo Tree Search, a powerful decision-making algorithm that combines random sampling with tree search. The AI can play strategically by simulating thousands of random game outcomes to determine the best move.

## What is Monte Carlo Tree Search?

Monte Carlo Tree Search is a heuristic search algorithm used in decision-making processes, particularly effective for game AI. Unlike traditional game trees that require evaluating every possible move, MCTS uses random sampling to explore the most promising moves.

### The Four Phases of MCTS

1. **Selection**: Starting from the root, recursively select the best child nodes using the UCT formula until reaching a leaf node.

2. **Expansion**: If the leaf node is not terminal, expand it by adding one or more child nodes representing possible moves.

3. **Simulation**: From the expanded node, play out a random game (playout/rollout) to completion.

4. **Backpropagation**: Update all nodes along the path from the expanded node back to the root with the simulation result.

## Key Features

- **UCT (Upper Confidence Bound for Trees)**: Balances exploration vs exploitation using the formula:
  ```
  UCT = (wins / visits) + c * sqrt(ln(parent_visits) / visits)
  ```
  where `c = √5` is the exploration constant

- **Configurable Simulation Limit**: Controls the number of MCTS iterations (default: 50)

- **Random Playouts**: Simulates games to completion using random legal moves

- **Win/Loss Evaluation**: Evaluates game states based on piece count difference

- **Interactive GUI**: Java Swing interface for human vs AI gameplay

## Project Structure

```
Kunle_Oguntoye_proj2/
├── edu/iastate/cs572/proj2/
│   ├── MonteCarloTreeSearch.java  # Main MCTS implementation
│   ├── MCNode.java                 # Tree node with UCT calculation
│   ├── MCTree.java                 # Optional tree container
│   ├── AdversarialSearch.java      # Abstract base class
│   ├── Checkers.java               # GUI and game controller
│   ├── CheckersData.java           # Game state representation
│   ├── CheckersMove.java           # Move representation
│   └── CheckersTest.java           # Testing utilities
└── README.md                       # This file
```

## Algorithm Details

### Selection Phase
Traverses the tree from root to leaf using the UCT formula to select child nodes. Nodes with higher UCT values are preferred, balancing:
- **Exploitation**: Selecting moves that have performed well
- **Exploration**: Trying moves that haven't been explored much

### Expansion Phase
When a leaf node is reached, one unexplored move is randomly selected and added as a child node. This incrementally grows the search tree.

### Simulation Phase
From the newly expanded node, the game is played out randomly until:
- A terminal state is reached (one player wins)
- A depth limit is reached (20 moves to prevent infinite loops)

The result is evaluated based on piece count:
- **1.0** = Win for Black (AI)
- **0.0** = Win for Red (opponent)
- **0.5** = Draw

### Backpropagation Phase
The simulation result propagates back up the tree, updating:
- **Visit count**: How many times each node has been visited
- **Reward sum**: Accumulated rewards from all simulations

This information guides future selection decisions.

## How to Run

### Prerequisites
- Java Development Kit (JDK) 8 or higher

### Compilation

```bash
cd "Monte_Carlo Tree search/Kunle_Oguntoye_proj2"
javac edu/iastate/cs572/proj2/*.java
```

### Running the Game

```bash
java edu.iastate.cs572.proj2.Checkers
```

This launches a graphical checkers game where you can play against the MCTS AI.

### Gameplay
- Red (human) always moves first
- Click a piece to select it
- Click a valid square to move
- The AI (Black) will respond automatically using MCTS
- Forced jumps are implemented (you must jump if possible)

## Technical Highlights

### UCT Formula Implementation
The UCT value balances exploration and exploitation:

```java
double exploitation = reward / visits;
double exploration = Math.sqrt(5) * Math.sqrt(Math.log(parent.getVisits()) / visits);
return exploitation + exploration;
```

- Higher exploitation → Focus on moves that have won before
- Higher exploration → Try moves that haven't been tested much
- The `√5` constant determines the balance between them

### Simulation Strategy
Random playouts with depth limiting:
- Prevents infinite game loops
- Focuses on near-term outcomes
- Fast enough for real-time gameplay

### State Management
- **Immutable states**: Each node stores a copy of the board state
- **Legal move generation**: Validates jumps and regular moves
- **Player switching**: Alternates between Red and Black

## Performance Considerations

### Simulation Limit
- **Lower limit (e.g., 50)**: Faster responses, less accurate
- **Higher limit (e.g., 1000)**: Slower responses, more strategic

### Simulation Depth
- **Shorter depth**: Faster simulations, focus on immediate outcomes
- **Longer depth**: More accurate evaluation, computationally expensive

### Trade-offs
The current configuration (50 simulations, 20-move depth) provides:
- ✓ Reasonable move time (~1-2 seconds)
- ✓ Decent strategic play
- ✗ May miss complex long-term strategies

## Potential Improvements

1. **Adaptive Simulation Limit**: Increase simulations in critical game positions
2. **Better Evaluation Function**: Use king count, board position, and mobility instead of just piece count
3. **Parallel MCTS**: Run simulations in parallel for faster tree growth
4. **Progressive Widening**: Limit child nodes to avoid over-expansion
5. **RAVE (Rapid Action Value Estimation)**: Share information between similar moves
6. **Opening Book**: Use pre-computed opening moves for early game

## Algorithm Comparison

| Aspect | Minimax + Alpha-Beta | MCTS |
|--------|---------------------|------|
| **Search Strategy** | Exhaustive, pruned | Sampling-based |
| **Evaluation** | Requires heuristic | Self-evaluating |
| **Branching Factor** | Struggles with high | Handles well |
| **Adaptation** | Fixed depth | Anytime algorithm |
| **Best for** | Chess, tactical games | Go, complex games |

## Applications Beyond Checkers

MCTS has been successfully applied to:
- **Board Games**: Go (AlphaGo), Chess, Shogi
- **Video Games**: Real-time strategy, procedural generation
- **Planning**: Automated scheduling, resource allocation
- **Optimization**: Combinatorial problems

## Author

**Kunle Oguntoye**

## References

- Browne, C., et al. (2012). "A Survey of Monte Carlo Tree Search Methods"
- Silver, D., et al. (2016). "Mastering the game of Go with deep neural networks and tree search"
- Coulom, R. (2006). "Efficient Selectivity and Backup Operators in Monte-Carlo Tree Search"

## License

This project is available for educational and portfolio purposes.
