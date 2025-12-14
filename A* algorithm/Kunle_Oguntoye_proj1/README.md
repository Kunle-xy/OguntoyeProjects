# 8-Puzzle Solver Using A* Algorithm

A Java implementation of the A* search algorithm to solve the classic 8-puzzle problem using multiple heuristics.

## Overview

The 8-puzzle is a sliding puzzle consisting of a 3x3 grid with 8 numbered tiles and one empty space. The goal is to rearrange the tiles from a given initial configuration to the target configuration:

```
1 2 3
8   4
7 6 5
```

This implementation uses the A* search algorithm with three different heuristics to find optimal solutions.

## Features

- **Multiple Heuristics**: Solves puzzles using three different heuristics:
  - **Tile Mismatch**: Counts the number of tiles not in their goal positions
  - **Manhattan Distance**: Sum of the Manhattan distances of each tile from its goal position
  - **Double Move Heuristic**: Optimized heuristic that allows double moves (moving two tiles at once)

- **Efficient Data Structures**: Uses circular doubly-linked lists for OPEN and CLOSED lists

- **Solvability Check**: Automatically detects unsolvable puzzle configurations using inversion count

- **Flexible Input**: Accepts puzzle configurations from text files

## Algorithm Details

### A* Search

A* is an informed search algorithm that uses a cost function `f(n) = g(n) + h(n)` where:
- `g(n)` is the cost to reach the current state from the initial state
- `h(n)` is the estimated cost to reach the goal from the current state (heuristic)

The algorithm maintains two lists:
- **OPEN**: States to be explored, sorted by increasing cost
- **CLOSED**: Already explored states

### Heuristics

1. **Tile Mismatch** (h₁):
   - Counts how many tiles are not in their correct positions
   - Admissible but not very informative

2. **Manhattan Distance** (h₂):
   - For each tile, computes the sum of horizontal and vertical distance to its goal position
   - More informative than tile mismatch, often finds solutions faster

3. **Double Move Heuristic** (h₃):
   - Allows moving two tiles in one move when the empty space is at an edge
   - Uses `⌈Manhattan Distance / 2⌉` as the heuristic value
   - Finds shorter solution paths when double moves are allowed

All three heuristics are **admissible** (never overestimate the actual cost), ensuring optimal solutions.

## Project Structure

```
Kunle_Oguntoye_proj1/
├── edu/iastate/cs472/proj1/
│   ├── EightPuzzle.java          # Main solver with A* implementation
│   ├── State.java                 # Represents a puzzle configuration
│   ├── OrderedStateList.java      # Circular doubly-linked list for OPEN/CLOSED
│   ├── PuzzleSolver.java          # Entry point for running the solver
│   ├── Heuristic.java             # Enum for heuristic types
│   ├── Move.java                  # Enum for possible moves
│   ├── StateComparator.java       # Comparator for lexicographic ordering
│   └── 8Puzzle.txt                # Sample puzzle configuration
└── README.md                      # This file
```

## How to Run

### Prerequisites
- Java Development Kit (JDK) 8 or higher

### Compilation

Navigate to the project directory and compile all Java files:

```bash
cd A*/Kunle_Oguntoye_proj1
javac edu/iastate/cs472/proj1/*.java
```

### Running the Solver

```bash
java edu.iastate.cs472.proj1.PuzzleSolver
```

The solver will read the puzzle from `8Puzzle.txt` and display solutions using all three heuristics.

### Running Performance Benchmarks

To compare the performance of different heuristics:

```bash
javac edu/iastate/cs472/proj1/PerformanceBenchmark.java
java edu.iastate.cs472.proj1.PerformanceBenchmark
```

This will test all three heuristics on multiple puzzles and display:
- Execution time
- Number of moves in the solution
- Number of states explored

The benchmark helps visualize the trade-offs between different heuristics.

### Input Format

Create a text file with the puzzle configuration. Each row should contain three digits (0-8) separated by spaces, where 0 represents the empty square:

```
8 1 2
6 0 3
7 5 4
```

## Example Output

```
Solving puzzle from file: 8Puzzle.txt
==================================================
Initial state:
2 3
1 8 4
7 6 5

Solution 1 using heuristic: TileMismatch
2 moves to the solution:

2 3
1 8 4
7 6 5

Move: LEFT
2   3
1 8 4
7 6 5

Move: LEFT
  2 3
1 8 4
7 6 5

...
```

## Technical Highlights

### Data Structures
- **Circular Doubly-Linked Lists**: Efficient insertion and deletion for OPEN/CLOSED lists
- **State Caching**: Heuristic values are computed once and cached to avoid redundant calculations

### Optimizations
- **Duplicate Detection**: States are checked against OPEN and CLOSED lists before expansion
- **Cost Updating**: If a better path to an existing state is found, the state is updated
- **Early Goal Detection**: Search terminates immediately upon finding the goal state

### Error Handling
- Validates input puzzle configurations (must be 3x3 with digits 0-8)
- Checks for solvability before attempting to solve
- Handles file not found and invalid format exceptions

## Performance

The algorithm's performance depends on the heuristic and initial configuration:
- **Tile Mismatch**: Explores more states, slower but still finds optimal solution
- **Manhattan Distance**: More efficient, explores fewer states
- **Double Move**: Finds shorter paths (fewer moves) when double moves are allowed

## Author

**Kunle Oguntoye**

## License

This project is available for educational and portfolio purposes.
