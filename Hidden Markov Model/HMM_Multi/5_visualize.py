"""
Visualization of HMM Backtest Results
- Equity curve comparison (Strategy vs Buy & Hold)
- State regimes overlay on price
- Drawdown chart
- Monthly returns heatmap
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
import pickle
import os
from config import (
    DATA_FILE,
    MODEL_FILE,
    BACKTEST_RESULTS_FILE,
    BACKTEST_PLOT_FILE,
    STATE_STATS_PLOT_FILE,
    PLOT_START_DATE,
    TEST_START_DATE
)

# Style settings
plt.style.use('seaborn-v0_8-whitegrid')
COLORS = {
    'bull': '#2ecc71',      # Green
    'bear': '#e74c3c',      # Red
    'strategy': '#3498db',  # Blue
    'buyhold': '#95a5a6',   # Gray
    'price': '#2c3e50',     # Dark blue
    'drawdown': '#e74c3c'   # Red
}


def load_data(data_path: str = DATA_FILE,
              results_path: str = BACKTEST_RESULTS_FILE,
              model_path: str = MODEL_FILE,
              plot_start: str = PLOT_START_DATE) -> tuple:
    """Load all required data for plotting."""
    
    # Load price data
    df = pd.read_csv(data_path, index_col="Date", parse_dates=True)
    df = df[df.index >= plot_start]
    
    # Load backtest results
    results = pd.read_csv(results_path, index_col="date", parse_dates=True)
    
    # Load model config
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    
    config = model_data['config']
    state_labels = model_data['state_labels']
    
    # Determine bull state
    model = model_data['model']
    bull_state = np.argmax([model.means_[i][0] for i in range(config['n_states'])])
    
    return df, results, config, state_labels, bull_state


def plot_results(data_path: str = DATA_FILE,
                 results_path: str = BACKTEST_RESULTS_FILE,
                 model_path: str = MODEL_FILE,
                 plot_start: str = PLOT_START_DATE,
                 test_start: str = TEST_START_DATE,
                 output_path: str = BACKTEST_PLOT_FILE):
    """
    Generate comprehensive backtest visualization.
    """
    
    # Load data
    df, results, config, state_labels, bull_state = load_data(
        data_path, results_path, model_path, plot_start
    )
    
    # Create figure with subplots
    fig = plt.figure(figsize=(14, 12))
    
    # Layout: 4 rows
    ax1 = plt.subplot2grid((4, 1), (0, 0), rowspan=2)  # Price + States
    ax2 = plt.subplot2grid((4, 1), (2, 0))              # Equity curve
    ax3 = plt.subplot2grid((4, 1), (3, 0))              # Drawdown
    
    # =========================================
    # PLOT 1: Price with State Regimes
    # =========================================
    
    # Plot price
    ax1.plot(df.index, df['Adj Close'], color=COLORS['price'], 
             linewidth=1.5, label='SPY Price', zorder=3)
    
    # Shade states (only for test period where we have predictions)
    test_mask = results.index >= test_start
    test_results = results[test_mask]
    
    # Find state change points
    state_changes = test_results['state'].diff().fillna(1) != 0
    change_dates = test_results.index[state_changes].tolist()
    change_dates.append(test_results.index[-1])  # Add end date
    
    for i in range(len(change_dates) - 1):
        start = change_dates[i]
        end = change_dates[i + 1]
        state = test_results.loc[start, 'state']
        
        color = COLORS['bull'] if state == bull_state else COLORS['bear']
        ax1.axvspan(start, end, alpha=0.2, color=color, zorder=1)
    
    # Add vertical line at test start
    ax1.axvline(x=pd.Timestamp(test_start), color='black', linestyle='--', 
                linewidth=1.5, label='Test Start (2025)', zorder=4)
    
    # Formatting
    ax1.set_ylabel('Price ($)', fontsize=11)
    ax1.set_title(
        f'SPY Price with HMM Regime Detection\n'
        f'Model: {config["n_states"]}-State Gaussian HMM | '
        f'Window: {config["window"]} days | '
        f'Wavelet Scale: {config["scale"]}',
        fontsize=13, fontweight='bold'
    )
    
    # Legend
    legend_elements = [
        plt.Line2D([0], [0], color=COLORS['price'], linewidth=2, label='SPY Price'),
        Patch(facecolor=COLORS['bull'], alpha=0.3, label=f'State {bull_state}: BULL'),
        Patch(facecolor=COLORS['bear'], alpha=0.3, label=f'State {1-bull_state}: BEAR'),
        plt.Line2D([0], [0], color='black', linestyle='--', linewidth=1.5, label='Test Start')
    ]
    ax1.legend(handles=legend_elements, loc='upper left', fontsize=9)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax1.tick_params(axis='x', rotation=0)
    
    # =========================================
    # PLOT 2: Equity Curve Comparison
    # =========================================
    
    # Strategy equity
    strategy_equity = test_results['total_value']
    initial_capital = strategy_equity.iloc[0]
    
    # Buy & Hold equity (normalized to same starting capital)
    first_price = test_results['price'].iloc[0]
    buyhold_equity = initial_capital * (test_results['price'] / first_price)
    
    ax2.plot(test_results.index, strategy_equity, color=COLORS['strategy'], 
             linewidth=2, label='HMM Strategy')
    ax2.plot(test_results.index, buyhold_equity, color=COLORS['buyhold'], 
             linewidth=2, linestyle='--', label='Buy & Hold')
    
    # Calculate returns for annotation
    strat_return = (strategy_equity.iloc[-1] / initial_capital - 1) * 100
    bh_return = (buyhold_equity.iloc[-1] / initial_capital - 1) * 100
    excess = strat_return - bh_return
    
    # Annotation box
    textstr = (f'Strategy: {strat_return:+.2f}%\n'
               f'Buy & Hold: {bh_return:+.2f}%\n'
               f'Excess: {excess:+.2f}%')
    props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray')
    ax2.text(0.02, 0.97, textstr, transform=ax2.transAxes, fontsize=10,
             verticalalignment='top', bbox=props)
    
    ax2.set_ylabel('Portfolio Value ($)', fontsize=11)
    ax2.set_title('Equity Curve: Strategy vs Buy & Hold (2025)', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # =========================================
    # PLOT 3: Drawdown
    # =========================================
    
    # Calculate drawdown
    cumulative = strategy_equity / initial_capital
    rolling_max = cumulative.expanding().max()
    drawdown = (cumulative - rolling_max) / rolling_max * 100
    
    ax3.fill_between(test_results.index, drawdown, 0, 
                     color=COLORS['drawdown'], alpha=0.4)
    ax3.plot(test_results.index, drawdown, color=COLORS['drawdown'], linewidth=1)
    
    # Max drawdown annotation
    max_dd = drawdown.min()
    max_dd_date = drawdown.idxmin()
    ax3.annotate(f'Max DD: {max_dd:.2f}%', 
                 xy=(max_dd_date, max_dd),
                 xytext=(max_dd_date + pd.Timedelta(days=10), max_dd - 2),
                 fontsize=9, color=COLORS['drawdown'],
                 arrowprops=dict(arrowstyle='->', color=COLORS['drawdown']))
    
    ax3.set_ylabel('Drawdown (%)', fontsize=11)
    ax3.set_xlabel('Date', fontsize=11)
    ax3.set_title('Strategy Drawdown', fontsize=12, fontweight='bold')
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax3.set_ylim(min(max_dd * 1.3, -1), 1)
    
    # =========================================
    # Final adjustments
    # =========================================
    
    plt.tight_layout()
    
    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"\nPlot saved to: {output_path}")
    
    plt.show()
    
    return fig


def plot_state_statistics(results_path: str = BACKTEST_RESULTS_FILE,
                          model_path: str = MODEL_FILE,
                          output_path: str = STATE_STATS_PLOT_FILE):
    """
    Plot state-specific return distributions and transition stats.
    """
    
    # Load data
    results = pd.read_csv(results_path, index_col="date", parse_dates=True)
    
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    
    model = model_data['model']
    config = model_data['config']
    n_states = config['n_states']
    bull_state = np.argmax([model.means_[i][0] for i in range(n_states)])
    
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    
    # =========================================
    # PLOT 1: Return distribution by state
    # =========================================
    
    ax1 = axes[0]
    for state in range(n_states):
        state_returns = results[results['state'] == state]['return'] * 100
        label = 'BULL' if state == bull_state else 'BEAR'
        color = COLORS['bull'] if state == bull_state else COLORS['bear']
        ax1.hist(state_returns, bins=30, alpha=0.6, label=f'{label} (n={len(state_returns)})',
                 color=color, edgecolor='white')
    
    ax1.axvline(x=0, color='black', linestyle='--', linewidth=1)
    ax1.set_xlabel('Daily Return (%)', fontsize=10)
    ax1.set_ylabel('Frequency', fontsize=10)
    ax1.set_title('Return Distribution by State', fontsize=11, fontweight='bold')
    ax1.legend(fontsize=9)
    
    # =========================================
    # PLOT 2: State duration
    # =========================================
    
    ax2 = axes[1]
    
    # Calculate state durations
    state_changes = results['state'].diff().fillna(1) != 0
    state_runs = []
    current_state = results['state'].iloc[0]
    current_length = 0
    
    for i, (idx, row) in enumerate(results.iterrows()):
        if state_changes.iloc[i] and i > 0:
            state_runs.append({'state': current_state, 'duration': current_length})
            current_state = row['state']
            current_length = 1
        else:
            current_length += 1
    state_runs.append({'state': current_state, 'duration': current_length})
    
    runs_df = pd.DataFrame(state_runs)
    
    for state in range(n_states):
        durations = runs_df[runs_df['state'] == state]['duration']
        label = 'BULL' if state == bull_state else 'BEAR'
        color = COLORS['bull'] if state == bull_state else COLORS['bear']
        ax2.hist(durations, bins=15, alpha=0.6, label=f'{label} (avg={durations.mean():.1f}d)',
                 color=color, edgecolor='white')
    
    ax2.set_xlabel('Regime Duration (days)', fontsize=10)
    ax2.set_ylabel('Frequency', fontsize=10)
    ax2.set_title('Regime Duration Distribution', fontsize=11, fontweight='bold')
    ax2.legend(fontsize=9)
    
    # =========================================
    # PLOT 3: Transition matrix heatmap
    # =========================================
    
    ax3 = axes[2]
    
    trans_matrix = model.transmat_
    labels = ['BULL' if i == bull_state else 'BEAR' for i in range(n_states)]
    
    im = ax3.imshow(trans_matrix, cmap='Blues', vmin=0, vmax=1)
    
    # Add text annotations
    for i in range(n_states):
        for j in range(n_states):
            text = ax3.text(j, i, f'{trans_matrix[i, j]:.2f}',
                           ha='center', va='center', fontsize=12,
                           color='white' if trans_matrix[i, j] > 0.5 else 'black')
    
    ax3.set_xticks(range(n_states))
    ax3.set_yticks(range(n_states))
    ax3.set_xticklabels(labels)
    ax3.set_yticklabels(labels)
    ax3.set_xlabel('To State', fontsize=10)
    ax3.set_ylabel('From State', fontsize=10)
    ax3.set_title('Transition Probabilities', fontsize=11, fontweight='bold')
    
    plt.colorbar(im, ax=ax3, shrink=0.8)
    
    # =========================================
    # Final adjustments
    # =========================================
    
    plt.suptitle(
        f'HMM State Analysis | Window: {config["window"]}d | Scale: {config["scale"]}',
        fontsize=13, fontweight='bold', y=1.02
    )
    
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"\nState statistics plot saved to: {output_path}")
    
    plt.show()
    
    return fig


def main():
    print("Generating backtest visualizations...")

    # Main results plot (uses config defaults)
    plot_results()

    # State statistics plot (uses config defaults)
    plot_state_statistics()

    print("\nAll plots generated!")


if __name__ == "__main__":
    main()
