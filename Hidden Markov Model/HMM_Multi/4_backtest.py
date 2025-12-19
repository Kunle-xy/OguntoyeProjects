"""
Backtest HMM Strategy on 2025 Data
- Regime-aware risk manager (inspired by qstrader)
- Only blocks NEW entries in undesirable regime
- Allows exits to complete gracefully
"""

import numpy as np
import pandas as pd
import pickle
import os
from wavelet_features import extract_wavelet_features
from config import (
    DATA_FILE,
    MODEL_FILE,
    RESULTS_DIR,
    BACKTEST_RESULTS_FILE,
    TEST_START_DATE,
    INITIAL_CAPITAL,
    MAX_POSITION_PCT,
    STOP_LOSS_PCT
)


class RegimeHMMRiskManager:
    """
    Regime-aware risk manager using HMM predictions.
    
    Logic:
    - Regime 0 (BULL/desirable): Allow buys and sells normally
    - Regime 1 (BEAR/undesirable): Block new buys, allow exits only
    
    This prevents whipsawing by not forcing immediate exits,
    but stops new entries in bad regimes.
    """
    
    def __init__(self, initial_capital: float = INITIAL_CAPITAL,
                 max_position_pct: float = MAX_POSITION_PCT,
                 stop_loss_pct: float = STOP_LOSS_PCT):
        
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.max_position_pct = max_position_pct
        self.stop_loss_pct = stop_loss_pct
        
        self.position = 0  # Number of shares
        self.entry_price = 0.0
        self.invested = False  # Track if we have open position
        
    def check_stop_loss(self, current_price: float) -> bool:
        """Check if stop loss is triggered."""
        if self.invested and self.entry_price > 0:
            loss_pct = (self.entry_price - current_price) / self.entry_price
            if loss_pct >= self.stop_loss_pct:
                return True
        return False
    
    def refine_order(self, regime: int, signal: str, price: float) -> str:
        """
        Decide whether to execute order based on regime.
        
        Args:
            regime: 0 = desirable (BULL), 1 = undesirable (BEAR)
            signal: 'BUY' or 'SELL' from strategy
            price: Current price
        
        Returns:
            'BUY', 'SELL', or 'HOLD' (blocked)
        """
        
        # Regime 0: Desirable (BULL) - allow normal trading
        if regime == 0:
            if signal == 'BUY':
                if not self.invested:
                    return 'BUY'
                else:
                    return 'HOLD'  # Already invested
            elif signal == 'SELL':
                if self.invested:
                    return 'SELL'
                else:
                    return 'HOLD'  # Nothing to sell
        
        # Regime 1: Undesirable (BEAR) - block buys, allow exits
        elif regime == 1:
            if signal == 'BUY':
                return 'HOLD'  # Block new entries in bad regime
            elif signal == 'SELL':
                if self.invested:
                    return 'SELL'  # Allow graceful exit
                else:
                    return 'HOLD'
        
        return 'HOLD'
    
    def execute_order(self, action: str, price: float) -> dict:
        """
        Execute the refined order.
        
        Returns:
            dict with execution details
        """
        result = {
            'action': action,
            'shares': 0,
            'cost': 0.0,
            'proceeds': 0.0
        }
        
        if action == 'BUY' and not self.invested:
            # Calculate shares to buy
            invest_amount = self.capital * self.max_position_pct
            shares = int(invest_amount / price)
            cost = shares * price
            
            if shares > 0:
                self.capital -= cost
                self.position = shares
                self.entry_price = price
                self.invested = True
                
                result['shares'] = shares
                result['cost'] = cost
        
        elif action == 'SELL' and self.invested:
            # Sell all shares
            proceeds = self.position * price
            
            result['shares'] = self.position
            result['proceeds'] = proceeds
            
            self.capital += proceeds
            self.position = 0
            self.entry_price = 0.0
            self.invested = False
        
        return result
    
    def get_total_value(self, price: float) -> float:
        """Get total portfolio value."""
        return self.capital + self.position * price


class HMMStrategy:
    """HMM-based trading strategy."""
    
    def __init__(self, model_path: str):
        """Load trained model."""
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.obs_mean = model_data['obs_mean']
        self.obs_std = model_data['obs_std']
        self.state_labels = model_data['state_labels']
        self.config = model_data['config']
        
        # Determine which state is BULL (higher mean return)
        means = self.model.means_
        n_states = len(means)
        self.bull_state = np.argmax([means[i][0] for i in range(n_states)])
        self.bear_state = np.argmin([means[i][0] for i in range(n_states)])
        
        print(f"Strategy loaded:")
        print(f"  Bull state (regime 0): {self.bull_state}")
        print(f"  Bear state (regime 1): {self.bear_state}")
    
    def predict_state(self, observations: np.ndarray) -> int:
        """
        Predict current state given observation history.
        
        Returns:
            Predicted current state
        """
        # Normalize
        obs_norm = (observations - self.obs_mean) / self.obs_std
        
        # Predict states for entire sequence, return last state
        states = self.model.predict(obs_norm)
        return states[-1]
    
    def get_regime(self, current_state: int) -> int:
        """
        Convert HMM state to regime.
        
        Returns:
            0 = desirable (BULL), 1 = undesirable (BEAR)
        """
        if current_state == self.bull_state:
            return 0  # Desirable
        else:
            return 1  # Undesirable
    
    def get_signal(self, regime: int, is_invested: bool) -> str:
        """
        Generate raw signal based on regime.
        
        Returns:
            'BUY' or 'SELL'
        """
        if regime == 0:  # BULL
            return 'BUY'
        else:  # BEAR
            return 'SELL'


def run_backtest(data_path: str = DATA_FILE,
                 model_path: str = MODEL_FILE,
                 test_start: str = TEST_START_DATE):
    """
    Run backtest with regime-aware risk manager.
    """
    # Load data
    df = pd.read_csv(data_path, index_col="Date", parse_dates=True)

    # Get config from model
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    config = model_data['config']
    window = config['window']
    scale = config['scale']

    # Initialize
    strategy = HMMStrategy(model_path)
    risk_mgr = RegimeHMMRiskManager()  # Uses config defaults
    
    # Get test period data (need lookback for wavelet)
    test_df = df[df.index >= test_start].copy()
    
    # Need prior data for wavelet calculation
    lookback_start = df.index.get_loc(test_df.index[0]) - window
    full_df = df.iloc[lookback_start:].copy()
    
    print(f"\nBacktest period: {test_df.index[0].date()} to {test_df.index[-1].date()}")
    print(f"Test days: {len(test_df)}")
    
    # Compute wavelet features for full period
    returns = full_df['return'].values
    energies = extract_wavelet_features(returns, window=window, scale=scale)
    full_df['energy'] = energies
    
    # Results storage
    results = []
    
    # Track order flow for debugging
    orders_blocked = 0
    orders_executed = 0
    
    # Run day by day through test period
    for i, (date, row) in enumerate(test_df.iterrows()):
        # Get observations up to today
        obs_end_idx = full_df.index.get_loc(date) + 1
        obs_df = full_df.iloc[:obs_end_idx]
        
        # Skip if not enough data
        valid_obs = obs_df[['return', 'energy']].dropna()
        if len(valid_obs) < window:
            continue
        
        observations = valid_obs[['return', 'energy']].values
        
        # Predict current state and regime
        current_state = strategy.predict_state(observations)
        regime = strategy.get_regime(current_state)
        
        # Get current price
        price = row['Adj Close']
        
        # Check stop loss first
        stop_triggered = risk_mgr.check_stop_loss(price)
        
        # Get raw signal from strategy
        raw_signal = strategy.get_signal(regime, risk_mgr.invested)
        
        # Override signal if stop loss triggered
        if stop_triggered:
            raw_signal = 'SELL'
            regime = 1  # Treat as undesirable to allow exit
        
        # Refine order through risk manager
        action = risk_mgr.refine_order(regime, raw_signal, price)
        
        # Execute order
        execution = risk_mgr.execute_order(action, price)
        
        # Track order stats
        if action == 'HOLD' and raw_signal in ['BUY', 'SELL']:
            orders_blocked += 1
        elif action in ['BUY', 'SELL']:
            orders_executed += 1
        
        # Record results
        total_value = risk_mgr.get_total_value(price)
        daily_return = row['return'] if not np.isnan(row['return']) else 0.0
        
        results.append({
            'date': date,
            'price': price,
            'return': daily_return,
            'energy': observations[-1, 1] if len(observations) > 0 else np.nan,
            'state': current_state,
            'regime': regime,
            'raw_signal': raw_signal,
            'action': action,
            'invested': risk_mgr.invested,
            'position': risk_mgr.position,
            'cash': risk_mgr.capital,
            'total_value': total_value,
            'stop_triggered': stop_triggered
        })
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    results_df.set_index('date', inplace=True)
    
    print(f"\nOrder Statistics:")
    print(f"  Orders executed: {orders_executed}")
    print(f"  Orders blocked:  {orders_blocked}")
    
    # Calculate metrics
    metrics = calculate_metrics(results_df, risk_mgr.initial_capital)
    
    return results_df, metrics


def calculate_metrics(results_df: pd.DataFrame, initial_capital: float) -> dict:
    """Calculate performance metrics."""
    
    final_value = results_df['total_value'].iloc[-1]
    total_return = (final_value - initial_capital) / initial_capital
    
    # Daily returns of strategy
    results_df['strategy_return'] = results_df['total_value'].pct_change()
    
    # Buy and hold comparison
    first_price = results_df['price'].iloc[0]
    last_price = results_df['price'].iloc[-1]
    buy_hold_return = (last_price - first_price) / first_price
    
    # Sharpe ratio (annualized)
    daily_returns = results_df['strategy_return'].dropna()
    sharpe = np.sqrt(252) * daily_returns.mean() / daily_returns.std() if daily_returns.std() > 0 else 0
    
    # Max drawdown
    cumulative = (1 + daily_returns).cumprod()
    rolling_max = cumulative.expanding().max()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    
    # Win rate
    winning_days = (daily_returns > 0).sum()
    total_days = len(daily_returns)
    win_rate = winning_days / total_days if total_days > 0 else 0
    
    # Trading stats
    buys = (results_df['action'] == 'BUY').sum()
    sells = (results_df['action'] == 'SELL').sum()
    holds = (results_df['action'] == 'HOLD').sum()
    
    # Time invested
    invested_days = results_df['invested'].sum()
    total_days = len(results_df)
    time_invested_pct = invested_days / total_days * 100
    
    # Regime distribution
    regime_dist = results_df['regime'].value_counts(normalize=True).to_dict()
    
    metrics = {
        'initial_capital': initial_capital,
        'final_value': final_value,
        'total_return': total_return,
        'total_return_pct': total_return * 100,
        'buy_hold_return': buy_hold_return,
        'buy_hold_return_pct': buy_hold_return * 100,
        'excess_return': total_return - buy_hold_return,
        'excess_return_pct': (total_return - buy_hold_return) * 100,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_drawdown,
        'max_drawdown_pct': max_drawdown * 100,
        'win_rate': win_rate,
        'win_rate_pct': win_rate * 100,
        'num_buys': buys,
        'num_sells': sells,
        'num_holds': holds,
        'time_invested_pct': time_invested_pct,
        'regime_distribution': regime_dist
    }
    
    return metrics


def print_report(results_df: pd.DataFrame, metrics: dict):
    """Print backtest report."""
    
    print("\n" + "="*70)
    print("BACKTEST REPORT (Regime-Aware Risk Manager)")
    print("="*70)
    
    print(f"\nPeriod: {results_df.index[0].date()} to {results_df.index[-1].date()}")
    print(f"Trading Days: {len(results_df)}")
    
    print("\n--- PERFORMANCE ---")
    print(f"Initial Capital:     ${metrics['initial_capital']:,.2f}")
    print(f"Final Value:         ${metrics['final_value']:,.2f}")
    print(f"Strategy Return:     {metrics['total_return_pct']:+.2f}%")
    print(f"Buy & Hold Return:   {metrics['buy_hold_return_pct']:+.2f}%")
    print(f"Excess Return:       {metrics['excess_return_pct']:+.2f}%")
    
    print("\n--- RISK METRICS ---")
    print(f"Sharpe Ratio:        {metrics['sharpe_ratio']:.3f}")
    print(f"Max Drawdown:        {metrics['max_drawdown_pct']:.2f}%")
    print(f"Win Rate:            {metrics['win_rate_pct']:.1f}%")
    
    print("\n--- TRADING ACTIVITY ---")
    print(f"Buy Orders:          {metrics['num_buys']}")
    print(f"Sell Orders:         {metrics['num_sells']}")
    print(f"Hold (blocked/none): {metrics['num_holds']}")
    print(f"Time Invested:       {metrics['time_invested_pct']:.1f}%")
    
    print("\n--- REGIME DISTRIBUTION ---")
    for regime, pct in metrics['regime_distribution'].items():
        label = 'BULL (desirable)' if regime == 0 else 'BEAR (undesirable)'
        print(f"  Regime {regime} ({label}): {pct*100:.1f}%")
    
    print("\n--- SAMPLE TRADES (first 15 BUY/SELL) ---")
    trades = results_df[results_df['action'].isin(['BUY', 'SELL'])].head(15)
    for date, row in trades.iterrows():
        regime_label = 'BULL' if row['regime'] == 0 else 'BEAR'
        print(f"  {date.date()}: {row['action']:4s} @ ${row['price']:.2f} | "
              f"Regime={regime_label} | Value=${row['total_value']:,.2f}")


def main():
    # Configuration from config.py
    print("Running HMM Strategy Backtest (Regime-Aware Risk Manager)...")

    results_df, metrics = run_backtest()  # Uses config defaults

    print_report(results_df, metrics)

    # Save results
    os.makedirs(RESULTS_DIR, exist_ok=True)
    results_df.to_csv(BACKTEST_RESULTS_FILE)
    print(f"\nResults saved to: {BACKTEST_RESULTS_FILE}")


if __name__ == "__main__":
    main()
