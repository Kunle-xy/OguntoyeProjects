"""
Wavelet Feature Extraction using Complex Morlet CWT
- Right-edge rolling window (no lookahead)
- Energy = |W_t|^2 (modulus squared)
"""

import numpy as np
import pywt

def compute_wavelet_energy(returns: np.ndarray, scale: float = 10.0, wavelet: str = 'cmor1.5-1.0') -> float:
    """
    Compute wavelet energy for the last point in the returns array.
    
    Args:
        returns: Array of returns (the window chunk)
        scale: Wavelet scale (controls frequency sensitivity)
        wavelet: Wavelet name (complex morlet)
    
    Returns:
        Energy at the right edge (last point)
    """
    # CWT with complex morlet
    coeffs, _ = pywt.cwt(returns, [scale], wavelet)
    
    # Get the last coefficient (right-edge, no lookahead)
    W_t = coeffs[0, -1]
    
    # Energy = |W_t|^2
    energy = np.abs(W_t) ** 2
    
    return energy


def extract_wavelet_features(returns: np.ndarray, window: int = 60, scale: float = 10.0) -> np.ndarray:
    """
    Extract wavelet energy features for entire return series.
    Uses rolling right-edge method to avoid lookahead bias.
    
    Args:
        returns: Full array of daily returns
        window: Lookback window size
        scale: Wavelet scale
    
    Returns:
        Array of wavelet energies (NaN for first window-1 points)
    """
    n = len(returns)
    energies = np.full(n, np.nan)
    
    for t in range(window - 1, n):
        # Grab past data only: [t - window + 1, t] inclusive
        chunk = returns[t - window + 1 : t + 1]
        
        # Skip if any NaN in chunk
        if np.any(np.isnan(chunk)):
            continue
        
        energies[t] = compute_wavelet_energy(chunk, scale=scale)
    
    return energies


if __name__ == "__main__":
    # Quick test
    np.random.seed(42)
    fake_returns = np.random.randn(100) * 0.02
    
    energies = extract_wavelet_features(fake_returns, window=20, scale=10.0)
    
    print("Test wavelet extraction:")
    print(f"  Returns shape: {fake_returns.shape}")
    print(f"  Energies shape: {energies.shape}")
    print(f"  Non-NaN energies: {np.sum(~np.isnan(energies))}")
    print(f"  Energy range: [{np.nanmin(energies):.6f}, {np.nanmax(energies):.6f}]")
