# HMM Multivariate Trading Strategy

A Hidden Markov Model (HMM) trading strategy using multivariate observations (returns + wavelet energy) for market regime detection and systematic trading.

---

## Table of Contents

1. [Introduction to Hidden Markov Models](#1-introduction-to-hidden-markov-models)
2. [SPY Data and Feature Engineering](#2-spy-data-and-feature-engineering)
3. [Wavelet Transform for Feature Extraction](#3-wavelet-transform-for-feature-extraction)
4. [State-Observation Diagram](#4-state-observation-diagram)
5. [Trading Strategy and Data Splitting](#5-trading-strategy-and-data-splitting)
6. [Quick Start Guide](#6-quick-start-guide)
7. [Configuration Reference](#7-configuration-reference)

---

## 1. Introduction to Hidden Markov Models

### 1.1 Problem Statement

Financial markets exhibit **regime-switching behavior**—alternating between distinct phases such as bull markets (upward trends with low volatility) and bear markets (downward trends with high volatility). The challenge is that:

1. **Regimes are not directly observable** — we cannot "see" whether the market is in a bull or bear state
2. **Only price/return data is observable** — we must infer the hidden regime from market observations
3. **Regimes are persistent** — markets tend to stay in a regime before transitioning

**Hidden Markov Models (HMMs)** provide an elegant probabilistic framework to solve this problem by modeling the relationship between hidden states (regimes) and observable data (returns, volatility).

### 1.2 Key Characteristics of HMMs

An HMM is a **doubly stochastic process** with two layers:

| Layer | Description | Financial Interpretation |
|-------|-------------|-------------------------|
| **Hidden Layer** | Markov chain of unobservable states | Market regimes (BULL/BEAR) |
| **Observable Layer** | Emissions from each state | Daily returns, volatility, wavelet energy |

**Core Assumptions:**
- **Markov Property**: The probability of transitioning to the next state depends *only* on the current state, not on the history
- **Conditional Independence**: Given the hidden state, the observation is independent of all other observations and states
- **Stationarity**: Transition and emission probabilities remain constant over time

### 1.3 Mathematical Formulation

An HMM is defined by the tuple $\lambda = (A, B, \pi)$ where:

#### State Space
Let $S = \{s_1, s_2, \ldots, s_N\}$ be the set of $N$ hidden states. In our case:
- $N = 2$ (BULL and BEAR regimes)
- $q_t \in S$ denotes the hidden state at time $t$

#### Transition Probability Matrix $A$

The **transition matrix** $A$ defines the probability of moving from state $i$ to state $j$:

$$A = [a_{ij}] \quad \text{where} \quad a_{ij} = P(q_{t+1} = s_j \mid q_t = s_i)$$

**Properties:**
- $a_{ij} \geq 0$ for all $i, j$
- $\sum_{j=1}^{N} a_{ij} = 1$ for all $i$ (rows sum to 1)

For a 2-state model:

$$A = \begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix} = \begin{bmatrix} P(\text{BULL} \to \text{BULL}) & P(\text{BULL} \to \text{BEAR}) \\ P(\text{BEAR} \to \text{BULL}) & P(\text{BEAR} \to \text{BEAR}) \end{bmatrix}$$

#### Emission (Observation) Probability $B$

For continuous observations (Gaussian HMM), each state $i$ emits observations from a multivariate Gaussian distribution:

$$b_i(\mathbf{o}_t) = P(\mathbf{o}_t \mid q_t = s_i) = \mathcal{N}(\mathbf{o}_t; \boldsymbol{\mu}_i, \boldsymbol{\Sigma}_i)$$

$$b_i(\mathbf{o}_t) = \frac{1}{(2\pi)^{d/2} |\boldsymbol{\Sigma}_i|^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{o}_t - \boldsymbol{\mu}_i)^\top \boldsymbol{\Sigma}_i^{-1}(\mathbf{o}_t - \boldsymbol{\mu}_i)\right)$$

Where:
- $\mathbf{o}_t \in \mathbb{R}^d$ is the observation vector at time $t$
- $\boldsymbol{\mu}_i \in \mathbb{R}^d$ is the mean vector for state $i$
- $\boldsymbol{\Sigma}_i \in \mathbb{R}^{d \times d}$ is the covariance matrix for state $i$
- $d = 2$ in our model (return + wavelet energy)

#### Initial State Distribution $\pi$

$$\pi = [\pi_i] \quad \text{where} \quad \pi_i = P(q_1 = s_i)$$

### 1.4 The Three Fundamental Problems of HMMs

| Problem | Name | Question | Algorithm |
|---------|------|----------|-----------|
| **Problem 1** | Evaluation | Given $\lambda$ and observation sequence $O$, what is $P(O \mid \lambda)$? | Forward Algorithm |
| **Problem 2** | Decoding | Given $\lambda$ and $O$, what is the most likely state sequence? | Viterbi Algorithm |
| **Problem 3** | Learning | Given $O$, how to estimate optimal parameters $\lambda^*$? | Baum-Welch (EM) Algorithm |

---

### 1.5 Forward Algorithm (Evaluation)

The **Forward Algorithm** computes the probability of observing sequence $O = (o_1, o_2, \ldots, o_T)$ given model $\lambda$.

#### Forward Variable Definition

$$\alpha_t(i) = P(o_1, o_2, \ldots, o_t, q_t = s_i \mid \lambda)$$

This represents the probability of observing the partial sequence up to time $t$ AND being in state $s_i$ at time $t$.

#### Recursive Computation

**Initialization ($t = 1$):**
$$\alpha_1(i) = \pi_i \cdot b_i(o_1) \quad \text{for } i = 1, \ldots, N$$

**Induction ($t = 2, \ldots, T$):**
$$\alpha_t(j) = \left[\sum_{i=1}^{N} \alpha_{t-1}(i) \cdot a_{ij}\right] \cdot b_j(o_t) \quad \text{for } j = 1, \ldots, N$$

**Termination:**
$$P(O \mid \lambda) = \sum_{i=1}^{N} \alpha_T(i)$$

**Complexity:** $O(N^2 T)$ compared to $O(N^T)$ for brute force enumeration.

---

### 1.6 Backward Algorithm

The **Backward Algorithm** computes the probability of future observations given the current state.

#### Backward Variable Definition

$$\beta_t(i) = P(o_{t+1}, o_{t+2}, \ldots, o_T \mid q_t = s_i, \lambda)$$

#### Recursive Computation

**Initialization ($t = T$):**
$$\beta_T(i) = 1 \quad \text{for } i = 1, \ldots, N$$

**Induction ($t = T-1, \ldots, 1$):**
$$\beta_t(i) = \sum_{j=1}^{N} a_{ij} \cdot b_j(o_{t+1}) \cdot \beta_{t+1}(j)$$

**Application:** Used in Baum-Welch for computing state occupation probabilities:

$$\gamma_t(i) = P(q_t = s_i \mid O, \lambda) = \frac{\alpha_t(i) \cdot \beta_t(i)}{\sum_{j=1}^{N} \alpha_t(j) \cdot \beta_t(j)}$$

---

### 1.7 Viterbi Algorithm (Decoding)

The **Viterbi Algorithm** finds the most likely state sequence $Q^* = (q_1^*, q_2^*, \ldots, q_T^*)$ using dynamic programming.

#### Viterbi Variable Definition

$$\delta_t(i) = \max_{q_1, \ldots, q_{t-1}} P(q_1, \ldots, q_{t-1}, q_t = s_i, o_1, \ldots, o_t \mid \lambda)$$

This is the maximum probability of any path ending in state $s_i$ at time $t$.

#### Recursive Computation

**Initialization ($t = 1$):**
$$\delta_1(i) = \pi_i \cdot b_i(o_1)$$
$$\psi_1(i) = 0$$

**Induction ($t = 2, \ldots, T$):**
$$\delta_t(j) = \max_{1 \leq i \leq N} [\delta_{t-1}(i) \cdot a_{ij}] \cdot b_j(o_t)$$
$$\psi_t(j) = \arg\max_{1 \leq i \leq N} [\delta_{t-1}(i) \cdot a_{ij}]$$

**Termination:**
$$P^* = \max_{1 \leq i \leq N} \delta_T(i)$$
$$q_T^* = \arg\max_{1 \leq i \leq N} \delta_T(i)$$

**Backtracking ($t = T-1, \ldots, 1$):**
$$q_t^* = \psi_{t+1}(q_{t+1}^*)$$

---

### 1.8 Baum-Welch Algorithm (Learning)

The **Baum-Welch Algorithm** (a special case of Expectation-Maximization) iteratively estimates HMM parameters from observations.

#### E-Step: Compute Expected Statistics

**State Occupation Probability:**
$$\gamma_t(i) = P(q_t = s_i \mid O, \lambda) = \frac{\alpha_t(i) \cdot \beta_t(i)}{P(O \mid \lambda)}$$

**Transition Probability:**
$$\xi_t(i, j) = P(q_t = s_i, q_{t+1} = s_j \mid O, \lambda) = \frac{\alpha_t(i) \cdot a_{ij} \cdot b_j(o_{t+1}) \cdot \beta_{t+1}(j)}{P(O \mid \lambda)}$$

#### M-Step: Re-estimate Parameters

**Initial State Distribution:**
$$\hat{\pi}_i = \gamma_1(i)$$

**Transition Probabilities:**
$$\hat{a}_{ij} = \frac{\sum_{t=1}^{T-1} \xi_t(i, j)}{\sum_{t=1}^{T-1} \gamma_t(i)}$$

**Emission Parameters (Gaussian):**
$$\hat{\boldsymbol{\mu}}_i = \frac{\sum_{t=1}^{T} \gamma_t(i) \cdot \mathbf{o}_t}{\sum_{t=1}^{T} \gamma_t(i)}$$

$$\hat{\boldsymbol{\Sigma}}_i = \frac{\sum_{t=1}^{T} \gamma_t(i) \cdot (\mathbf{o}_t - \hat{\boldsymbol{\mu}}_i)(\mathbf{o}_t - \hat{\boldsymbol{\mu}}_i)^\top}{\sum_{t=1}^{T} \gamma_t(i)}$$

**Convergence:** Iterate E-step and M-step until $|P(O \mid \lambda^{(n+1)}) - P(O \mid \lambda^{(n)})| < \epsilon$.

---

## 2. SPY Data and Feature Engineering

### 2.1 Why SPY (S&P 500 ETF)?

**SPY** (SPDR S&P 500 ETF Trust) is chosen for several reasons:

| Property | Benefit |
|----------|---------|
| **Liquidity** | Most traded ETF globally (~$30B daily volume) |
| **Diversification** | Represents 500 largest U.S. companies |
| **Long History** | Data available since 1993 |
| **Low Tracking Error** | Closely follows S&P 500 index |
| **Regime Behavior** | Clear bull/bear cycles visible |

### 2.2 Adjusted Close vs. Raw Close

We use **Adjusted Close** rather than raw closing prices:

$$\text{Adjusted Close}_t = \text{Close}_t \times \text{Adjustment Factor}_t$$

**Why Adjusted Close?**

| Event | Raw Close Impact | Adjusted Close |
|-------|-----------------|----------------|
| **Stock Split** | Price drops artificially | Adjusted backward to show true performance |
| **Dividends** | Missing from price return | Included in adjusted return |
| **Spin-offs** | Discontinuity in price | Smoothly adjusted |

### 2.3 Adjusted Return Calculation

The **daily adjusted return** is computed as:

$$r_t = \frac{P_t^{adj} - P_{t-1}^{adj}}{P_{t-1}^{adj}} = \frac{P_t^{adj}}{P_{t-1}^{adj}} - 1$$

Where $P_t^{adj}$ is the adjusted closing price at time $t$.

**Properties of Returns:**
- **Stationarity**: Returns are approximately stationary (unlike prices)
- **Interpretability**: Percentage change is unit-free
- **Additivity**: Log returns are additive over time
- **Normality**: Returns are approximately Gaussian (suitable for Gaussian HMM)

### 2.4 Return Distribution by Regime

| Regime | Mean Daily Return | Volatility | Interpretation |
|--------|------------------|------------|----------------|
| **BULL** | $\mu_{bull} > 0$ | Lower $\sigma$ | Steady upward trend |
| **BEAR** | $\mu_{bear} < 0$ | Higher $\sigma$ | Volatile downward movement |

---

## 3. Wavelet Transform for Feature Extraction

### 3.1 Why Wavelets?

Standard HMMs using only returns suffer from:
1. **Noise Sensitivity**: Daily returns are noisy; small fluctuations trigger false regime changes
2. **Scale Blindness**: Returns don't capture multi-scale market dynamics
3. **Lag**: Moving averages introduce lag

**Wavelet transforms** address these issues by providing:
- **Time-Frequency Localization**: Capture both when and at what frequency patterns occur
- **Multi-Resolution Analysis**: Decompose signal into different time scales
- **Energy Concentration**: Identify periods of high market activity

### 3.2 Continuous Wavelet Transform (CWT)

The **Continuous Wavelet Transform** of a signal $x(t)$ is defined as:

$$W(a, b) = \frac{1}{\sqrt{a}} \int_{-\infty}^{\infty} x(t) \cdot \psi^*\left(\frac{t - b}{a}\right) dt$$

Where:
- $\psi(t)$ is the **mother wavelet** (analyzing function)
- $\psi^*$ denotes the complex conjugate
- $a > 0$ is the **scale parameter** (inversely related to frequency)
- $b$ is the **translation parameter** (time localization)
- $\frac{1}{\sqrt{a}}$ is a normalization factor

### 3.3 Complex Morlet Wavelet

We use the **Complex Morlet wavelet**, defined as:

$$\psi(t) = \frac{1}{\sqrt{\pi f_b}} \exp\left(2\pi i f_c t\right) \exp\left(-\frac{t^2}{f_b}\right)$$

Where:
- $f_c$ is the **center frequency** (controls oscillation)
- $f_b$ is the **bandwidth parameter** (controls envelope width)
- In our implementation: `cmor1.5-1.0` means $f_b = 1.5$, $f_c = 1.0$

**Why Complex Morlet?**
| Property | Benefit |
|----------|---------|
| **Complex-valued** | Provides both amplitude and phase information |
| **Gaussian envelope** | Optimal time-frequency localization (Heisenberg uncertainty) |
| **Oscillatory** | Good frequency resolution for financial cycles |

### 3.4 Wavelet Energy Calculation

The **wavelet energy** at time $t$ quantifies the signal's activity at the chosen scale:

$$E_t = |W_t|^2 = |W(a, t)|^2$$

Where $W_t$ is the complex wavelet coefficient at time $t$ and scale $a$.

**Implementation (Right-Edge Rolling Window):**

```
For each time t from window to T:
    1. Extract return window: chunk = [r_{t-window+1}, ..., r_t]
    2. Apply CWT at scale a: coeffs = CWT(chunk, scale=a)
    3. Take last coefficient: W_t = coeffs[-1]  (right-edge, no lookahead)
    4. Compute energy: E_t = |W_t|^2
```

### 3.5 Key Wavelet Parameters

| Parameter | Symbol | Config Variable | Default | Interpretation |
|-----------|--------|-----------------|---------|----------------|
| **Window Size** | $w$ | `WINDOW` | 5 | Lookback period in days |
| **Scale** | $a$ | `SCALE` | 5 | Frequency sensitivity (higher = lower frequency) |
| **Wavelet** | $\psi$ | — | `cmor1.5-1.0` | Complex Morlet with $f_b=1.5$, $f_c=1.0$ |

**Scale-Frequency Relationship:**

$$f \approx \frac{f_c}{a \cdot \Delta t}$$

Where $\Delta t$ is the sampling period (1 day). Higher scales capture lower-frequency (longer-term) patterns.

### 3.6 Multivariate Observation Vector

Our HMM uses a **2-dimensional observation vector**:

$$\mathbf{o}_t = \begin{bmatrix} r_t \\ E_t \end{bmatrix} = \begin{bmatrix} \text{Adjusted Return} \\ \text{Wavelet Energy} \end{bmatrix}$$

**Normalization** (Z-score) is applied before training:

$$\tilde{\mathbf{o}}_t = \frac{\mathbf{o}_t - \boldsymbol{\mu}_{train}}{\boldsymbol{\sigma}_{train}}$$

---

## 4. State-Observation Diagram

### 4.1 HMM Structure Diagram

```
                    ┌─────────────────────────────────────────────────────────┐
                    │               HIDDEN MARKOV MODEL                       │
                    └─────────────────────────────────────────────────────────┘

    ═══════════════════════════════════════════════════════════════════════════
                              HIDDEN LAYER (Regimes)
    ═══════════════════════════════════════════════════════════════════════════

                              a₁₁ (persist)
                          ┌────────────────┐
                          │                │
                          ▼                │
                    ┌───────────┐    a₁₂    ┌───────────┐
                    │           │ ────────▶ │           │
                    │   BULL    │           │   BEAR    │
                    │  (State 0)│ ◀──────── │  (State 1)│
                    │           │    a₂₁    │           │
                    └───────────┘           └───────────┘
                          │                       │
                          ▲                       ▲
                          │                       │
                          └───────────────────────┘
                                   a₂₂ (persist)

    ═══════════════════════════════════════════════════════════════════════════
                              EMISSION PROBABILITIES
    ═══════════════════════════════════════════════════════════════════════════

              BULL State Emission               BEAR State Emission
              b₁(oₜ) = N(μ₁, Σ₁)                b₂(oₜ) = N(μ₂, Σ₂)

                    │                                 │
                    │                                 │
                    ▼                                 ▼

    ═══════════════════════════════════════════════════════════════════════════
                          OBSERVABLE LAYER (Market Data)
    ═══════════════════════════════════════════════════════════════════════════

         ┌─────────────────────────────────────────────────────────────────┐
         │                                                                 │
         │    Observation Vector:  oₜ = [rₜ, Eₜ]ᵀ                          │
         │                                                                 │
         │    ┌────────────────┐    ┌────────────────┐                     │
         │    │  Adjusted      │    │  Wavelet       │                     │
         │    │  Return (rₜ)   │    │  Energy (Eₜ)   │                     │
         │    └────────────────┘    └────────────────┘                     │
         │           │                     │                               │
         │           └──────────┬──────────┘                               │
         │                      │                                          │
         │                      ▼                                          │
         │            ┌────────────────┐                                   │
         │            │   SPY Price    │                                   │
         │            │   Time Series  │                                   │
         │            └────────────────┘                                   │
         │                                                                 │
         └─────────────────────────────────────────────────────────────────┘

    ═══════════════════════════════════════════════════════════════════════════
                               TIME EVOLUTION
    ═══════════════════════════════════════════════════════════════════════════

         t=1        t=2        t=3        t=4        t=5       ...      t=T
          │          │          │          │          │                  │
          ▼          ▼          ▼          ▼          ▼                  ▼
       ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐          ┌──────┐
       │ q₁   │──▶│ q₂   │──▶│ q₃   │──▶│ q₄   │──▶│ q₅   │── ... ──▶│ qₜ   │
       │(BULL)│   │(BULL)│   │(BEAR)│   │(BEAR)│   │(BULL)│          │ (?)  │
       └──────┘   └──────┘   └──────┘   └──────┘   └──────┘          └──────┘
          │          │          │          │          │                  │
          ▼          ▼          ▼          ▼          ▼                  ▼
       ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐          ┌──────┐
       │ o₁   │   │ o₂   │   │ o₃   │   │ o₄   │   │ o₅   │          │ oₜ   │
       │[r,E] │   │[r,E] │   │[r,E] │   │[r,E] │   │[r,E] │          │[r,E] │
       └──────┘   └──────┘   └──────┘   └──────┘   └──────┘          └──────┘
```

### 4.2 2D State-Space Visualization

The following diagram shows how the two hidden states (BULL/BEAR) map to the 2D observation space:

```
                          WAVELET ENERGY (E)
                                 ▲
                                 │
                 High Energy     │         ┌─────────────────────┐
                 (Volatile)      │         │                     │
                                 │         │   BEAR REGIME       │
                                 │    ●    │   μ = [μᵣ⁻, μₑ⁺]    │
                                 │   ●●●   │   High energy       │
                                 │  ●●●●●  │   Negative returns  │
                                 │   ●●●   │                     │
                                 │    ●    └─────────────────────┘
                                 │
                                 │
                 ─────────────────┼───────────────────────────────▶ RETURN (r)
                 Negative        │                          Positive
                 Returns         │
                                 │    ●    ┌─────────────────────┐
                                 │   ●●●   │                     │
                                 │  ●●●●●  │   BULL REGIME       │
                                 │  ●●●●●  │   μ = [μᵣ⁺, μₑ⁻]    │
                                 │   ●●●   │   Low energy        │
                 Low Energy      │    ●    │   Positive returns  │
                 (Calm)          │         │                     │
                                 │         └─────────────────────┘
                                 │

        Legend:
        ●●●●● = Gaussian emission distribution (contour of Σᵢ)
        μᵣ⁺/⁻ = Mean return (positive/negative)
        μₑ⁺/⁻ = Mean wavelet energy (high/low)
```

---

## 5. Trading Strategy and Data Splitting

### 5.1 Walk-Forward Methodology

To avoid **lookahead bias** and ensure realistic backtesting, we use a strict **train-test split**:

```
    ════════════════════════════════════════════════════════════════════════
                              DATA TIMELINE
    ════════════════════════════════════════════════════════════════════════

    │◀────────── TRAINING PERIOD ──────────▶│◀──── TEST PERIOD ────▶│
    │                                        │                       │
    │   2000-01-01 to TRAIN_END_DATE         │   TEST_START_DATE     │
    │                                        │   to DATA_END_DATE    │
    │                                        │                       │
    │   • Download historical data           │   • Freeze model      │
    │   • Extract wavelet features           │   • Apply to new data │
    │   • Train HMM (Baum-Welch)             │   • Real-time decode  │
    │   • Learn A, B, π                      │   • Execute trades    │
    │                                        │                       │
    ════════════════════════════════════════════════════════════════════════
        DATA_START_DATE                    TRAIN_END_DATE         DATA_END_DATE
```

### 5.2 Current Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| `DATA_START_DATE` | `2000-01-01` | Beginning of historical data |
| `DATA_END_DATE` | `2008-12-31` | End of data download |
| `TRAIN_END_DATE` | `2007-12-31` | Last training date (inclusive) |
| `TEST_START_DATE` | `2008-01-01` | First test date |

**Example:** Train on 2000–2007 (8 years), test on 2008 (financial crisis year).

### 5.3 Regime-Aware Trading Strategy

The strategy uses a **RegimeHMMRiskManager** with the following logic:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TRADING DECISION MATRIX                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Current Regime    │    Signal    │    Position    │    Action            │
│   ─────────────────────────────────────────────────────────────────────     │
│   BULL (State 0)    │    BUY       │    Flat        │    ✅ ENTER LONG     │
│   BULL (State 0)    │    SELL      │    Long        │    ✅ EXIT           │
│   BEAR (State 1)    │    BUY       │    Flat        │    ❌ BLOCKED        │
│   BEAR (State 1)    │    SELL      │    Long        │    ✅ EXIT (graceful)│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

   Key Insight: Block new entries in BEAR regime, but allow graceful exits
               to avoid whipsaw from forced liquidation.
```

### 5.4 Risk Management Parameters

| Parameter | Variable | Default | Description |
|-----------|----------|---------|-------------|
| **Initial Capital** | `INITIAL_CAPITAL` | $100,000 | Starting portfolio value |
| **Position Size** | `MAX_POSITION_PCT` | 100% | Maximum capital to deploy |
| **Stop Loss** | `STOP_LOSS_PCT` | 2% | Automatic exit threshold |

### 5.5 Strategy Execution Pipeline

```
    ┌───────────────────────────────────────────────────────────────────┐
    │                    DAILY EXECUTION LOOP                           │
    └───────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  1. OBSERVE Market Data        │
                    │     • Get adjusted close Pₜ    │
                    │     • Compute return rₜ        │
                    └───────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  2. EXTRACT Features           │
                    │     • Wavelet energy Eₜ       │
                    │     • Form oₜ = [rₜ, Eₜ]      │
                    │     • Normalize with train μ,σ │
                    └───────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  3. DECODE Hidden State        │
                    │     • Run Viterbi/predict      │
                    │     • qₜ ∈ {BULL, BEAR}       │
                    └───────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  4. GENERATE Signal            │
                    │     • BULL → BUY signal       │
                    │     • BEAR → SELL signal      │
                    └───────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  5. REFINE Order               │
                    │     • Check regime constraints │
                    │     • Check position status    │
                    │     • Check stop-loss          │
                    └───────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  6. EXECUTE Trade              │
                    │     • BUY: Invest capital      │
                    │     • SELL: Liquidate position │
                    │     • HOLD: No action          │
                    └───────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  7. UPDATE Portfolio           │
                    │     • Record P&L               │
                    │     • Update NAV               │
                    └───────────────────────────────┘
                                    │
                                    ▼
                              Next Day (t+1)
```

---

## 6. Quick Start Guide

### 6.1 Prerequisites

```bash
pip install -r requirements.txt
```

Required packages:
- `numpy`
- `pandas`
- `yfinance`
- `hmmlearn`
- `pywt` (PyWavelets)
- `matplotlib`
- `seaborn`

### 6.2 Configure Settings

Edit `config.py` to set your parameters:

```python
# Date Configuration
DATA_START_DATE = "2000-01-01"  # Start of historical data
DATA_END_DATE = "2008-12-31"    # End of data
TRAIN_END_DATE = "2007-12-31"   # Train on 2000-2007
TEST_START_DATE = "2008-01-01"  # Test on 2008

# Model Configuration
N_STATES = 2      # BULL/BEAR
WINDOW = 5        # Wavelet window (days)
SCALE = 5         # Wavelet scale
```

### 6.3 Run Complete Pipeline

```bash
python run_pipeline.py
```

This executes:
1. **Download Data** → `data/SPY.csv`
2. **Train HMM** → `models/hmm_model.pkl`
3. **Backtest Strategy** → `results/backtest_results.csv`
4. **Generate Plots** → `results/*.png`

### 6.4 Run Individual Scripts

```bash
# Step-by-step execution
python 1_download_data.py    # Download SPY data
python 3_train_hmm.py        # Train HMM model
python 4_backtest.py         # Run backtest
python 5_visualize.py        # Generate visualizations
```

---

## 7. Configuration Reference

### 7.1 Date Settings

| Variable | Type | Description |
|----------|------|-------------|
| `DATA_START_DATE` | `str` | Start date for data download (YYYY-MM-DD) |
| `DATA_END_DATE` | `str` | End date for data download |
| `TRAIN_END_DATE` | `str` | Last date included in training set |
| `TEST_START_DATE` | `str` | First date of test/backtest period |
| `PLOT_START_DATE` | `str` | Start date for visualization context |

### 7.2 Model Parameters

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `N_STATES` | `int` | `2` | Number of hidden states |
| `WINDOW` | `int` | `5` | Wavelet lookback window (days) |
| `SCALE` | `float` | `5` | Wavelet scale parameter |
| `N_ITER` | `int` | `100` | Max Baum-Welch iterations |
| `RANDOM_STATE` | `int` | `42` | Random seed for reproducibility |

### 7.3 Trading Parameters

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `INITIAL_CAPITAL` | `float` | `100000.0` | Starting portfolio value |
| `MAX_POSITION_PCT` | `float` | `1.0` | Maximum position as % of capital |
| `STOP_LOSS_PCT` | `float` | `0.02` | Stop-loss threshold (2%) |

### 7.4 Output Files

| File | Description |
|------|-------------|
| `data/SPY.csv` | Downloaded price data with returns |
| `models/hmm_model.pkl` | Serialized trained HMM model |
| `results/backtest_results.csv` | Daily P&L and state predictions |
| `results/backtest_plot.png` | Portfolio equity curve |
| `results/state_stats.png` | Regime analysis visualization |

---

## References

1. Rabiner, L. R. (1989). "A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition." *Proceedings of the IEEE*, 77(2), 257-286.
2. Hamilton, J. D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." *Econometrica*, 57(2), 357-384.
3. Mallat, S. (2009). *A Wavelet Tour of Signal Processing: The Sparse Way*. Academic Press.

---

## License

MIT License
