# Monte Carlo Tree Search for Checkers

An intelligent AI player for Checkers built using Monte Carlo Tree Search (MCTS), a powerful decision-making algorithm that learns optimal moves through strategic simulation.

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [The Four Components of MCTS](#the-four-components-of-mcts)
3. [Why MCTS Beats Minimax](#why-mcts-beats-minimax)
4. [How to Play](#how-to-play)

---

## Quick Start

**Prerequisites:** Java JDK 8 or higher

```bash
# Navigate to project directory
cd "Monte_Carlo Tree search/Kunle_Oguntoye_proj2"

# Compile
javac edu/iastate/cs572/proj2/*.java

# Run
java edu.iastate.cs572.proj2.Checkers
```

---

## The Four Components of MCTS

Monte Carlo Tree Search builds a decision tree by repeatedly executing four phases. Each iteration improves the AI's understanding of which moves lead to victory.

### 1. **Selection** 🎯

**Purpose:** Navigate from the root to a promising leaf node.

**How it works:**
- Start at the root node (current game state)
- At each level, choose the child node with the highest UCT (Upper Confidence Bound for Trees) value
- Continue until reaching a leaf node

**UCT Formula:**
```
UCT = (wins/visits) + √5 × √(ln(parent_visits)/visits)
```

**Why this matters:** The UCT formula balances two competing strategies:
- **Exploitation** (`wins/visits`): Choose moves that have won before
- **Exploration** (`√5 × √(ln(parent_visits)/visits)`): Try moves we haven't explored much

The constant `√5` determines how adventurous the AI is in trying new moves.

---

### 2. **Expansion** 🌳

**Purpose:** Grow the search tree by adding new possible moves.

**How it works:**
- When we reach a leaf node that hasn't been fully explored
- Generate all legal moves from that position
- Randomly select ONE unexplored move
- Create a new child node for that move

**Why incremental expansion?**
- Keeps the tree manageable in size
- Focuses computational resources on promising branches
- The tree naturally grows toward winning strategies

**Example:**
```
Current position has 5 legal moves → Already explored 3
→ Randomly pick 1 of the 2 remaining moves
→ Add it as a new node
```

---

### 3. **Simulation (Playout)** 🎲

**Purpose:** Evaluate the newly expanded node by playing out the game.

**How it works:**
- From the new node, play the game randomly to completion
- Both players make random legal moves
- Continue until:
  - Someone wins (no pieces left for opponent)
  - Maximum depth reached (20 moves to prevent infinite games)

**Result Scoring:**
- **1.0** = Black (AI) wins
- **0.5** = Draw or depth limit reached
- **0.0** = Red (human) wins

**Why random playouts work:**
- Law of large numbers: After many simulations, good moves win more often
- Fast to compute compared to strategic evaluation
- Surprisingly effective for complex games

---

### 4. **Backpropagation** 📈

**Purpose:** Update all ancestor nodes with the simulation result.

**How it works:**
- Take the result from the simulation (0.0, 0.5, or 1.0)
- Traverse back up the tree from the expanded node to the root
- Update each node along the path:
  - **Increment visit count** by 1
  - **Add the reward** to the node's total score

**Why this matters:**
- Nodes on winning paths accumulate higher scores
- Visit counts help the UCT formula balance exploration/exploitation
- The entire tree becomes smarter with each iteration

**Example:**
```
Simulation result: Black wins (1.0)
Path: Root → Move A → Move B → New Node

Update:
- Root: visits++, reward += 1.0
- Move A: visits++, reward += 1.0  
- Move B: visits++, reward += 1.0
- New Node: visits++, reward += 1.0
```

---

### The Complete MCTS Cycle

```
┌─────────────────────────────────────────────┐
│  Run this cycle 50 times per move          │
└─────────────────────────────────────────────┘

1. SELECTION: Walk down tree using UCT
              ↓
2. EXPANSION: Add one new child node
              ↓
3. SIMULATION: Play random game to end
              ↓
4. BACKPROPAGATION: Update all ancestor nodes
              ↓
   [Repeat 50 times]
              ↓
   Choose move with highest visit count
```

**Configuration:**
- **50 iterations** per AI move (configurable)
- **20-move depth limit** for simulations
- **√5 exploration constant** in UCT formula

---

## Why MCTS Beats Minimax

Monte Carlo Tree Search overcomes the fundamental limitations of traditional Minimax with Alpha-Beta pruning.

### The Minimax Problem

**Minimax approach:**
1. Generate entire game tree to a fixed depth
2. Evaluate leaf positions using a heuristic function
3. Propagate minimax values up the tree
4. Choose the move with the best guaranteed outcome

**Critical weaknesses:**

| Problem | Impact on Checkers |
|---------|-------------------|
| **Exponential growth** | Checkers has ~10^20 positions. Can't search deep enough. |
| **Requires good heuristic** | Hard to design. Bad heuristic = bad play. |
| **Fixed depth** | Must stop at arbitrary depth, may miss crucial tactics. |
| **No learning** | Same heuristic forever, no adaptation. |

---

### How MCTS Solves These Problems

#### 1. **Smart Sampling Instead of Exhaustive Search**

**Minimax:** Tries to evaluate every position to depth D
**MCTS:** Focuses simulations on promising branches

```
Minimax at depth 4:          MCTS after 50 iterations:
    *                             *
   /|\                           /|\
  * * *                         * * *
 /|\ |\ |\                     /|   |
* * * * * *                   * *   *
[Must explore ALL]            [Only explores 
                               promising paths]
```

**Result:** MCTS effectively searches deeper where it matters.

---

#### 2. **Self-Evaluating (No Heuristic Needed)**

**Minimax:** Requires hand-crafted evaluation function
```java
// Complex heuristic needed
eval = pieceCount + 2*kingCount + 
       0.5*mobility + 0.3*position - ...
```

**MCTS:** Uses actual game outcomes
```java
// Simple: Did we win?
result = simulate_random_game();
// 1.0 if we won, 0.0 if we lost
```

**Result:** No expertise needed to design evaluation functions. The algorithm discovers what works.

---

#### 3. **Anytime Algorithm (Flexible Computation)**

**Minimax:** 
- Must complete entire depth-D search
- Can't stop early
- Fixed computation time

**MCTS:**
- Can stop after ANY number of iterations
- More iterations = better move (but returns something useful immediately)
- Adaptive: Use more time in critical positions

```
Available time: 2 seconds
- Run 100 iterations → Good move
- Run 1000 iterations → Better move
- Run 10000 iterations → Best move
```

---

#### 4. **Handles High Branching Factor**

**Checkers branching factor:** 8-12 legal moves per position

**Minimax:** Must evaluate all branches
```
Depth 4: ~10,000 positions
Depth 6: ~1,000,000 positions
Depth 8: ~100,000,000 positions (impractical)
```

**MCTS:** Naturally focuses on best moves
```
After 50 iterations:
- Move A: 25 visits (winning a lot)
- Move B: 15 visits (losing often)
- Move C: 7 visits (mixed results)
- Move D: 3 visits (unpromising)

→ More simulations automatically go to Move A
```

---

### Performance Comparison

| Aspect | Minimax + Alpha-Beta | MCTS | Winner |
|--------|---------------------|------|--------|
| **Search depth** | Limited (depth 6-8) | Adaptive (effectively deeper) | MCTS ✓ |
| **Heuristic needed?** | Yes (expert knowledge) | No (learns from play) | MCTS ✓ |
| **Branching factor** | Struggles with high | Handles naturally | MCTS ✓ |
| **Computation time** | Fixed | Flexible (anytime) | MCTS ✓ |
| **Tactical precision** | Excellent (when deep enough) | Good (statistical) | Minimax ✓ |
| **Strategic play** | Depends on heuristic | Emerges naturally | MCTS ✓ |

**Bottom line:** For complex games like Checkers with large state spaces, MCTS provides stronger play with less domain knowledge.

---

## How to Play

### Game Setup

1. **Launch the game:**
   ```bash
   java edu.iastate.cs572.proj2.Checkers
   ```

2. **A window appears** with an 8×8 checkerboard:
   - **Red pieces** (bottom): You control these
   - **Black pieces** (top): AI controls these

---

### Checkers Rules

#### Piece Movement
- **Regular pieces:** Move diagonally forward one square
- **Kings:** Move diagonally forward OR backward one square (crowned when reaching opposite end)

#### Capturing (Jumping)
- Jump over an opponent's piece to capture it
- Can chain multiple jumps in one turn
- **Mandatory jumps:** If you can jump, you MUST jump

#### Winning
- Capture all opponent pieces, OR
- Trap opponent so they have no legal moves

---

### Playing Against the AI

#### Your Turn (Red)

1. **Click on one of your red pieces**
   - Selected piece is highlighted
   - Valid destination squares are shown

2. **Click on a destination square**
   - If it's a legal move, your piece moves
   - If it's a jump, the opponent's piece is captured
   - If you can chain jumps, you must continue

3. **The AI responds automatically**

#### AI's Turn (Black)

1. **The AI thinks** (1-2 seconds)
   - Running 50 MCTS iterations
   - Building a decision tree
   - Simulating thousands of random games

2. **The AI moves its black piece**
   - Usually makes strategically sound moves
   - Becomes stronger as game progresses

3. **Your turn again**

---

### Strategy Tips

**Against the MCTS AI:**

1. **Control the center** - More mobility means more options
2. **Get kings early** - Double mobility is powerful  
3. **Force trades when ahead** - Simplify when you're winning
4. **Create threats** - Make the AI defend multiple pieces
5. **Avoid traps** - The AI is good at tactical sequences

**What the AI does well:**
- ✓ Avoids obvious blunders
- ✓ Finds multi-jump sequences
- ✓ Trades pieces when ahead
- ✓ Maintains piece advantage

**What the AI struggles with:**
- ✗ Very long-term strategies (beyond 20 moves)
- ✗ Subtle positional play
- ✗ Opening theory (plays randomly until tree builds)

---

### Example Game Flow

```
Turn 1 (Human):
  - Click red piece at (5,2)
  - Click destination (4,3)
  - Piece moves forward

Turn 1 (AI):
  - AI runs MCTS (50 iterations)
  - Evaluates ~50-500 positions
  - Selects best move
  - Black piece moves automatically

Turn 5 (Human):  
  - Jump available! (5,4) → (3,2)
  - MUST take the jump
  - Black piece captured

Turn 5 (AI):
  - AI notices threat to another piece
  - MCTS simulations show defensive move wins more
  - Retreats threatened piece

... game continues until someone wins
```

---

### Understanding AI Behavior

**Why does the AI pause before moving?**
- Running 50 MCTS iterations
- Each iteration: Selection → Expansion → Simulation → Backpropagation
- More iterations = smarter move (configurable in code)

**Why does the AI get better as the game progresses?**
- Fewer pieces = smaller game tree
- MCTS can simulate more complete games
- Endgame is easier to evaluate

**Can I make the AI stronger?**
Yes! Edit `MonteCarloTreeSearch.java`:
```java
// Change this line:
private static final int SIMULATION_LIMIT = 50;

// To something higher:
private static final int SIMULATION_LIMIT = 200;

// Trade-off: Stronger play but slower moves
```

---

## Project Structure

```
Kunle_Oguntoye_proj2/
├── edu/iastate/cs572/proj2/
│   ├── MonteCarloTreeSearch.java   # Main MCTS algorithm (4 phases)
│   ├── MCNode.java                 # Tree node with UCT calculation
│   ├── Checkers.java               # GUI and game controller
│   ├── CheckersData.java           # Board state and move validation
│   ├── CheckersMove.java           # Move representation
│   └── CheckersTest.java           # Testing utilities
├── README.md                       # Original documentation
└── README2.md                      # This file
```

---

## Author

**Kunle Oguntoye**

---

## Key Takeaways

1. **MCTS has four components** that work together in a cycle: Selection, Expansion, Simulation, and Backpropagation

2. **MCTS beats Minimax** by sampling intelligently instead of exhaustive search, requiring no heuristic evaluation function

3. **Playing is simple**: Click your piece, click destination, and watch the AI respond using sophisticated tree search

4. **The magic**: Through random playouts and statistical analysis, MCTS discovers winning strategies without being explicitly programmed with game knowledge

---

*"The best way to predict the future is to simulate it many times and see what happens most often."* – MCTS Philosophy
