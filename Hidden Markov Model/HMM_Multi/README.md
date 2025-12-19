# HMM Multivariate Trading Strategy

A Hidden Markov Model (HMM) trading strategy using multivariate observations (returns + wavelet energy) for regime detection.

## Quick Start

1. **Configure your settings** in `config.py`:
   ```python
   # Adjust these dates for your needs
   DATA_START_DATE = "2000-01-01"  # Start of historical data
   DATA_END_DATE = "2025-12-31"    # End of historical data
   TRAIN_END_DATE = "2024-12-31"   # Last date for training
   TEST_START_DATE = "2025-01-01"  # First date for testing
   PLOT_START_DATE = "2024-01-01"  # Start date for visualization
   ```

2. **Run the complete pipeline**:
   ```bash
   python run_pipeline.py
   ```

   This will:
   - Download SPY data for your configured date range
   - Train the HMM model on the training period
   - Backtest the strategy on the test period
   - Generate visualization plots

## Configuration

All settings are centralized in `config.py`:

### Date Settings
- `DATA_START_DATE`: Beginning of data download period
- `DATA_END_DATE`: End of data download period
- `TRAIN_END_DATE`: Last date used for training (inclusive)
- `TEST_START_DATE`: First date for backtesting (inclusive)
- `PLOT_START_DATE`: Start date for price charts (shows context before test period)

### Model Parameters
- `N_STATES`: Number of HMM states (2 = BULL/BEAR)
- `WINDOW`: Wavelet window size in days
- `SCALE`: Wavelet scale parameter
- `N_ITER`: Maximum EM iterations for training
- `RANDOM_STATE`: Random seed for reproducibility

### Trading Parameters
- `INITIAL_CAPITAL`: Starting portfolio value
- `MAX_POSITION_PCT`: Maximum % of capital to invest
- `STOP_LOSS_PCT`: Stop loss threshold

### View Current Configuration
```bash
python config.py
```

## Individual Scripts

You can also run each step individually:

```bash
# 1. Download data
python 1_download_data.py

# 2. Train HMM model
python 3_train_hmm.py

# 3. Backtest strategy
python 4_backtest.py

# 4. Generate plots
python 5_visualize.py
```

All scripts automatically use the settings from `config.py`.

## Outputs

- `data/SPY.csv` - Downloaded price data
- `models/hmm_model.pkl` - Trained HMM model
- `results/backtest_results.csv` - Daily backtest results
- `results/backtest_plot.png` - Main performance visualization
- `results/state_stats.png` - HMM state analysis

## Example: Adjusting Date Ranges

### Scenario 1: Different training/test split
```python
# In config.py
DATA_START_DATE = "2010-01-01"
DATA_END_DATE = "2024-12-31"
TRAIN_END_DATE = "2023-12-31"   # Train on 2010-2023
TEST_START_DATE = "2024-01-01"   # Test on 2024
PLOT_START_DATE = "2023-01-01"   # Show 1 year before test
```

### Scenario 2: Longer historical data
```python
# In config.py
DATA_START_DATE = "1993-01-01"   # SPY inception
DATA_END_DATE = "2025-12-31"
TRAIN_END_DATE = "2024-12-31"
TEST_START_DATE = "2025-01-01"
PLOT_START_DATE = "2023-01-01"
```

After editing `config.py`, simply run:
```bash
python run_pipeline.py
```

The pipeline will automatically use your new date settings!
