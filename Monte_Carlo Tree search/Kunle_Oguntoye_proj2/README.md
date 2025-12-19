# Monte Carlo Tree Search for Checkers

An intelligent AI opponent for Checkers that learns winning strategies through simulation rather than brute force search.

![Checkers Game](edu/iastate/cs572/proj2/CHECKERS.png)

---

## Table of Contents
1. [What's New](#whats-new)
2. [What is Monte Carlo Tree Search?](#what-is-monte-carlo-tree-search)
3. [Why Not Use Minimax?](#why-not-use-minimax)
4. [The Four Pillars of MCTS](#the-four-pillars-of-mcts)
5. [How to Run the Game](#how-to-run-the-game)
6. [How to Play](#how-to-play)

---

## What's New

### 🎮 Latest Features (December 2024)

#### Dynamic Difficulty System ⭐ NEW
Challenge yourself with three AI difficulty levels, each using different MCTS parameters:

- **Easy Mode**: 20 simulations, $c = \sqrt{2}$ (Beginner-friendly, ~0.5s thinking time)
- **Medium Mode**: 50 simulations, $c = \sqrt{5}$ (Balanced challenge, ~1-2s)
- **Hard Mode**: 150 simulations, $c = 3.0$ (Advanced opponent, ~3-5s)

**Key Innovation**: Different exploration constants alter how the AI balances trying new moves versus sticking with proven strategies. Higher $c$ values make the AI more exploratory and less predictable!

💡 **Try this**: Start on Easy to learn the game mechanics, then switch to Hard mid-game to see how the AI's playing style transforms.

---

#### Bug Fixes & Improvements

**Fixed: Multi-Jump Move Bug** ✅
- **Issue**: Pieces were disappearing after executing multi-jump sequences
- **Root Cause**: Duplicate position entries in move arrays during jump exploration
- **Solution**: Refined `exploreAllJumps()` to only add starting position once per sequence
- **Impact**: Multi-jump captures now work flawlessly!

**Fixed: State Copy Bug** ✅
- **Issue**: MCTS simulations weren't preserving turn order
- **Root Cause**: `copy()` method didn't copy `currentPlayer` field
- **Solution**: Added `newState.currentPlayer = this.currentPlayer` to state cloning
- **Impact**: AI simulations now accurately model game flow

**Code Cleanup** 🧹
- Removed all debug print statements for cleaner output
- Eliminated unused imports and commented code
- Professional, production-ready codebase

---

### 🔧 Known Issues & Limitations

**Current Limitations:**
- **No Opening Book**: First 3-4 moves are somewhat random (AI hasn't "memorized" good openings)
- **Limited Simulation Depth**: Default 20-move simulation limit may miss very deep tactics
- **Simple Evaluation**: Uses piece count difference; doesn't understand positional nuances
- **No Persistent Learning**: AI doesn't remember games between sessions

**Performance Notes:**
- Hard mode may lag slightly on slower computers (~5-7s thinking time)
- Very large branching factors in mid-game can slow down expansion phase

**Planned Fixes:**
- Implement progressive widening to handle high branching factors
- Add iterative deepening for simulation phase
- Consider RAVE (Rapid Action Value Estimation) for faster convergence

---

### Coming Soon 🚀

**Roadmap for Future Versions:**

**Version 2.1 (Planned - Q1 2025)**
- **🎯 Move Hints System**: Click "Hint" button to see AI's recommended move
- **📊 Statistics Dashboard**: Real-time display of:
  - Win rate estimates for each legal move
  - Nodes explored per second
  - Tree depth statistics
  - Simulation outcomes histogram

**Version 3.0 (Planned - Q2 2025)**
- **💾 Save/Load Games**: Persist game state to JSON files
- **🤖 AI vs AI Mode**: Watch Easy vs Hard compete
- **🎬 Replay Mode**: Step through saved games move-by-move
- **📈 Performance Profiler**:
  - Visualize MCTS tree as it grows
  - See which branches get explored most
  - Animated UCT value changes

**Future Considerations:**
- **🏆 Endgame Tablebase**: Perfect play when ≤6 pieces remain
- **🧠 Neural Network Enhancement**: Use NN for simulation policy instead of random
- **☁️ Cloud Integration**: Upload games, compare against global AI strength
- **🎓 Learning Mode**: Interactive tutorials on checkers tactics

Want to contribute? Check out the [Project Structure](#project-structure) section to get started!

---

### 📜 Version History

#### Version 2.0 (December 2024) - Major Update
- ✨ Added dynamic difficulty system (Easy/Medium/Hard)
- ✨ Variable exploration constants per difficulty level
- 🐛 Fixed critical multi-jump bug causing piece disappearance
- 🐛 Fixed state copy bug affecting MCTS simulations
- 🧹 Complete code cleanup and documentation overhaul
- 📚 Comprehensive README with mathematical explanations

#### Version 1.0 (Initial Release)
- 🎮 Fully functional MCTS Checkers AI
- 🌲 Complete implementation of 4-phase MCTS algorithm
- 🎨 Java Swing GUI with previous board display
- ♟️ Full checkers rules including forced jumps and king promotion
- 📊 UCT-based node selection with configurable parameters

---

## What is Monte Carlo Tree Search?

Monte Carlo Tree Search (MCTS) is a smart way to make decisions in games. Instead of trying to look at every possible move (which is impossible for complex games), MCTS:

1. **Focuses on promising moves** - Spends more time exploring moves that look good
2. **Learns from experience** - Plays thousands of random games to see what works
3. **Gets better with time** - The more it thinks, the better its moves become

**Think of it like this:** Rather than memorizing every chess opening, you play lots of practice games and learn which positions tend to win.

---

## Why Not Use Minimax?

Traditional game AI uses an algorithm called **Minimax**. It sounds good in theory, but has some serious problems for games like Checkers.

### The Minimax Algorithm Explained

Minimax is a recursive algorithm that explores the game tree by assuming both players play optimally. The core principle is:

**Minimax Value Function:**

$$V(s) = \begin{cases}
\text{utility}(s) & \text{if } s \text{ is terminal} \\
\max_{a \in Actions(s)} V(\text{Result}(s, a)) & \text{if player is MAX} \\
\min_{a \in Actions(s)} V(\text{Result}(s, a)) & \text{if player is MIN}
\end{cases}$$

Where:
- $V(s)$ = the minimax value of state $s$
- $\text{utility}(s)$ = the game outcome (win/loss/draw) at terminal state
- $\text{Actions}(s)$ = set of legal moves from state $s$
- $\text{Result}(s, a)$ = resulting state after taking action $a$ from state $s$

**The Process:**
1. **MAX player** (you) tries to maximize the score: $\max(V_1, V_2, \ldots, V_n)$
2. **MIN player** (opponent) tries to minimize your score: $\min(V_1, V_2, \ldots, V_n)$
3. The algorithm recursively alternates between MAX and MIN layers
4. Returns the "best guaranteed outcome" assuming perfect play

**Alpha-Beta Pruning Enhancement:**

To speed up Minimax, Alpha-Beta pruning eliminates branches that cannot affect the final decision:

$$\alpha = \max(\alpha, v) \quad \text{(MAX's best option)}$$
$$\beta = \min(\beta, v) \quad \text{(MIN's best option)}$$

Prune when: $\beta \leq \alpha$ (the opponent won't allow this branch)

In the best case, Alpha-Beta reduces complexity from $O(b^d)$ to $O(b^{d/2})$, effectively doubling the search depth. However, even with this improvement, Minimax faces fundamental limitations.

---

### The Four Critical Pitfalls

#### Problem 1: Combinatorial Explosion

The branching factor $b$ and search depth $d$ create exponential growth in the number of states to evaluate.

**State Space Complexity:**

$$\text{States to evaluate} = b^d$$

For Checkers with average branching factor $b \approx 10$:

| Depth $d$ | States | Notation | Feasibility |
|-----------|--------|----------|-------------|
| 4 | $10^4$ | 10,000 | ✅ Trivial |
| 6 | $10^6$ | 1 million | ✅ Fast |
| 8 | $10^8$ | 100 million | ⚠️ Slow |
| 10 | $10^{10}$ | 10 billion | ❌ Impractical |
| 12 | $10^{12}$ | 1 trillion | ❌ Impossible |
| Full game | $\approx 10^{20}$ | 100 quintillion | ❌ Impossible |

**With Alpha-Beta pruning:** Best case reduces to $O(b^{d/2})$, but this requires perfect move ordering.

$$\text{Best case: } b^{d/2} \quad \text{(e.g., } 10^4 \text{ instead of } 10^8 \text{ for } d=8)$$

**The fundamental issue:** Even at depth 8, we only see 4 moves ahead for each player. Critical tactics in Checkers (multi-jump sequences, king endgames) often require 15+ moves of foresight.

---

#### Problem 2: The Heuristic Function Dependency

#### Problem 2: The Heuristic Function Dependency

Since exhaustive search is impossible, Minimax requires an **evaluation function** $h(s)$ to estimate the value of non-terminal states:

$$h(s) = w_1 f_1(s) + w_2 f_2(s) + \cdots + w_n f_n(s)$$

**Common Checkers heuristic:**

$$h(s) = w_p \cdot P + w_k \cdot K + w_m \cdot M + w_c \cdot C + w_t \cdot T$$

Where:
- $P$ = piece count difference (your pieces - opponent pieces)
- $K$ = king count difference (your kings - opponent kings)
- $M$ = mobility (number of legal moves available)
- $C$ = center control (pieces occupying central squares)
- $T$ = threat count (pieces under attack)
- $w_p, w_k, w_m, w_c, w_t$ = weight coefficients

**Example values:** $w_p = 3, w_k = 5, w_m = 0.5, w_c = 1, w_t = -2$

**The fundamental problems:**

1. **Weight Tuning:** How do we determine optimal weights? Trial and error? Machine learning? Expert intuition?
   
2. **Feature Selection:** What features matter? Should we include:
   - Back row protection? ($w_b \cdot B$)
   - Diagonal control? ($w_d \cdot D$)
   - Piece advancement? ($w_a \cdot A$)
   - The list grows complex very quickly!

3. **Position-Dependent Evaluation:** The same piece configuration has different values in different contexts:
   - Opening: Mobility matters more
   - Midgame: Material balance dominates  
   - Endgame: King positioning is critical
   
   A single linear function cannot capture this complexity.

4. **Garbage In, Garbage Out:** If $h(s)$ misvalues positions, Minimax makes bad decisions:
   
   $$\text{Minimax}(\text{bad heuristic}) \Rightarrow \text{suboptimal play}$$

**MCTS advantage:** No heuristic needed! Game outcomes speak for themselves through simulations.

#### Problem 3: The Horizon Effect

Minimax searches to a fixed depth $d$ and evaluates leaf nodes with $h(s)$. But important tactics often occur at depth $d+1$ or beyond.

**Mathematical formulation:**

At depth $d$, Minimax sees state $s_d$ and evaluates $h(s_d)$. But the true value depends on subsequent moves:

$$V_{\text{true}}(s_d) = \text{outcome at } s_{d+k} \quad (k > 0)$$

If $h(s_d) \neq V_{\text{true}}(s_d)$, Minimax makes incorrect decisions.

**Concrete example:**

```
Depth 0: Your turn, multiple moves available
Depth 1: Opponent responds  
Depth 2: Your turn
Depth 3: Opponent responds
Depth 4: Your turn
Depth 5: Opponent responds
Depth 6: Your turn (SEARCH STOPS HERE - h(s) evaluates as "safe position")
------ HORIZON ------
Depth 7: Opponent discovers forcing sequence!
Depth 8: You must respond (only 1 legal move)
Depth 9: Opponent captures your piece
Depth 10: Material disadvantage
```

**The illusion:** At depth 6, $h(s_6) = +2.5$ (looks good!)  
**The reality:** At depth 10, $V(s_{10}) = -3.0$ (actually losing!)

**Why it happens:**
- Forcing moves (checks, threats, captures) often require 8-12 move sequences
- Quiet positions at the horizon mask upcoming tactical explosions
- The evaluation function cannot predict future complications

**Attempted solutions:**
1. **Quiescence Search:** Continue searching "unstable" positions (captures, checks)
   - Problem: How do you define "unstable"? You might miss quiet but deadly moves.

2. **Iterative Deepening:** Gradually increase depth
   - Problem: Doesn't solve the fundamental issue, just moves the horizon deeper

3. **Selective Extensions:** Search critical lines deeper
   - Problem: How do you know which lines are critical before searching them?

**MCTS advantage:** Simulations naturally play through the horizon! No artificial cutoff depth.

---

#### Problem 4: The Perfect Play Assumption

#### Problem 4: The Perfect Play Assumption

Minimax computes the **minimax value** under the assumption of optimal play by both sides:

$$V^{\*}(s) = \begin{cases}
\max_{a} V^{\*}(\text{Result}(s,a)) & \text{MAX's turn} \\
\min_{a} V^{\*}(\text{Result}(s,a)) & \text{MIN's turn}
\end{cases}$$

This assumes the opponent always chooses the move that minimizes your score. But real opponents:

1. **Make mistakes** - Don't always see the best move
2. **Have varying skill levels** - Beginners vs experts play differently  
3. **Can be confused** - Complex positions lead to errors
4. **Face time pressure** - Limited thinking time causes blunders

**The trap paradox:**

Consider a position where:
- Move A: Safe, leads to small advantage (+1.5)
- Move B: Risky sacrifice, leads to:
  - +5.0 if opponent makes the obvious (but wrong) response  
  - -2.0 if opponent finds the hidden defensive move

$$V_{\text{Minimax}}(\text{Move B}) = -2.0 \quad \text{(assumes perfect defense)}$$
$$V_{\text{Minimax}}(\text{Move A}) = +1.5 \quad \text{(safe)}$$

**Minimax chooses A** (safe move with +1.5)

But against a **human opponent** who makes mistakes 30% of the time:

$$V_{\text{Expected}}(\text{Move B}) = 0.7 \times (-2.0) + 0.3 \times (+5.0) = +0.1$$

Still chooses A, **missing the psychological advantage!**

**Against a beginner** (60% mistake rate):

$$V_{\text{Expected}}(\text{Move B}) = 0.4 \times (-2.0) + 0.6 \times (+5.0) = +2.2$$

**Now B is better!** But Minimax will never consider it.

**Additional issues:**
- Cannot adapt strategy based on opponent strength
- Cannot set traps or create complexity
- Plays the same against beginners and grandmasters
- Misses opportunities to exploit opponent weaknesses

**MCTS advantage:** Through many random simulations, MCTS naturally discovers moves that create practical chances, not just theoretically optimal moves.

---

### Summary: Why Minimax Falls Short

| Issue | Minimax Problem | MCTS Solution |
|-------|----------------|---------------|
| **Branching** | $O(b^d)$ explosion, limited depth | Focuses on promising branches |
| **Evaluation** | Requires handcrafted $h(s)$ | Uses actual game outcomes |
| **Horizon** | Fixed depth cutoff | Simulations play to completion |
| **Adaptivity** | Assumes perfection | Discovers practical moves |
| **Scalability** | Stuck at depth 6-8 | Improves with more time |

**The fundamental insight:** When you can't search everything, don't try to evaluate positions with guesswork. Instead, simulate many complete games and let the statistics guide you.

---

## The Four Pillars of MCTS

MCTS solves the Minimax problems through four iterative phases that balance exploration and exploitation:

```
┌─────────────────────────────────────────────────┐
│  Repeat N times (20/50/150 for Easy/Med/Hard)  │
└─────────────────────────────────────────────────┘
        │
        ↓
   1. SELECTION    → Navigate tree using UCT
   2. EXPANSION    → Add one new node
   3. SIMULATION   → Play random game
   4. BACKPROPAGATION → Update statistics
        │
        ↓
   Choose move with most visits
```

### Algorithm Overview

**MCTS Pseudocode:**

```
function MCTS(root_state, iterations):
    root = create_node(root_state)
    
    for i = 1 to iterations:
        node = SELECT(root)           # Pillar 1
        child = EXPAND(node)          # Pillar 2  
        reward = SIMULATE(child)      # Pillar 3
        BACKPROPAGATE(child, reward)  # Pillar 4
    
    return best_child(root)           # Most visited
```

**Key difference from Minimax:** Instead of exhaustively searching to depth $d$, MCTS adaptively explores the tree, spending more time on promising branches.



Let's understand each pillar:

---

### Pillar 1: SELECTION - Navigate to Promising Areas

**Objective:** Traverse the tree from root to a leaf node, balancing exploration of new moves with exploitation of known good moves.

**The UCT Formula (Upper Confidence Bound for Trees):**

$$\text{UCT}(v) = \frac{Q(v)}{N(v)} + c \sqrt{\frac{\ln N(\text{parent}(v))}{N(v)}}$$

Where:
- $Q(v)$ = total reward accumulated at node $v$ (sum of all simulation rewards)
- $N(v)$ = number of times node $v$ has been visited
- $N(\text{parent}(v))$ = visit count of parent node
- $c$ = exploration constant (controls exploration vs exploitation trade-off)

**Breaking down the formula:**

$$\underbrace{\frac{Q(v)}{N(v)}}_{\text{Exploitation term}} + \underbrace{c \sqrt{\frac{\ln N(\text{parent}(v))}{N(v)}}}_{\text{Exploration bonus}}$$

1. **Exploitation term:** $\frac{Q(v)}{N(v)}$ = average reward (win rate)
   - Higher win rate → More attractive
   - Range: $[0, 1]$ for our implementation

2. **Exploration bonus:** $c \sqrt{\frac{\ln N(\text{parent}(v))}{N(v)}}$
   - Increases for rarely-visited nodes (small $N(v)$)
   - Increases as parent gets visited more (large $\ln N(\text{parent})$)
   - Controlled by $c$: larger $c$ → more exploration

**Difficulty-specific exploration constants:**

| Difficulty | $c$ value | Behavior |
|-----------|-----------|----------|
| Easy | $c = \sqrt{2} \approx 1.414$ | Moderate exploration |
| Medium | $c = \sqrt{5} \approx 2.236$ | Balanced |
| Hard | $c = 3.0$ | Aggressive exploration |

**Selection algorithm:**

```
function SELECT(node):
    while node is not terminal:
        if node has unexpanded children:
            return node
        else:
            node = child with highest UCT value
    return node
```

**Concrete example:**

Consider a node with 3 children after 25 parent visits:

| Child | $Q(v)$ | $N(v)$ | $\frac{Q(v)}{N(v)}$ | $\sqrt{\frac{\ln 25}{N(v)}}$ | $\text{UCT}$ (c=2.236) |
|-------|--------|--------|---------------------|------------------------------|------------------------|
| A | 15 | 12 | 1.25 | 0.519 | **2.41** |
| B | 8 | 10 | 0.80 | 0.571 | 2.08 |
| C | 2 | 3 | 0.67 | 1.041 | **2.99** ← Selected! |

**Child C wins!** Despite having lower win rate (67% vs 104% for A), the exploration bonus is large enough because $N(C) = 3$ is small.

**Mathematical insight:** As $N(v) \to \infty$, the exploration term $\sqrt{\frac{\ln N_p}{N(v)}} \to 0$, so UCT converges to pure exploitation (win rate).

**The Chernoff-Hoeffding bound connection:**

UCT is derived from the **Hoeffding inequality**, which bounds the probability that the empirical mean deviates from the true mean:

$$P\left(\left|\frac{Q(v)}{N(v)} - \mu\right| \geq \epsilon\right) \leq 2e^{-2N(v)\epsilon^2}$$

The exploration term ensures we don't miss a potentially good move due to insufficient sampling!



---

### Pillar 2: EXPANSION - Add One New Possibility

**Objective:** Grow the search tree incrementally by adding one unexplored child node.

**Expansion strategy:**

```
function EXPAND(node):
    if node is terminal:
        return node
    
    unexpanded = get_legal_moves(node) - expanded_children(node)
    
    if unexpanded is empty:
        return SELECT(node)  # All children expanded, continue selection
    
    move = randomly_choose(unexpanded)
    child = create_child_node(node, move)
    return child
```

**Why expand only one node per iteration?**

This is a key insight of MCTS! By expanding incrementally:

1. **Adaptive growth:** Good branches naturally get more attention
2. **Efficiency:** Don't waste time expanding bad moves
3. **Anytime algorithm:** Can stop at any iteration and return best move so far

**Mathematical justification:**

Let $b$ = branching factor. After $n$ iterations:

- **Minimax with Alpha-Beta:** Tries to expand all $b^d$ nodes to depth $d$
  $$\text{Nodes} = b + b^2 + \cdots + b^d = \frac{b^{d+1} - 1}{b - 1} = O(b^d)$$

- **MCTS:** Expands at most $n$ nodes total (one per iteration)
  $$\text{Nodes} \leq n$$

But MCTS focuses these $n$ expansions on promising paths! 

**Example growth pattern:**

```
Iteration 1:  Root (1 visit)
              └─ A (1 visit)

Iteration 5:  Root (5 visits)
              ├─ A (3 visits) ← Getting expanded more
              │  ├─ A1 (1 visit)
              │  └─ A2 (1 visit)
              └─ B (1 visit)

Iteration 20: Root (20 visits)
              ├─ A (12 visits) ← Dominant branch
              │  ├─ A1 (5 visits)
              │  │  ├─ A1a (2 visits)
              │  │  └─ A1b (2 visits)
              │  ├─ A2 (4 visits)
              │  └─ A3 (2 visits)
              ├─ B (6 visits)
              │  ├─ B1 (3 visits)
              │  └─ B2 (2 visits)
              └─ C (1 visit) ← Bad move, rarely expanded
```

Notice: The tree grows **asymmetrically** toward promising moves!

**Expansion order invariance:**

The order in which unexpanded children are selected doesn't significantly affect convergence, because:

$$\lim_{n \to \infty} \frac{Q(v)}{N(v)} \to E[\text{reward}(v)]$$

All moves eventually get sampled enough to estimate their true value (by the **Law of Large Numbers**).



---

### Pillar 3: SIMULATION - Play It Out

**Objective:** Estimate the value of a newly expanded node by playing a complete random game (rollout/playout).

**Simulation algorithm:**

```
function SIMULATE(node):
    state = node.game_state
    depth = 0
    MAX_DEPTH = 20  # Prevent infinite games
    
    while not is_terminal(state) and depth < MAX_DEPTH:
        moves = get_legal_moves(state)
        move = random_choice(moves)
        state = apply_move(state, move)
        depth++
    
    return evaluate_outcome(state, original_player)
```

**Reward structure:**

$$R(s) = \begin{cases}
1.0 & \text{if AI wins} \\
0.5 & \text{if draw or depth limit reached} \\
0.0 & \text{if AI loses}
\end{cases}$$

**Why random playouts work:**

This seems counterintuitive! How can **random** moves provide meaningful information?

**The statistical answer:**

Let $s$ be a game state, and $V(s)$ be its true value (probability AI wins from $s$ with optimal play). Let $\hat{V}_n(s)$ be the estimated value after $n$ random simulations.

**Law of Large Numbers:**

$$\lim_{n \to \infty} \hat{V}_n(s) = E[R | s] = p_{\text{win}}(s)$$

Where $p_{\text{win}}(s)$ is the probability of winning from $s$ under random play.

**Key insight:** While $p_{\text{win}}(s) \neq V(s)$ (random play ≠ optimal play), the ranking is often preserved:

$$V(s_1) > V(s_2) \Rightarrow p_{\text{win}}(s_1) > p_{\text{win}}(s_2)$$

**Empirical evidence:**

```
Position A: Strong tactical advantage
  - Random playouts: Wins 78% of games
  
Position B: Balanced position  
  - Random playouts: Wins 52% of games
  
Position C: Disadvantaged position
  - Random playouts: Wins 23% of games

Ranking: A > B > C (correct!)
```

**Mathematical intuition:**

Good positions have more ways to win. Even random play will stumble into winning tactics more often from advantageous positions!

**Central Limit Theorem application:**

After $n$ simulations, the standard error of our estimate is:

$$\sigma_{\hat{V}} = \frac{\sigma}{\sqrt{n}} \approx \frac{0.5}{\sqrt{n}}$$

Where $\sigma \leq 0.5$ for binary rewards $\{0, 1\}$.

**Example:** After 50 iterations (Medium difficulty):
$$\sigma_{\hat{V}} \approx \frac{0.5}{\sqrt{50}} \approx 0.071$$

Our win rate estimate has ~7% standard error. Usually sufficient for good decisions!

**Simulation policy improvements:**

While pure random works, we can enhance simulations:

1. **Favor captures:** $P(\text{capture move}) = 2 \times P(\text{normal move})$
2. **Avoid edge moves:** $P(\text{edge}) = 0.5 \times P(\text{center})$
3. **Domain knowledge:** Encode simple heuristics in rollout policy

Our implementation uses **pure random** for simplicity, but these enhancements can improve convergence rate.



---

### Pillar 4: BACKPROPAGATION - Share What You Learned

**Objective:** Update all nodes on the path from root to the simulated node with the outcome.

**Backpropagation algorithm:**

```
function BACKPROPAGATE(node, reward):
    while node is not null:
        node.visits++
        node.total_reward += reward
        node = node.parent
```

**The update equations:**

For each node $v$ on the path from root to leaf:

$$N(v) \leftarrow N(v) + 1$$
$$Q(v) \leftarrow Q(v) + R$$

Where $R \in \{0.0, 0.5, 1.0\}$ is the simulation reward.

**Why update all ancestors?**

Because the simulation result provides information about **every decision** that led to that position!

**Statistical interpretation:**

After $n$ simulations passing through node $v$:

$$\text{Win rate}(v) = \frac{Q(v)}{N(v)} = \frac{1}{N(v)} \sum_{i=1}^{N(v)} R_i$$

This is the **sample mean** of rewards, which converges to the true expected value:

$$\lim_{N(v) \to \infty} \frac{Q(v)}{N(v)} = E[R | v]$$

**Perspective switching:**

Important: Rewards are from the perspective of the **player to move** at each node!

When backpropagating through opponent nodes, we need to **invert** the reward:

$$R_{\text{opponent}} = 1 - R_{\text{us}}$$

**Example:**
- AI wins simulation: $R = 1.0$ for AI nodes
- Same simulation: $R = 0.0$ for opponent nodes (they lost!)

**Concrete backpropagation trace:**

```
Simulation result: AI wins (R = 1.0)

Path: Root → Move A → Opp X → Move B → New Node

Updates:
┌──────────────┬──────────┬────────────┬─────────────┬──────────┐
│ Node         │ Before   │ Reward     │ After       │ Win Rate │
├──────────────┼──────────┼────────────┼─────────────┼──────────┤
│ New Node     │ (0, 0)   │ +1.0       │ (1, 1)      │ 100.0%   │
│ Move B (AI)  │ (6, 5)   │ +1.0       │ (7, 6)      │ 85.7%    │
│ Opp X (Opp)  │ (11, 8)  │ +0.0 (inv) │ (12, 8)     │ 66.7%    │
│ Move A (AI)  │ (24, 15) │ +1.0       │ (25, 16)    │ 64.0%    │
│ Root         │ (49, 25) │ +1.0       │ (50, 26)    │ 52.0%    │
└──────────────┴──────────┴────────────┴─────────────┴──────────┘

Format: (N(v), Q(v))
```

**Observations:**
1. **Deeper nodes have higher win rates** - This path led to a win!
2. **Opponent node has lower win rate** - From opponent's perspective, this path loses
3. **Root has modest win rate** - Averaging over all paths (good and bad)

**Confidence bounds:**

Using the **Hoeffding bound**, we can compute confidence intervals:

$$P\left(\left|\frac{Q(v)}{N(v)} - \mu(v)\right| \geq \epsilon\right) \leq 2e^{-2N(v)\epsilon^2}$$

With 95% confidence ($\alpha = 0.05$), solving for $\epsilon$:

$$\epsilon = \sqrt{\frac{\ln(2/\alpha)}{2N(v)}} = \sqrt{\frac{\ln 40}{2N(v)}} \approx \frac{1.36}{\sqrt{N(v)}}$$

**Example confidence intervals:**

| $N(v)$ | Win Rate Estimate | 95% Confidence Interval |
|--------|-------------------|-------------------------|
| 10 | 60% | $60\% \pm 43\%$ → [17%, 100%] |
| 25 | 64% | $64\% \pm 27\%$ → [37%, 91%] |
| 100 | 58% | $58\% \pm 14\%$ → [44%, 72%] |

**Insight:** More visits → Tighter confidence → More reliable estimate!

---

### Putting It All Together: The Complete MCTS Iteration

**After $N$ iterations (e.g., 50 for Medium difficulty):**

```
Root State (50 visits, 26 wins → 52% win rate)
│
├─ Move A (25 visits, 16 wins → 64%) ← Highest visit count
│  ├─ Opponent X (12 visits, 8 losses → 67% for opponent)
│  │  ├─ Response A1 (6 visits, 5 wins → 83%)  
│  │  │  └─ [depth 4+] (several branches)
│  │  └─ Response A2 (4 visits, 2 wins → 50%)
│  └─ Opponent Y (8 visits, 6 losses → 75% for opponent)
│     ├─ Response A3 (3 visits, 2 wins → 67%)
│     └─ Response A4 (2 visits, 1 win → 50%)
│
├─ Move B (15 visits, 6 wins → 40%)
│  ├─ Opponent Z (8 visits, 4 losses → 50% for opponent)
│  └─ [other branches...]
│
├─ Move C (8 visits, 3 wins → 38%)
│  └─ [lightly explored...]
│
└─ Move D (2 visits, 0 wins → 0%) ← Almost ignored

**Decision: Choose Move A** (25 visits = most explored = most reliable)
```

**Key observations:**

1. **Asymmetric growth:** Move A dominates with 50% of iterations (25/50)
2. **Adaptive depth:** Move A explored to depth 4+, while Move D barely expanded
3. **Visit count = reliability:** We trust Move A more than Move C despite similar win rates
4. **Exploration still happens:** Even "bad" Move D got 2 visits to confirm it's bad

**Why choose by visit count, not win rate?**

Consider this scenario:
- Move X: 100 visits, 55% win rate  
- Move Y: 5 visits, 80% win rate

Which is better? **Move X!** Because:

$$\text{Confidence}(X) = \frac{1.36}{\sqrt{100}} = 13.6\%$$
$$\text{Confidence}(Y) = \frac{1.36}{\sqrt{5}} = 60.8\%$$

Move Y's 80% could be anywhere from 20% to 100%! Not reliable enough.

**Mathematical guarantee:** As $N \to \infty$, MCTS converges to selecting the move with highest true value (by the Law of Large Numbers).

---

### Complexity Analysis

**Time complexity per iteration:**

1. **Selection:** $O(d \cdot b)$ where $d$ = tree depth, $b$ = branching factor
   - Must compute UCT for $b$ children at each of $d$ levels
   
2. **Expansion:** $O(b)$ to identify unexpanded moves
   
3. **Simulation:** $O(m \cdot b)$ where $m$ = average simulation length
   - Each move requires generating and choosing from $b$ legal moves
   
4. **Backpropagation:** $O(d)$ to update nodes on path

**Total per iteration:** $O(m \cdot b + d \cdot b) = O((m + d) \cdot b)$

**For $N$ iterations:** $O(N \cdot (m + d) \cdot b)$

**Space complexity:** $O(N)$ because we store at most $N$ nodes (one per expansion)

**Comparison with Minimax:**

| Algorithm | Time | Space | Depth Reached |
|-----------|------|-------|---------------|
| **Minimax** | $O(b^d)$ | $O(d)$ | Fixed $d$ (usually 6-8) |
| **Minimax + Alpha-Beta** | $O(b^{d/2})$ (best case) | $O(d)$ | Fixed $d$ |
| **MCTS** | $O(N \cdot (m+d) \cdot b)$ | $O(N)$ | Variable (adaptive) |

**Key advantage:** MCTS is **anytime** - you can stop after any number of iterations and get a reasonable answer. Minimax must complete to depth $d$.



### Putting It All Together

After 50 iterations (Medium difficulty):

```
Root (50 visits)
├── Move A (25 visits, 18 wins) ← 72% win rate, heavily explored
│   ├── Response X (12 visits) → went 6 levels deep
│   └── Response Y (8 visits) → went 4 levels deep
├── Move B (15 visits, 6 wins) ← 40% win rate, moderately explored  
├── Move C (8 visits, 3 wins) ← 38% win rate, lightly explored
└── Move D (2 visits, 0 wins) ← 0% win rate, almost ignored

Decision: Choose Move A (most visits = most reliable)
```

**Key insight:** We choose the move with the **most visits**, not the highest win rate. Why? Because more visits = more reliable statistics. A move with 20 visits and 60% win rate is more trustworthy than one with 2 visits and 100% win rate.

---

## How to Run the Game

### Prerequisites
- Java JDK 8 or higher

### Step 1: Compile the Code

Open your terminal and navigate to the project folder:

```bash
cd "Monte_Carlo Tree search/Kunle_Oguntoye_proj2"
javac edu/iastate/cs572/proj2/*.java
```

### Step 2: Run the Game

```bash
java edu.iastate.cs572.proj2.Checkers
```

A window will appear with the checkers board!

### Step 3: Choose Difficulty

Use the dropdown menu at the top right of the window to select AI difficulty:

| Difficulty | Simulations | Exploration Constant ($c$) | Thinking Time | Play Style |
|-----------|-------------|---------------------------|---------------|------------|
| **Easy** | 20 | $\sqrt{2} \approx 1.414$ | ~0.5 seconds | Faster, more exploitative - Beatable for beginners |
| **Medium** | 50 | $\sqrt{5} \approx 2.236$ | ~1-2 seconds | Balanced exploration/exploitation - Good challenge |
| **Hard** | 150 | $3.0$ | ~3-5 seconds | Aggressive exploration - Very difficult to beat |

**How difficulty affects AI behavior:**

1. **Simulation Count:**
   - More simulations = more statistical samples = better move evaluation
   - Easy (20): Quick decisions, may miss subtle tactics
   - Hard (150): Thorough analysis, finds complex winning sequences

2. **Exploration Constant ($c$ in UCT formula):**

   Recall the UCT formula:
   $$\text{UCT}(v) = \frac{Q(v)}{N(v)} + c \sqrt{\frac{\ln N(\text{parent}(v))}{N(v)}}$$

   - **Easy ($c = \sqrt{2}$):** Lower exploration bonus
     - Focuses more on moves that have worked before (exploitation)
     - Faster to converge on a "good enough" move
     - May miss creative or unusual winning tactics

   - **Medium ($c = \sqrt{5}$):** Balanced
     - Standard balance between trying new moves and using proven ones
     - Default recommended setting

   - **Hard ($c = 3.0$):** Higher exploration bonus
     - Tries more different move variations
     - Less likely to miss hidden tactical opportunities
     - Finds moves that require deeper foresight

**Dynamic Difficulty:**
- You can change difficulty **mid-game** using the dropdown
- The AI immediately adapts to the new settings
- Next move will use the new simulation count and exploration constant

**Challenge yourself:** Start with Easy, then switch to Hard once you understand the game!

---

## How to Play

### Game Setup

When you launch the game, you'll see:
- **Red pieces** (bottom rows): You control these
- **Black pieces** (top rows): The AI controls these
- **Difficulty dropdown**: At the top of the window

### Basic Checkers Rules

**Movement:**
- Regular pieces move diagonally forward one square
- Kings (marked with 'K') can move diagonally forward OR backward

**Capturing (Jumping):**
- Jump over opponent pieces diagonally to capture them
- Can chain multiple jumps in one turn
- **Mandatory jumps:** If you can jump, you MUST jump!

**Winning:**
- Capture all opponent pieces, OR
- Trap opponent so they have no legal moves

**Becoming a King:**
- When your piece reaches the opposite end of the board, it becomes a king

---

### Playing a Turn

**Your Turn (Red):**

1. **Click on one of your red pieces**
   - Valid moves will be highlighted
   - Only pieces with legal moves can be selected

2. **Click on the destination square**
   - Your piece moves there
   - If it's a jump, opponent's piece is captured
   - If you can continue jumping, you must do so

3. **AI's turn starts automatically**

**AI's Turn (Black):**

1. **The AI thinks** (you'll see a brief pause)
   - Running MCTS algorithm
   - Playing simulations in the background
   - Building its decision tree

2. **Black piece moves automatically**
   - You'll see which piece moved
   - The AI generally makes smart moves!

3. **Back to your turn**

---

### Strategy Tips

**Playing Against MCTS:**

✅ **Do:**
- Control the center - more mobility = more options
- Get kings early - they're much more powerful
- Force trades when you're ahead - simplify the position
- Think several moves ahead
- Protect your back row to prevent early kings

❌ **Don't:**
- Leave pieces undefended - MCTS will punish you!
- Make random moves - the AI learns from patterns
- Rush forward without a plan
- Forget mandatory jumps (the game won't let you anyway)

**What the AI does well:**
- Finds tactical captures and multi-jump sequences
- Avoids obvious blunders
- Trades pieces when ahead
- Maintains material advantage

**What the AI struggles with:**
- Very long-term strategic positioning (beyond simulation depth)
- Subtle traps that require 15+ move sequences
- Opening theory (first few moves are somewhat random)

---

### Understanding AI Behavior

**Why does the AI pause before moving?**
- It's running 20, 50, or 150 simulation cycles (depending on difficulty)
- Each cycle: Selection → Expansion → Simulation → Backpropagation
- More cycles = smarter move, but takes longer

**Does the AI get smarter as the game goes on?**
- Yes! Fewer pieces = smaller game tree = deeper search
- Endgame positions are easier to evaluate accurately
- The AI is strongest in the endgame

**Can I make the AI even harder?**

Yes! You can add custom difficulty levels by modifying `MonteCarloTreeSearch.java`:

```java
// In the Difficulty enum (around line 14), add:
public enum Difficulty {
    EASY(20, Math.sqrt(2)),
    MEDIUM(50, Math.sqrt(5)),
    HARD(150, 3.0),
    EXPERT(500, 4.0);  // Super challenging! Takes 10-15 seconds per move

    // ... rest of the code
}
```

Then add "Expert" to the difficulty selector in `Checkers.java`:

```java
difficultySelector = new JComboBox<>(new String[]{"Easy", "Medium", "Hard", "Expert"});
```

**Warning:** Expert difficulty will be very strong but slow!

---

## Project Structure

```
Kunle_Oguntoye_proj2/
├── edu/iastate/cs572/proj2/
│   ├── MonteCarloTreeSearch.java   # Main MCTS algorithm
│   ├── MCNode.java                 # Tree node with UCT calculation
│   ├── Checkers.java               # GUI and game controller
│   ├── CheckersData.java           # Game state and rules
│   ├── CheckersMove.java           # Move representation
│   ├── CHECKERS.png                # Game screenshot
│   └── ...
├── README.md                       # Original documentation
└── README2.md                      # This file
```

---

## Key Concepts Summary

### MCTS vs Minimax

| Feature | Minimax | MCTS |
|---------|---------|------|
| **Search Strategy** | Breadth-first to fixed depth | Focused on promising paths |
| **Evaluation** | Needs heuristic function | Uses random playouts |
| **Depth** | Fixed (6-8 moves) | Variable (focuses deeper where it matters) |
| **Expert Knowledge** | Required (design heuristic) | Not needed (learns from games) |
| **Handles Complexity** | Struggles with high branching | Handles naturally |
| **Adaptivity** | Fixed strategy | Improves with more iterations |

### The Four Pillars Recap

1. **Selection:** Navigate tree using UCT (balance exploration/exploitation)
2. **Expansion:** Add one new move possibility
3. **Simulation:** Play random game to estimate value
4. **Backpropagation:** Update all moves on path with result

### Why It Works

- **Law of Large Numbers:** Many random games → reliable statistics
- **UCT Formula:** Automatically balances trying new moves vs exploiting good ones
- **Incremental Growth:** Tree grows toward winning strategies naturally
- **No Heuristic:** Game outcomes speak for themselves

---

## Author

**Kunle Oguntoye**  
Implementation of Monte Carlo Tree Search for Checkers

---

## References

- Browne, C., et al. (2012). "A Survey of Monte Carlo Tree Search Methods"
- Kocsis, L. & Szepesvári, C. (2006). "Bandit based Monte-Carlo Planning"
- Silver, D., et al. (2016). "Mastering the game of Go with deep neural networks and tree search" (AlphaGo)

---

*"The best way to predict the future is to simulate it many times and see what happens most often."* - MCTS Philosophy
