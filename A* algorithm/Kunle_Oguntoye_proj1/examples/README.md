# Example Puzzles

This directory contains sample 8-puzzle configurations with varying difficulty levels.

## Test Cases

### 1. Easy (easy.txt)
```
1 2 3
8 0 4
7 6 5
```
- **Difficulty**: Trivial
- **Optimal Solution**: 0 moves (already at goal state)
- **Purpose**: Test goal state detection

### 2. Medium (medium.txt)
```
2 3 0
1 8 4
7 6 5
```
- **Difficulty**: Easy
- **Optimal Solution**: 2 moves
- **Solution Path**:
  - Move LEFT: `2 _ 3 / 1 8 4 / 7 6 5`
  - Move LEFT: `_ 2 3 / 1 8 4 / 7 6 5` (goal state)
- **Purpose**: Test basic algorithm functionality

### 3. Hard (hard.txt)
```
8 1 2
6 0 3
7 5 4
```
- **Difficulty**: Moderate
- **Optimal Solution**: ~8-10 moves (depending on heuristic)
- **Purpose**: Test algorithm efficiency with more complex puzzles

### 4. Unsolvable (unsolvable.txt)
```
1 2 3
8 0 4
7 5 6
```
- **Difficulty**: Impossible
- **Optimal Solution**: None (unsolvable)
- **Purpose**: Test solvability detection
- **Note**: Tiles 5 and 6 are swapped, creating an odd number of inversions

## Using These Examples

To test with a specific example, modify `PuzzleSolver.java` line 32:

```java
String fileNames[] = new String[] {"examples/medium.txt"};
```

Or run multiple tests in sequence:

```java
String fileNames[] = new String[] {
    "examples/easy.txt",
    "examples/medium.txt",
    "examples/hard.txt",
    "examples/unsolvable.txt"
};
```

## Understanding Solvability

The 8-puzzle has only half of all possible configurations that are solvable. A configuration is solvable if and only if the number of inversions has the same parity as the goal state.

An **inversion** occurs when a larger numbered tile appears before a smaller numbered tile when reading the puzzle left-to-right, top-to-bottom (ignoring the blank).

For the goal state `1 2 3 / 8 0 4 / 7 6 5`, there are 4 inversions (even parity).
For the unsolvable example, there are 5 inversions (odd parity), making it impossible to solve.
