"""
Multivariate Gaussian HMM Training
- Observations: [adjusted_return, wavelet_energy]
- Train on data up to end of 2024
"""

import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
import pickle
import os
from wavelet_features import extract_wavelet_features
from config import (
    DATA_FILE,
    MODEL_FILE,
    MODEL_DIR,
    TRAIN_END_DATE,
    N_STATES,
    WINDOW,
    SCALE,
    N_ITER,
    RANDOM_STATE
)

# Rename the import to avoid confusion
from wavelet_features import extract_wavelet_features as compute_wavelet_features


def prepare_observations(df: pd.DataFrame, window: int = 60, scale: float = 10.0) -> tuple:
    """
    Prepare observation matrix [return, wavelet_energy] for HMM.
    
    Returns:
        observations: (N, 2) array
        valid_index: DatetimeIndex of valid observations
    """
    returns = df['return'].values
    
    # Extract wavelet energies
    energies = compute_wavelet_features(returns, window=window, scale=scale)
    
    # Combine into observation matrix
    obs = np.column_stack([returns, energies])
    
    # Find valid rows (no NaN)
    valid_mask = ~np.isnan(obs).any(axis=1)
    
    valid_obs = obs[valid_mask]
    valid_index = df.index[valid_mask]
    
    return valid_obs, valid_index


def train_hmm(observations: np.ndarray, n_states: int = N_STATES, n_iter: int = N_ITER,
              random_state: int = RANDOM_STATE) -> GaussianHMM:
    """
    Train a Gaussian HMM on the observations.
    
    Args:
        observations: (N, 2) array of [return, energy]
        n_states: Number of hidden states
        n_iter: Max EM iterations
        random_state: For reproducibility
    
    Returns:
        Trained GaussianHMM model
    """
    model = GaussianHMM(
        n_components=n_states,
        covariance_type="full",  # Full covariance to capture return-energy correlation
        n_iter=n_iter,
        random_state=random_state,
        verbose=True
    )
    
    model.fit(observations)
    
    return model


def analyze_states(model: GaussianHMM, n_states: int):
    """Print state characteristics for interpretation."""
    print("\n" + "="*60)
    print("STATE ANALYSIS")
    print("="*60)
    
    for i in range(n_states):
        mean_ret, mean_energy = model.means_[i]
        print(f"\nState {i}:")
        print(f"  Mean Return:  {mean_ret*100:+.4f}% daily")
        print(f"  Mean Energy:  {mean_energy:.6f}")
        print(f"  Covariance:\n{model.covars_[i]}")
    
    print("\nTransition Matrix:")
    print(model.transmat_)
    
    # Label states by return
    state_labels = {}
    mean_returns = [model.means_[i][0] for i in range(n_states)]
    sorted_states = np.argsort(mean_returns)
    
    if n_states == 2:
        state_labels[sorted_states[0]] = "BEAR (low return)"
        state_labels[sorted_states[1]] = "BULL (high return)"
    elif n_states == 3:
        state_labels[sorted_states[0]] = "BEAR"
        state_labels[sorted_states[1]] = "SIDEWAYS"
        state_labels[sorted_states[2]] = "BULL"
    
    print("\nState Labels (by mean return):")
    for state, label in state_labels.items():
        print(f"  State {state}: {label}")
    
    return state_labels


def main():
    # Configuration from config.py
    DATA_PATH = DATA_FILE
    MODEL_PATH = MODEL_FILE
    TRAIN_END = TRAIN_END_DATE

    # Create models directory
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Load data
    print("Loading data...")
    df = pd.read_csv(DATA_PATH, index_col="Date", parse_dates=True)
    
    # Split train/test
    train_df = df[df.index <= TRAIN_END]
    print(f"Training period: {train_df.index[0].date()} to {train_df.index[-1].date()}")
    print(f"Training samples: {len(train_df)}")
    
    # Prepare observations
    print("\nPreparing observations...")
    train_obs, train_index = prepare_observations(train_df, window=WINDOW, scale=SCALE)
    print(f"Valid observations: {len(train_obs)}")
    
    # Normalize observations for better HMM convergence
    obs_mean = train_obs.mean(axis=0)
    obs_std = train_obs.std(axis=0)
    train_obs_normalized = (train_obs - obs_mean) / obs_std
    
    # Train HMM
    print("\nTraining HMM...")
    model = train_hmm(train_obs_normalized, n_states=N_STATES)
    
    # Analyze states
    state_labels = analyze_states(model, N_STATES)
    
    # Save model and normalization params
    model_data = {
        'model': model,
        'obs_mean': obs_mean,
        'obs_std': obs_std,
        'state_labels': state_labels,
        'config': {
            'n_states': N_STATES,
            'window': WINDOW,
            'scale': SCALE,
            'train_end': TRAIN_END
        }
    }
    
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\nModel saved to: {MODEL_PATH}")
    
    # Quick validation: decode training states
    train_states = model.predict(train_obs_normalized)
    print(f"\nTraining state distribution:")
    for i in range(N_STATES):
        count = np.sum(train_states == i)
        pct = count / len(train_states) * 100
        print(f"  State {i}: {count} days ({pct:.1f}%)")


if __name__ == "__main__":
    main()
