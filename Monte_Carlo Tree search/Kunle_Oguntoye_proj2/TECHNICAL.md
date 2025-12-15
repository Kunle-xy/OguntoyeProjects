# Technical Documentation: UCT Formula and Parameters

## Upper Confidence Bound for Trees (UCT)

### The Formula

The UCT formula used in node selection is:

```
UCT(node) = Q(node)/N(node) + c * sqrt(ln(N(parent)) / N(node))
```

Where:
- **Q(node)**: Total reward accumulated by this node
- **N(node)**: Number of times this node has been visited
- **N(parent)**: Number of times the parent node has been visited
- **c**: Exploration constant (we use √5 ≈ 2.236)

### Breaking Down the Formula

#### Exploitation Component: Q(node) / N(node)
```java
double exploitation = reward / visits;
```

This is the **average reward** or win rate of the node:
- Higher values = This move has historically performed well
- Encourages selecting moves that have won before
- Purely greedy if used alone

**Example:**
- Node A: 8 wins / 10 visits = 0.80
- Node B: 5 wins / 10 visits = 0.50
- Exploitation favors Node A

#### Exploration Component: c * sqrt(ln(N_parent) / N_node)
```java
double exploration = Math.sqrt(5) * Math.sqrt(Math.log(parent.getVisits()) / visits);
```

This encourages trying **less-visited nodes**:
- Higher values for rarely visited nodes
- Ensures all moves get tried eventually
- Prevents getting stuck in local optima

**Example:**
- Node A: Visited 100 times → Low exploration value
- Node B: Visited 10 times → High exploration value
- Exploration favors Node B

### Why This Works

The UCT formula creates a **multi-armed bandit** strategy:
1. Initially, all nodes have low visit counts → **explore everything**
2. As simulations run, good moves get more visits → **exploit winners**
3. The logarithm ensures exploration never stops completely
4. The balance shifts from exploration to exploitation over time

## Parameter Tuning

### Exploration Constant (c)

**Current Value:** `c = √5 ≈ 2.236`

This constant controls the exploration-exploitation trade-off:

| Value | Behavior | Use Case |
|-------|----------|----------|
| c = 0 | Pure exploitation | When evaluation is perfect |
| c = 1/√2 | Theoretical optimum | Standard recommendation |
| c = √2 | Balanced | General games |
| c = √5 | More exploration | Complex, uncertain games |
| c > 3 | Heavy exploration | Unknown game spaces |

**Why √5 for Checkers?**
- Checkers has moderate complexity (not as simple as Tic-Tac-Toe, not as complex as Go)
- Encourages trying different strategic paths
- Prevents premature convergence on suboptimal moves

#### Adjusting the Exploration Constant

```java
// In MCNode.java, line 73
double exploration = Math.sqrt(5) * Math.sqrt(Math.log(parent.getVisits()) / visits);

// To change exploration behavior:
// More exploration (c = 3):
double exploration = 3.0 * Math.sqrt(Math.log(parent.getVisits()) / visits);

// Less exploration (c = 1):
double exploration = Math.sqrt(Math.log(parent.getVisits()) / visits);
```

### Simulation Limit

**Current Value:** `SIMULATION_LIMIT = 50`

This controls how many MCTS iterations run before selecting a move.

| Limit | Response Time | Move Quality | Recommended For |
|-------|--------------|--------------|-----------------|
| 10 | Very fast (~0.1s) | Poor | Testing only |
| 50 | Fast (~1s) | Decent | Casual play |
| 100 | Medium (~2s) | Good | Competitive play |
| 500 | Slow (~10s) | Very good | Strong AI |
| 1000+ | Very slow | Near-optimal | Tournaments |

**Trade-off:**
- **More simulations** = Better moves, but slower response
- **Fewer simulations** = Faster play, but weaker strategy

#### Adjusting Simulation Limit

```java
// In MonteCarloTreeSearch.java, line 14
private final int SIMULATION_LIMIT = 50;

// For stronger AI:
private final int SIMULATION_LIMIT = 200;

// For faster responses:
private final int SIMULATION_LIMIT = 20;
```

### Simulation Depth

**Current Value:** `depth < 20` (in simulation phase)

This limits how far random playouts go.

| Depth | Simulation Speed | Evaluation Accuracy |
|-------|-----------------|---------------------|
| 5 | Very fast | Poor (too shallow) |
| 10 | Fast | Fair |
| 20 | Medium | Good |
| 50 | Slow | Better |
| ∞ | Varies | Best (game end) |

**Why 20 moves?**
- Average checkers game is 40-80 moves
- 20 moves = ~25-50% of game
- Prevents infinite loops in draws
- Fast enough for real-time play

#### Adjusting Simulation Depth

```java
// In MonteCarloTreeSearch.java, line 82
while (!simulationState.isTerminal() && depth < 20) {
    // ... simulation code
}

// For deeper simulations:
while (!simulationState.isTerminal() && depth < 50) {

// For faster simulations:
while (!simulationState.isTerminal() && depth < 10) {
```

## Advanced Tuning Strategies

### Adaptive Parameters

Instead of fixed values, adjust based on game state:

```java
// More simulations in endgame
int simulations = (piecesOnBoard < 6) ? 200 : 50;

// Higher exploration in opening
double c = (movesPlayed < 10) ? Math.sqrt(5) : Math.sqrt(2);
```

### Progressive Widening

Limit child expansion to prevent over-branching:

```java
// Only expand if visits exceed threshold
int maxChildren = (int) Math.pow(node.getVisits(), 0.5);
if (node.childrenCount() < maxChildren) {
    // expand new child
}
```

### RAVE (Rapid Action Value Estimation)

Share statistics across similar moves:

```java
// Consider all moves of the same piece type
double uctValue = exploitation + exploration + raveBonus;
```

## Computational Complexity

### Time Complexity
- **Per simulation**: O(d * b) where:
  - d = simulation depth (20)
  - b = average branching factor (~8 in checkers)
- **Total**: O(s * d * b) where s = simulation limit (50)
- **Overall**: ~8,000 operations per move

### Space Complexity
- **Tree nodes**: O(s) = 50 nodes stored
- **Each node**: ~100 bytes
- **Total memory**: ~5 KB (very efficient)

## Evaluation Function

Current evaluation uses **piece count difference**:

```java
int redPieces = simulationState.countPieces(CheckersData.RED);
int blackPieces = simulationState.countPieces(CheckersData.BLACK);

if (blackPieces > redPieces) return 1.0;  // AI wins
else if (redPieces > blackPieces) return 0.0;  // Opponent wins
else return 0.5;  // Draw
```

### Improving Evaluation

A better evaluation function could include:

```java
double score = 0.0;

// Piece count (kings worth more)
score += 1.0 * normalPieces;
score += 1.5 * kingPieces;

// Board position (center control)
score += 0.1 * centerPieces;

// Mobility (number of legal moves)
score += 0.05 * legalMoveCount;

// Back row safety
score += 0.2 * backRowPieces;

return score;
```

## Debugging and Analysis

### Tracking UCT Values

To see which moves are favored:

```java
System.out.println("Move: " + move +
    " | Visits: " + visits +
    " | Reward: " + reward +
    " | UCT: " + getUCTValue());
```

### Visualizing the Tree

To understand search behavior:

```java
public void printTree(int depth) {
    String indent = "  ".repeat(depth);
    System.out.println(indent + this.toString());
    for (MCNode<E> child : children) {
        child.printTree(depth + 1);
    }
}
```

## Benchmarking

To compare parameter settings:

```java
long startTime = System.currentTimeMillis();
CheckersMove move = makeMove(legalMoves);
long endTime = System.currentTimeMillis();

System.out.println("Time: " + (endTime - startTime) + "ms");
System.out.println("Root visits: " + root.getVisits());
System.out.println("Best move visits: " + bestChild.getVisits());
```

## References

1. **Original UCT Paper**: Kocsis & Szepesvári (2006), "Bandit based Monte-Carlo Planning"
2. **MCTS Survey**: Browne et al. (2012), "A Survey of Monte Carlo Tree Search Methods"
3. **Exploration Constants**: Gelly & Silver (2007), "Combining Online and Offline Knowledge in UCT"

## Summary

| Parameter | Current Value | Purpose | Tuning Direction |
|-----------|--------------|---------|------------------|
| Exploration constant (c) | √5 ≈ 2.236 | Balance explore/exploit | Higher = more exploration |
| Simulation limit | 50 | AI strength vs speed | Higher = stronger, slower |
| Simulation depth | 20 moves | Playout accuracy | Higher = more accurate |

**Key Insight:** MCTS is an **anytime algorithm** - it improves the longer you let it run. The parameters control the trade-off between **time** and **quality**.
