# Usage Guide: MCTS Checkers AI

## Quick Start

### Running the Game

1. **Compile the project:**
   ```bash
   cd "Monte_Carlo Tree search/Kunle_Oguntoye_proj2"
   javac edu/iastate/cs572/proj2/*.java
   ```

2. **Launch the GUI:**
   ```bash
   java edu.iastate.cs572.proj2.Checkers
   ```

3. **Play the game:**
   - You play as Red (moves first)
   - AI plays as Black
   - Click a piece to select it
   - Click a destination square to move
   - The AI will automatically respond

## Game Rules

### Basic Movement
- Regular pieces move diagonally forward one square
- Kings (reached the opposite end) can move diagonally in any direction

### Jumping
- You can jump over opponent pieces diagonally
- Captured pieces are removed from the board
- **Forced jumps**: If you can jump, you must jump

### Winning
- Capture all opponent pieces, or
- Block opponent so they have no legal moves

## Understanding the AI

### What the AI is Doing

When it's the AI's turn, it:
1. **Creates a search tree** starting from the current board state
2. **Runs 50 simulations** (each simulation is one complete game)
3. **Selects the most visited move** (the one explored most often)

### AI Thinking Time

- **Fast** (~1 second): The AI is exploring 50 possible game outcomes
- **Slower** when many pieces are on board (more possible moves)
- **Faster** in endgame (fewer pieces = fewer options)

## Customizing the AI

### Making the AI Stronger

Edit `MonteCarloTreeSearch.java` line 14:

```java
// Current: Fast but moderate strength
private final int SIMULATION_LIMIT = 50;

// Strong AI (slower, ~3-5 seconds per move)
private final int SIMULATION_LIMIT = 200;

// Very strong AI (slow, ~10+ seconds per move)
private final int SIMULATION_LIMIT = 500;
```

### Making the AI Faster

```java
// Quick AI (very fast, ~0.5 seconds, weaker play)
private final int SIMULATION_LIMIT = 20;

// Ultra-fast AI (instant, random-like)
private final int SIMULATION_LIMIT = 5;
```

### Adjusting AI Behavior

Edit `MCNode.java` line 73 to change how adventurous the AI is:

```java
// Current: Balanced exploration
double exploration = Math.sqrt(5) * Math.sqrt(Math.log(parent.getVisits()) / visits);

// Conservative AI (exploits known good moves)
double exploration = Math.sqrt(2) * Math.sqrt(Math.log(parent.getVisits()) / visits);

// Aggressive AI (tries many different moves)
double exploration = 3.0 * Math.sqrt(Math.log(parent.getVisits()) / visits);
```

## Playing Strategies

### Against the AI

**Early Game:**
- Control the center
- Keep your back row protected (prevents king promotion)
- Don't rush forward - the AI capitalizes on exposed pieces

**Mid Game:**
- Create forced jump sequences
- Trade pieces when ahead
- Watch for AI sacrifices (it may sacrifice to get a king)

**End Game:**
- Promote to kings as quickly as possible
- Kings are significantly more powerful
- Corner your opponent's last pieces

### What the AI is Good At

✓ **Tactical sequences**: Spots multi-jump opportunities
✓ **Piece counting**: Knows when ahead/behind in material
✓ **Avoiding traps**: Random simulations reveal dangerous positions

### What the AI Struggles With

✗ **Long-term strategy**: Only simulates 20 moves deep
✗ **Positional play**: Doesn't understand "good" vs "bad" positions
✗ **Opening theory**: Doesn't know standard opening moves
✗ **Endgame tablebase**: Doesn't have perfect endgame knowledge

## Example Game Flow

### Turn 1 (Human - Red)
```
Initial Board:
  r   r   r   r
r   r   r   r
  r   r   r   r
.   .   .   .
  .   .   .   .
b   b   b   b
  b   b   b   b
b   b   b   b

Your move: Red piece from (5,0) to (4,1)
```

### Turn 2 (AI - Black)
```
AI Thinking...
- Running 50 MCTS simulations
- Exploring possible responses
- Best move found: (2,1) to (3,0)

AI moves Black piece from (2,1) to (3,0)
```

### Turn 3 (Human - Red)
```
You can jump! (Forced move)
Your move: Jump from (4,1) to (2,3)
AI piece at (3,0) is captured!

Board after jump:
  r   r   .   r
r   r   R   r     <- Your piece became a King!
  .   .   r   r
.   .   .   .
```

## Debugging and Analysis

### Enable Debug Output

To see what the AI is thinking:

Edit `MonteCarloTreeSearch.java` and add print statements:

```java
@Override
public CheckersMove makeMove(CheckersMove[] legalMoves) {
    MCNode<CheckersMove> root = new MCNode<>(null, null, board);

    // Run simulations
    for (int i = 0; i < SIMULATION_LIMIT; i++) {
        MCNode<CheckersMove> selectedNode = selection(root);
        MCNode<CheckersMove> expandedNode = expansion(selectedNode);
        double simulationResult = simulation(expandedNode);
        backpropagation(expandedNode, simulationResult);
    }

    // Print analysis
    System.out.println("=== AI Analysis ===");
    System.out.println("Total simulations: " + root.getVisits());
    for (MCNode<CheckersMove> child : root.getChildren()) {
        System.out.println("Move: " + child.getMove() +
            " | Visits: " + child.getVisits() +
            " | Win Rate: " + (child.getReward() / child.getVisits()));
    }

    MCNode<CheckersMove> bestChild = root.getBestChildByVisits();
    return bestChild.getMove();
}
```

### Visualizing Search Tree

To see the search tree structure:

```java
public void printTree(int depth, int maxDepth) {
    if (depth > maxDepth) return;

    String indent = "  ".repeat(depth);
    System.out.println(indent + "├─ " + this.toString());

    for (MCNode<E> child : children) {
        child.printTree(depth + 1, maxDepth);
    }
}

// In makeMove():
root.printTree(0, 3); // Print first 3 levels
```

## Performance Benchmarking

### Measuring AI Strength

Play multiple games and record:

```java
int aiWins = 0;
int humanWins = 0;
int totalMoves = 0;

// After each game:
if (winner == BLACK) {
    aiWins++;
    System.out.println("AI won in " + moveCount + " moves");
} else {
    humanWins++;
}

// After N games:
System.out.println("AI Win Rate: " + (aiWins / (double)(aiWins + humanWins)));
```

### Comparing Parameter Settings

Test different SIMULATION_LIMIT values:

```java
int[] limits = {20, 50, 100, 200};

for (int limit : limits) {
    long startTime = System.currentTimeMillis();

    // Run AI with this limit
    SIMULATION_LIMIT = limit;
    CheckersMove move = makeMove(legalMoves);

    long duration = System.currentTimeMillis() - startTime;
    System.out.println("Limit: " + limit + " | Time: " + duration + "ms");
}
```

## Advanced Usage

### Integrating MCTS into Other Games

The MCTS implementation can be adapted to other two-player games:

1. **Create a game state class** similar to `CheckersData`
   - Implement `copy()` for state cloning
   - Implement `getLegalMoves()`
   - Implement `makeMove()`
   - Implement `isTerminal()`

2. **Extend AdversarialSearch:**
   ```java
   public class MyGameMCTS extends AdversarialSearch {
       @Override
       public MyMove makeMove(MyMove[] legalMoves) {
           // Same MCTS logic
       }
   }
   ```

3. **Adjust evaluation function** for your game's win conditions

### Parallel MCTS

For faster processing, run simulations in parallel:

```java
ExecutorService executor = Executors.newFixedThreadPool(4);
List<Future<Double>> futures = new ArrayList<>();

for (int i = 0; i < SIMULATION_LIMIT; i++) {
    futures.add(executor.submit(() -> {
        MCNode<CheckersMove> selectedNode = selection(root);
        MCNode<CheckersMove> expandedNode = expansion(selectedNode);
        return simulation(expandedNode);
    }));
}

// Collect results and backpropagate
for (Future<Double> future : futures) {
    double result = future.get();
    backpropagation(expandedNode, result);
}
```

## Troubleshooting

### AI Moves Too Slowly
- Reduce `SIMULATION_LIMIT` (line 14 in MonteCarloTreeSearch.java)
- Reduce simulation depth (line 82 in MonteCarloTreeSearch.java)

### AI Makes Weak Moves
- Increase `SIMULATION_LIMIT`
- Check evaluation function (simulation method)
- Verify UCT calculations are correct

### Game Hangs / Freezes
- Check for infinite loops in simulation
- Ensure `isTerminal()` works correctly
- Add depth limit to simulations (already implemented)

### Compilation Errors
- Ensure all `.java` files are in the correct package structure
- Check Java version (requires Java 8+)
- Verify classpath is set correctly

## Tips for Best Experience

1. **Start with default settings** to understand baseline performance
2. **Experiment with parameters** after playing several games
3. **Compare AI versions** by playing the same position multiple times
4. **Learn from AI moves** - if the AI makes a surprising move, it may have seen something you missed
5. **Record interesting games** for later analysis

## FAQ

**Q: Why does the AI sometimes make bad moves?**
A: With only 50 simulations, the AI has limited search depth. Increasing simulations improves play quality.

**Q: Can the AI play against itself?**
A: Yes! Modify `Checkers.java` to create two AI players with different parameter settings.

**Q: How does MCTS compare to Minimax?**
A: MCTS is more flexible and handles large branching factors better, but Minimax can be stronger with a good evaluation function.

**Q: Why √5 for the exploration constant?**
A: It's a balance between exploration and exploitation suitable for checkers' complexity. Experiment with different values!

**Q: Can I save/load games?**
A: Not currently implemented, but you could add serialization to `CheckersData`.

## Next Steps

- Try different parameter combinations
- Track win rates against the AI
- Modify the evaluation function
- Implement game saving/loading
- Create an AI tournament with different settings
- Visualize the search tree
- Add more sophisticated heuristics

Happy playing! 🎮
