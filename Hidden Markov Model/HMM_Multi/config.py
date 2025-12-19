"""
Centralized Configuration for HMM Trading Strategy
All date settings and parameters in one place for easy adjustment
"""

# ============================================================================
# DATE CONFIGURATION
# ============================================================================



# Data Download Settings
DATA_START_DATE = "2000-01-01"  # Start date for historical data download
DATA_END_DATE = "2008-12-31"    # End date for historical data download

# Train/Test Split
TRAIN_END_DATE = "2007-12-31"   # Last date for training (inclusive)
TEST_START_DATE = "2008-01-01"  # First date for testing (inclusive)

# Visualization Settings
PLOT_START_DATE = "2007-01-01"  # Start date for price chart visualization
                                # (shows context before test period)

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

# HMM Parameters
N_STATES = 2        # Number of hidden states (2 = BULL/BEAR)
WINDOW = 5          # Wavelet window size (days)
SCALE = 5           # Wavelet scale parameter
N_ITER = 100        # Max EM iterations for HMM training
RANDOM_STATE = 42   # Random seed for reproducibility

# ============================================================================
# TRADING CONFIGURATION
# ============================================================================

# Risk Management
INITIAL_CAPITAL = 100000.0    # Starting portfolio value
MAX_POSITION_PCT = 1.0        # Max % of capital to invest (1.0 = 100%)
STOP_LOSS_PCT = 0.02          # Stop loss threshold (0.02 = 2%)

# ============================================================================
# FILE PATHS
# ============================================================================

# Data
TICKER = "SPY"
DATA_DIR = "data"
DATA_FILE = f"{DATA_DIR}/{TICKER}.csv"

# Model
MODEL_DIR = "models"
MODEL_FILE = f"{MODEL_DIR}/hmm_model.pkl"

# Results
RESULTS_DIR = "results"
BACKTEST_RESULTS_FILE = f"{RESULTS_DIR}/backtest_results.csv"
BACKTEST_PLOT_FILE = f"{RESULTS_DIR}/backtest_plot.png"
STATE_STATS_PLOT_FILE = f"{RESULTS_DIR}/state_stats.png"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def print_config():
    """Print current configuration for verification."""
    print("\n" + "="*70)
    print("CURRENT CONFIGURATION")
    print("="*70)

    print("\n--- DATE SETTINGS ---")
    print(f"Data Download:    {DATA_START_DATE} to {DATA_END_DATE}")
    print(f"Training Period:  {DATA_START_DATE} to {TRAIN_END_DATE}")
    print(f"Testing Period:   {TEST_START_DATE} to {DATA_END_DATE}")
    print(f"Plot Start:       {PLOT_START_DATE}")

    print("\n--- MODEL SETTINGS ---")
    print(f"HMM States:       {N_STATES}")
    print(f"Wavelet Window:   {WINDOW} days")
    print(f"Wavelet Scale:    {SCALE}")
    print(f"Max Iterations:   {N_ITER}")

    print("\n--- TRADING SETTINGS ---")
    print(f"Initial Capital:  ${INITIAL_CAPITAL:,.2f}")
    print(f"Max Position:     {MAX_POSITION_PCT*100:.0f}%")
    print(f"Stop Loss:        {STOP_LOSS_PCT*100:.1f}%")

    print("\n--- FILE PATHS ---")
    print(f"Data File:        {DATA_FILE}")
    print(f"Model File:       {MODEL_FILE}")
    print(f"Results File:     {BACKTEST_RESULTS_FILE}")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Print config when run directly
    print_config()
