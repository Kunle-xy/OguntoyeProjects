package edu.iastate.cs472.proj1;

import java.io.FileNotFoundException;

/**
 * Performance benchmarking utility for comparing A* heuristics.
 *
 * @author Kunle Oguntoye
 */
public class PerformanceBenchmark {

    private static class BenchmarkResult {
        String heuristic;
        long timeMs;
        int numMoves;
        int statesExplored;

        BenchmarkResult(String heuristic, long timeMs, int numMoves, int statesExplored) {
            this.heuristic = heuristic;
            this.timeMs = timeMs;
            this.numMoves = numMoves;
            this.statesExplored = statesExplored;
        }

        @Override
        public String toString() {
            return String.format("%-25s | %6d ms | %5d moves | %6d states",
                    heuristic, timeMs, numMoves, statesExplored);
        }
    }

    /**
     * Benchmark a single puzzle with a specific heuristic.
     */
    private static BenchmarkResult benchmarkHeuristic(State initialState, Heuristic h) {
        long startTime = System.currentTimeMillis();

        // Count states explored by tracking CLOSE list size
        OrderedStateList OPEN = new OrderedStateList(h, true);
        OrderedStateList CLOSE = new OrderedStateList(h, false);

        OPEN.addState(initialState);
        State goalState = null;
        int statesExplored = 0;

        while (OPEN.size() > 0) {
            State current = OPEN.remove();

            if (current.isGoalState()) {
                goalState = current;
                break;
            }

            CLOSE.addState(current);
            statesExplored++;

            for (Move move : Move.values()) {
                if (h != Heuristic.DoubleMoveHeuristic) {
                    if (move == Move.DBL_LEFT || move == Move.DBL_RIGHT ||
                        move == Move.DBL_UP || move == Move.DBL_DOWN) {
                        continue;
                    }
                }

                try {
                    State successor = current.successorState(move);
                    if (successor == null) continue;

                    State closedState = CLOSE.findState(successor);
                    if (closedState != null) {
                        if (successor.cost() < closedState.cost()) {
                            CLOSE.removeState(closedState);
                            OPEN.addState(successor);
                        }
                        continue;
                    }

                    State openState = OPEN.findState(successor);
                    if (openState == null) {
                        OPEN.addState(successor);
                    } else if (successor.cost() < openState.cost()) {
                        OPEN.removeState(openState);
                        OPEN.addState(successor);
                    }
                } catch (IllegalArgumentException e) {
                    continue;
                }
            }
        }

        long endTime = System.currentTimeMillis();
        int numMoves = (goalState != null) ? goalState.numMoves : -1;

        return new BenchmarkResult(h.toString(), endTime - startTime, numMoves, statesExplored);
    }

    /**
     * Run benchmarks for all heuristics on a given puzzle.
     */
    public static void runBenchmark(String puzzleFile) {
        try {
            System.out.println("\n" + "=".repeat(70));
            System.out.println("PERFORMANCE BENCHMARK: " + puzzleFile);
            System.out.println("=".repeat(70));

            State initialState = new State(puzzleFile);
            System.out.println("Initial State:");
            System.out.println(initialState);

            if (!initialState.solvable()) {
                System.out.println("Puzzle is UNSOLVABLE. Skipping benchmark.");
                return;
            }

            BenchmarkResult[] results = new BenchmarkResult[3];
            Heuristic[] heuristics = {
                Heuristic.TileMismatch,
                Heuristic.ManhattanDist,
                Heuristic.DoubleMoveHeuristic
            };

            for (int i = 0; i < 3; i++) {
                results[i] = benchmarkHeuristic(initialState, heuristics[i]);
            }

            System.out.println("\nResults:");
            System.out.println("-".repeat(70));
            System.out.println(String.format("%-25s | %10s | %11s | %13s",
                    "Heuristic", "Time (ms)", "Moves", "States Explored"));
            System.out.println("-".repeat(70));

            for (BenchmarkResult result : results) {
                System.out.println(result);
            }

            System.out.println("-".repeat(70));

            // Find best performing heuristic
            BenchmarkResult fastest = results[0];
            for (BenchmarkResult r : results) {
                if (r.timeMs < fastest.timeMs) {
                    fastest = r;
                }
            }

            System.out.println("\nFastest: " + fastest.heuristic +
                    " (" + fastest.timeMs + " ms)");

        } catch (FileNotFoundException e) {
            System.err.println("Error: File not found: " + puzzleFile);
        } catch (IllegalArgumentException e) {
            System.err.println("Error: Invalid puzzle format in " + puzzleFile);
        }
    }

    public static void main(String[] args) {
        String[] testFiles = {
            "examples/medium.txt",
            "examples/hard.txt",
            "8Puzzle.txt"
        };

        System.out.println("\n╔════════════════════════════════════════════════════════════════════╗");
        System.out.println("║          8-PUZZLE A* ALGORITHM PERFORMANCE BENCHMARK              ║");
        System.out.println("╚════════════════════════════════════════════════════════════════════╝");

        for (String file : testFiles) {
            runBenchmark(file);
        }

        System.out.println("\n" + "=".repeat(70));
        System.out.println("Benchmark complete!");
        System.out.println("=".repeat(70) + "\n");
    }
}
