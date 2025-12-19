"""
Main runner script - Execute the full pipeline
"""

import subprocess
import sys
import os
from config import print_config

def run_step(script_name: str, description: str):
    """Run a script and handle errors."""
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"{'='*60}\n")
    
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    
    if result.returncode != 0:
        print(f"\nERROR: {script_name} failed!")
        sys.exit(1)
    
    print(f"\n✓ {description} completed successfully")


def main():
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print("="*70)
    print("HMM GAUSSIAN MULTIVARIATE TRADING STRATEGY")
    print("="*70)

    # Display current configuration
    print_config()

    print("\nThis pipeline will:")
    print("1. Download historical data")
    print("2. Train HMM on training period")
    print("3. Backtest on test period")
    print("4. Generate visualizations")
    print("\nTIP: Edit config.py to adjust dates and parameters")

    # Create directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    # Run pipeline
    run_step("1_download_data.py", "Download SPY Data")
    run_step("3_train_hmm.py", "Train HMM Model")
    run_step("4_backtest.py", "Backtest Strategy")
    run_step("5_visualize.py", "Generate Plots")
    
    print("\n" + "="*60)
    print("PIPELINE COMPLETE!")
    print("="*60)
    print("\nOutputs:")
    print("  - data/SPY.csv                   : Raw price data")
    print("  - models/hmm_model.pkl           : Trained HMM model")
    print("  - results/backtest_results.csv   : Daily backtest results")
    print("  - results/backtest_plot.png      : Main performance chart")
    print("  - results/state_stats.png        : State analysis chart")


if __name__ == "__main__":
    main()
