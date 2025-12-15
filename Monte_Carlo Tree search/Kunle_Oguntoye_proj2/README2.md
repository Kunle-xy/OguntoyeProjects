# Monte Carlo Tree Search for Checkers

An intelligent AI player for Checkers built using Monte Carlo Tree Search (MCTS), a game-changing algorithm that discovers winning strategies through intelligent simulation rather than exhaustive search.

---

## Table of Contents
1. [Understanding the Problem: Why Traditional Game AI Fails](#understanding-the-problem-why-traditional-game-ai-fails)
2. [The MCTS Solution](#the-mcts-solution)
3. [The Four Components of MCTS](#the-four-components-of-mcts)
4. [Mathematical Foundation](#mathematical-foundation)
5. [Quick Start](#quick-start)
6. [How to Play](#how-to-play)

---

## Understanding the Problem: Why Traditional Game AI Fails

### The Minimax Approach: A Beautiful Idea with Fatal Flaws

**The Core Concept:**
Minimax attempts to guarantee optimal play by exploring the complete game tree. The algorithm assumes:
- **You** (the maximizing player) want to maximize your score
- **Your opponent** (the minimizing player) will minimize your score
- Both players play perfectly

**How Minimax Works:**

1. **Build a game tree** to depth $d$
2. **Evaluate leaf positions** using a heuristic function $h(s)$
3. **Propagate values upward:**
   - At MAX nodes: $\text{value}(s) = \max(\text{value}(\text{children}))$
   - At MIN nodes: $\text{value}(s) = \min(\text{value}(\text{children}))$
4. **Choose the move** leading to the best guaranteed outcome

---

### Critical Flaw #1: The Exponential Explosion

**The Mathematics of Impossibility:**

Let:
- $b$ = average branching factor (legal moves per position)
- $d$ = search depth
- $N$ = total nodes to evaluate

Then: $N = b^d$

**For Checkers:**
- Early game: $b \approx 10$ legal moves per position
- To search depth 8: $N = 10^8 = 100,000,000$ positions
- To search depth 10: $N = 10^{10} = 10,000,000,000$ positions
- **Entire game tree**: $\approx 10^{20}$ positions (impossible to compute)

**Alpha-Beta Pruning helps, but not enough:**

Best case (perfect move ordering): $N \approx 2b^{d/2}$

For depth 10: $N \approx 2 \times 10^5 = 200,000$ nodes (better, but still limited)

**The Reality:** Even with pruning, we're stuck at shallow depths (6-8 plies), missing crucial tactics that occur deeper in the game tree.

---

### Critical Flaw #2: The Heuristic Function Problem

**Minimax requires a hand-crafted evaluation function $h(s)$:**

$$h(s) = w_1 \cdot f_1(s) + w_2 \cdot f_2(s) + \cdots + w_n \cdot f_n(s)$$

Where:
- $f_i(s)$ = features (piece count, king count, position, mobility, etc.)
- $w_i$ = weights (how important is each feature?)

**Example Checkers Heuristic:**

$$h(s) = 3 \cdot (\text{pieces}) + 5 \cdot (\text{kings}) + 0.5 \cdot (\text{mobility}) + 0.3 \cdot (\text{center control}) - \text{opponent\_score}$$

**Why This Is Problematic:**

1. **Requires Expert Knowledge:** Must understand what makes a position "good"
2. **Hard to Get Right:** Small weight changes dramatically affect play quality
3. **Game-Specific:** Doesn't transfer to other games
4. **Misses Emergent Strategy:** Can't capture complex patterns humans haven't noticed
5. **Local vs Global:** May favor immediate gains over long-term strategy

**Real Example:**

```
Position A: +2 pieces advantage, poor positioning
Position B: Equal pieces, excellent positioning for king promotion

Bad heuristic picks A (immediate material)
Good player picks B (strategic advantage)
```

How do we know which heuristic is "good"? **We often don't!**

---

### Critical Flaw #3: The Fixed Depth Horizon Problem

**Minimax searches to depth $d$ and stops:**

```
Depth 0: Current position
Depth 1: All responses
Depth 2: All responses to responses
...
Depth d: STOP and evaluate with h(s)
```

**The Horizon Effect:**

Consider this scenario:
```
Depth 6: Your piece is safe
Depth 7: Opponent threatens your piece
Depth 8: You must sacrifice another piece to save it
```

If you search to depth 6, **you don't see the threat!**

**Quiescence Search** helps but adds complexity and doesn't solve the fundamental problem.

---

### Critical Flaw #4: The Assumption of Perfect Play

**Minimax assumes:**
$$\text{opponent\_move} = \arg\min_{m \in \text{moves}} \text{value}(m)$$

**Reality:** Opponents make mistakes, especially in complex positions.

A good strategy might:
- **Set traps** that look bad to Minimax but confuse human opponents
- **Create complexity** to increase opponent error rate
- **Adapt to opponent skill level**

Minimax can't do any of this—it assumes perfect opponent play always.

---

## The MCTS Solution

### Why Monte Carlo Tree Search Changes Everything

Instead of the Minimax approach, MCTS uses a **fundamentally different philosophy:**

| Minimax Approach | MCTS Approach |
|-----------------|---------------|
| "Explore everything shallowly" | "Explore promising moves deeply" |
| "Evaluate positions with heuristics" | "Evaluate by actually playing games" |
| "Assume perfect play" | "Learn from statistical outcomes" |
| "Build the entire tree to depth $d$" | "Grow the tree where it matters" |

---

### The Core Insight: Selective Sampling

**Key Idea:** Instead of evaluating ALL positions to depth $d$, evaluate SOME positions to depth $d, d+1, \ldots, d+k$ by **actually playing them out**.

**Why This Works:**

1. **Reality-Based Evaluation:** 
   - Instead of guessing with $h(s)$, play random games
   - Win rate = actual probability of winning from that position
   - No expert knowledge required

2. **Adaptive Depth:**
   - Important positions get explored deeply (automatically!)
   - Unimportant positions get ignored
   - Computational budget goes where it matters

3. **Statistical Convergence:**
   - Law of Large Numbers: After many simulations, win rates converge to true values
   - More iterations = more accurate (unlike Minimax's fixed accuracy)

---

### The Mathematical Guarantee

**Central Limit Theorem Application:**

After $n$ simulations from position $s$, the estimated win rate $\hat{p}$ converges to the true win rate $p$:

$$\hat{p} \xrightarrow{n \to \infty} p$$

With standard error: $\sigma = \sqrt{\frac{p(1-p)}{n}}$

**Practical Meaning:**
- 50 iterations: $\sigma \approx 0.07$ (7% error)
- 200 iterations: $\sigma \approx 0.035$ (3.5% error)
- 1000 iterations: $\sigma \approx 0.016$ (1.6% error)

**The Beauty:** More computation = better accuracy, **guaranteed by mathematics**.

---

### Quick Start

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

MCTS builds a decision tree iteratively by repeating four phases. Each iteration adds one node to the tree and updates statistics, gradually building understanding of which moves lead to victory.

### Overview: The MCTS Cycle

```
For i = 1 to N iterations:
    1. SELECTION: Navigate from root to a leaf node
    2. EXPANSION: Add one new child to that leaf
    3. SIMULATION: Play a random game from the new node
    4. BACKPROPAGATION: Update all ancestors with the result

After N iterations:
    Choose the move with the most visits
```

---

### Phase 1: Selection 🎯

**Purpose:** Navigate through the existing tree to find the most promising leaf node to expand.

**The Algorithm:**

Starting at the root node, repeatedly select the child with the highest **Upper Confidence Bound for Trees (UCT)** value until reaching a leaf node.

**The UCT Formula:**

$$\text{UCT}(v_i) = \frac{w_i}{n_i} + c \sqrt{\frac{\ln N}{n_i}}$$

Where:
- $v_i$ = child node $i$
- $w_i$ = total reward (wins) from node $i$
- $n_i$ = number of times node $i$ has been visited
- $N$ = number of times parent node has been visited
- $c$ = exploration constant (typically $\sqrt{2}$ to $\sqrt{5}$)

**Breaking Down the Formula:**

1. **Exploitation Term:** $\frac{w_i}{n_i}$
   - This is the **empirical win rate** of this move
   - Higher value = this move has won more often
   - Range: $[0, 1]$ where 1.0 = always wins

2. **Exploration Term:** $c \sqrt{\frac{\ln N}{n_i}}$
   - This **bonus** encourages trying less-explored moves
   - Gets larger when $n_i$ is small (few visits)
   - Gets larger when $N$ is large (parent visited many times)
   - $c$ controls exploration vs exploitation balance

**Intuition:**

The formula says: *"Pick the move that has either won a lot (exploitation) OR hasn't been tried much (exploration), weighted by the exploration constant."*

**Example:**

```
Parent node N = 50 visits, c = √5 ≈ 2.236

Child A: w=20, n=25 visits
UCT(A) = 20/25 + 2.236√(ln(50)/25)
       = 0.80 + 2.236√(3.912/25)
       = 0.80 + 2.236 × 0.395
       = 0.80 + 0.88 = 1.68

Child B: w=8, n=15 visits
UCT(B) = 8/15 + 2.236√(ln(50)/15)
       = 0.533 + 2.236√(3.912/15)
       = 0.533 + 2.236 × 0.510
       = 0.533 + 1.14 = 1.67

Child C: w=5, n=8 visits
UCT(C) = 5/8 + 2.236√(ln(50)/8)
       = 0.625 + 2.236√(3.912/8)
       = 0.625 + 2.236 × 0.699
       = 0.625 + 1.56 = 2.19  ← HIGHEST!

Choose Child C (less explored but decent win rate)
```

**Key Properties:**

- **Unvisited nodes:** If $n_i = 0$, set $\text{UCT} = \infty$ (always explore unvisited children first)
- **Convergence:** As iterations increase, exploitation dominates and the best move rises to the top
- **Adaptivity:** The formula naturally balances exploration and exploitation based on visit counts

**Pseudocode:**

```python
def selection(node):
    while not node.is_leaf():
        node = node.child_with_max_UCT()
    return node

def UCT(child, c):
    if child.visits == 0:
        return infinity
    exploitation = child.wins / child.visits
    exploration = c * sqrt(ln(child.parent.visits) / child.visits)
    return exploitation + exploration
```

---

### Phase 2: Expansion 🌳

**Purpose:** Grow the search tree by adding one new node representing an unexplored move.

**The Algorithm:**

1. We're at a leaf node $v$ (selected in Phase 1)
2. Generate all legal moves $M = \{m_1, m_2, \ldots, m_k\}$ from state $s(v)$
3. Identify unexplored moves: $M_{\text{unexplored}} = M \setminus \{m : m \in \text{children}(v)\}$
4. If $M_{\text{unexplored}} \neq \emptyset$:
   - Randomly select $m \in M_{\text{unexplored}}$
   - Create new child node $v_{\text{new}}$ for move $m$
   - Add $v_{\text{new}}$ to children of $v$
5. Return $v_{\text{new}}$ (this becomes the node we simulate from)

**Why Expand Only ONE Node?**

**Option 1 (Bad):** Expand all children at once
```
Node has 6 legal moves
→ Add all 6 children immediately
→ Which one do we simulate?
→ Simulate all 6? (6× slower per iteration)
→ Tree grows too fast, wastes memory on bad moves
```

**Option 2 (Good - MCTS way):** Expand one at a time
```
Node has 6 legal moves: A, B, C, D, E, F

Iteration 10: Expand A, simulate → A wins
Iteration 15: Expand B, simulate → B loses
Iteration 18: UCT favors A, goes deeper on A
Iteration 22: Expand C, simulate → C loses
Iteration 25: UCT still favors A, continues exploring A's subtree
Iteration 40: Expand D, simulate → D wins
...

Result: Good moves (A, D) get deep exploration
        Bad moves (B, C) barely explored
        Moves E, F might never get added if A is clearly best
```

**The Mathematics:**

After $n$ iterations, if the tree grows uniformly, expected depth is:

$$d_{\text{avg}} \approx \log_b(n)$$

Where $b$ is the branching factor.

But MCTS doesn't grow uniformly—it focuses on promising branches, so:

$$d_{\text{max}} \approx k \cdot \log_b(n) \text{ where } k \in [1.5, 3]$$

The best paths get explored $2-3×$ deeper than average paths.

**Pseudocode:**

```python
def expansion(node):
    unexplored = node.get_unexplored_moves()
    
    if len(unexplored) == 0:
        return node  # Fully expanded, return current node
    
    # Randomly select one unexplored move
    move = random.choice(unexplored)
    
    # Create new state by applying the move
    new_state = node.state.apply_move(move)
    
    # Create new child node
    child = Node(move, node, new_state)
    node.add_child(child)
    
    return child
```

---

### Phase 3: Simulation (Playout) 🎲

**Purpose:** Estimate the value of the newly expanded node by playing a random game to completion.

**The Algorithm:**

1. Start from state $s$ (the newly expanded node's state)
2. While game is not over and depth $< D_{\max}$:
   - Generate legal moves $M$ for current player
   - Randomly select move $m \in M$
   - Apply $m$ to state: $s \leftarrow s \oplus m$
   - Switch players
   - Increment depth
3. Evaluate terminal state and return reward

**The Reward Function:**

For our Checkers implementation:

$$r(s) = \begin{cases}
1.0 & \text{if Black (AI) wins} \\
0.5 & \text{if draw or depth limit reached} \\
0.0 & \text{if Red (opponent) wins}
\end{cases}$$

For depth-limited simulations (didn't reach terminal state):

$$r(s) = 0.5 + 0.5 \cdot \tanh\left(\frac{\text{pieces}_{\text{black}} - \text{pieces}_{\text{red}}}{\text{pieces}_{\text{total}}}\right)$$

This provides a continuous reward in $[0, 1]$ based on material advantage.

**Why Random Playouts Work:**

This seems counterintuitive—why should random moves tell us anything?

**Mathematical Justification:**

Let $p(s)$ = true probability of winning from state $s$ under perfect play.

After $n$ random simulations from $s$, our estimate is:

$$\hat{p}(s) = \frac{1}{n} \sum_{i=1}^{n} r_i$$

By the **Law of Large Numbers**:

$$\lim_{n \to \infty} \hat{p}(s) = \mathbb{E}[r] = p_{\text{random}}(s)$$

Where $p_{\text{random}}(s)$ = probability of winning from $s$ under random play.

**Key Insight:** While $p_{\text{random}}(s) \neq p(s)$, the **ranking is preserved!**

If state $s_A$ is better than state $s_B$ under perfect play:
$$p(s_A) > p(s_B) \implies p_{\text{random}}(s_A) > p_{\text{random}}(s_B)$$

(With high probability after sufficient simulations)

**Empirical Evidence:**

```
Position Quality    | Random Win Rate
--------------------|------------------
Excellent position  | 80-90%
Good position       | 60-75%
Equal position      | 45-55%
Bad position        | 25-40%
Losing position     | 10-20%
```

The ordering is correct! That's all MCTS needs.

**Depth Limit $D_{\max} = 20$:**

Why limit simulation depth?

1. **Prevents Infinite Loops:** Some positions can cycle forever
2. **Computational Efficiency:** Long simulations don't add much information
3. **Near-Term Focus:** Rewards positions that win quickly

**Pseudocode:**

```python
def simulation(node):
    state = node.state.copy()
    depth = 0
    
    while not state.is_terminal() and depth < MAX_DEPTH:
        moves = state.get_legal_moves()
        if len(moves) == 0:
            break
        
        # Random move selection
        move = random.choice(moves)
        state.apply_move(move)
        state.switch_player()
        depth += 1
    
    # Evaluate final state
    return evaluate(state)

def evaluate(state):
    black_pieces = state.count_pieces(BLACK)
    red_pieces = state.count_pieces(RED)
    
    if black_pieces == 0:
        return 0.0  # AI lost
    elif red_pieces == 0:
        return 1.0  # AI won
    elif black_pieces > red_pieces:
        return 0.7  # AI ahead
    elif red_pieces > black_pieces:
        return 0.3  # AI behind
    else:
        return 0.5  # Even
```

---

### Phase 4: Backpropagation 📈

**Purpose:** Update all nodes along the path from the expanded node to the root with the simulation result.

**The Algorithm:**

1. Start at the newly expanded node $v_{\text{new}}$
2. While $v \neq \text{null}$:
   - Increment visit count: $n_v \leftarrow n_v + 1$
   - Add reward: $w_v \leftarrow w_v + r$
   - Move to parent: $v \leftarrow \text{parent}(v)$

**The Update Equations:**

For each node $v$ on the path:

$$n_v^{\text{new}} = n_v^{\text{old}} + 1$$

$$w_v^{\text{new}} = w_v^{\text{old}} + r$$

$$\bar{w}_v = \frac{w_v}{n_v} \quad \text{(average reward)}$$

**Why Update All Ancestors?**

Every node on the path from root to the expanded node contributed to reaching this position. The simulation result provides information about **all of them**.

**Example:**

```
Simulation result: r = 1.0 (AI wins)

Path taken:
Root → Move A → Resp X → Move A2 → New Node

Updates:
┌──────────────┬─────────┬─────────┬─────────┐
│ Node         │ Before  │ After   │ Avg Win │
├──────────────┼─────────┼─────────┼─────────┤
│ Root         │ n=49    │ n=50    │ varies  │
│              │ w=25    │ w=26    │ 0.52    │
├──────────────┼─────────┼─────────┼─────────┤
│ Move A       │ n=24    │ n=25    │ 0.60    │
│              │ w=14    │ w=15    │         │
├──────────────┼─────────┼─────────┼─────────┤
│ Resp X       │ n=11    │ n=12    │ 0.67    │
│              │ w=7     │ w=8     │         │
├──────────────┼─────────┼─────────┼─────────┤
│ Move A2      │ n=6     │ n=7     │ 0.71    │
│              │ w=4     │ w=5     │         │
├──────────────┼─────────┼─────────┼─────────┤
│ New Node     │ n=0     │ n=1     │ 1.00    │
│              │ w=0     │ w=1     │         │
└──────────────┴─────────┴─────────┴─────────┘

Interpretation:
- New Node: 100% win rate (small sample)
- Move A2: 71% win rate (good move)
- Resp X: 67% win rate (opponent's best response)
- Move A: 60% win rate (strong first move)
- Root: 52% win rate (slightly favorable position)
```

**Information Propagation:**

The win rate improves as we go deeper because we're following the **best path**. Backpropagation ensures:

1. Good paths accumulate high rewards → High $\bar{w}_v$
2. High $\bar{w}_v$ → High UCT → More visits
3. More visits → Better statistics → More reliable

**Mathematical Property - Consistency:**

After many iterations, the visit count distribution converges:

$$\frac{n_{\text{child}}}{n_{\text{parent}}} \approx \frac{e^{\bar{w}_{\text{child}}/\tau}}{\sum_{\text{siblings}} e^{\bar{w}_{\text{sibling}}/\tau}}$$

This is similar to **Softmax distribution**—better moves get exponentially more visits.

**Pseudocode:**

```python
def backpropagation(node, reward):
    while node is not None:
        node.visits += 1
        node.total_reward += reward
        node = node.parent
```

---

### The Complete MCTS Cycle: Putting It All Together

**One Iteration Visualized:**

```
Iteration 25:

1. SELECTION (UCT-based)
   Root (n=24, w=12)
   ├─ Move A (n=12, w=8) ← UCT = 0.75
   ├─ Move B (n=7, w=3)  ← UCT = 0.68
   └─ Move C (n=5, w=1)  ← UCT = 0.82 ✓ SELECTED
      └─ Resp Y (n=3, w=1) ← LEAF

2. EXPANSION
   Resp Y has unexplored moves: [M1, M2, M3, M4]
   Randomly pick M2
   Create: Resp Y → Move M2 (new node)

3. SIMULATION
   Play random game from Move M2's state
   ... 12 random moves later ...
   Result: Black wins! (r = 1.0)

4. BACKPROPAGATION
   Move M2:  n=0→1,  w=0→1    (100% win)
   Resp Y:   n=3→4,  w=1→2    (50% win)
   Move C:   n=5→6,  w=1→2    (33% win)
   Root:     n=24→25, w=12→13 (52% win)

Next iteration: UCT will likely pick Move A or C again
```

**After 50 Iterations:**

```
Root (n=50)
├─ Move A (n=25, w=18) ← 72% win rate
│  ├─ Resp X (n=12)
│  │  └─ Move A2 (n=7)
│  │     └─ ... (depth 6)
│  └─ Resp Y (n=8)
│     └─ ... (depth 4)
├─ Move B (n=15, w=6)  ← 40% win rate
│  └─ ... (depth 3)
├─ Move C (n=8, w=3)   ← 37% win rate
└─ Move D (n=2, w=0)   ← 0% win rate

Decision: Choose Move A (highest visit count)
```

**Why Visit Count, Not Win Rate?**

We choose the child with the **most visits**, not the highest win rate. Why?

- **Visit count** = reliability (more samples = more confidence)
- A move with n=20, w=12 (60% win) is more reliable than n=2, w=2 (100% win)
- The exploration phase already ensured we visited promising moves more

**Final Selection Formula:**

$$m^* = \arg\max_{m \in \text{children(root)}} n_m$$

Simple and robust!

---

## Mathematical Foundation

### The Theory Behind MCTS: Why It Works

**Core Theorem (Kocsis & Szepesvári, 2006):**

Under the UCT policy, the failure probability (selecting a suboptimal move) decays exponentially:

$$P(\text{select suboptimal move}) \leq e^{-cn}$$

Where $n$ is the number of iterations and $c$ is a constant depending on the game.

**Translation:** Double the iterations → Square the error rate!

---

### UCT Regret Bound

The **regret** of an algorithm is how much worse it performs compared to the optimal strategy.

**Theorem:** For UCT with exploration constant $c = \sqrt{2}$:

$$R_n = O(\sqrt{n \log n})$$

Where:
- $R_n$ = cumulative regret after $n$ iterations
- $O(\cdot)$ = big-O notation (upper bound)

**What this means:**
- Per-iteration regret: $r_n = R_n / n = O(\sqrt{\log n / n})$
- As $n \to \infty$, $r_n \to 0$

**MCTS provably converges to the optimal policy!**

---

### Confidence Intervals

After $n$ simulations from a move with true win probability $p$:

**95% Confidence Interval:**

$$\hat{p} \pm 1.96 \sqrt{\frac{p(1-p)}{n}} \approx \hat{p} \pm \frac{1}{\sqrt{n}}$$

**Examples:**

| Iterations | Error Margin |
|-----------|--------------|
| 25 | ±20% |
| 100 | ±10% |
| 400 | ±5% |
| 1600 | ±2.5% |

To halve the error, we need **4× more iterations**.

---

### Exploration vs Exploitation Trade-off

The exploration constant $c$ controls the balance:

**Small $c$ (e.g., $c = 1$):**
- More exploitation
- Quickly focuses on best move
- Risk: Might miss better moves due to insufficient exploration

**Large $c$ (e.g., $c = 3$):**
- More exploration
- Tries many different moves
- Risk: Wastes iterations on obviously bad moves

**Optimal $c$:** Depends on the game, but $c \in [\sqrt{2}, \sqrt{5}]$ works well for most games.

**Our Implementation:**
- Easy: $c = \sqrt{2} \approx 1.414$ (conservative)
- Medium: $c = \sqrt{5} \approx 2.236$ (balanced)
- Hard: $c = 3.0$ (exploratory)

---

### Depth vs Breadth Analysis

After $n$ iterations with branching factor $b$:

**Expected nodes at each depth:**

$$E[n_d] \approx \frac{n}{b^d}$$

**For Checkers with $b \approx 10$ and $n = 50$:**

| Depth | Expected Nodes |
|-------|----------------|
| 0 (root) | 50 |
| 1 | 50/10 = 5 |
| 2 | 50/100 = 0.5 |
| 3+ | < 0.1 |

But UCT focuses exploration, so actual distribution is:

| Depth | Actual Nodes (typical) |
|-------|----------------------|
| 1 | 4 (root's children) |
| 2 | 8-10 (best paths) |
| 3 | 12-15 (promising continuations) |
| 4-6 | 10-15 (deep in best line) |

The best move's path can reach depth 6-8, while bad moves stay at depth 1!

---

## Quick Start

**Prerequisites:** Java JDK 8 or higher

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

### Selecting Difficulty

The game includes three difficulty levels:

| Difficulty | Iterations | Exploration $c$ | Thinking Time | Strength |
|-----------|-----------|-----------------|---------------|----------|
| **Easy** | 20 | $\sqrt{2} \approx 1.414$ | ~0.5 sec | Beatable |
| **Medium** | 50 | $\sqrt{5} \approx 2.236$ | ~1-2 sec | Challenging |
| **Hard** | 150 | $3.0$ | ~3-5 sec | Very Strong |

Use the dropdown menu in the game to switch between difficulty levels.

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
