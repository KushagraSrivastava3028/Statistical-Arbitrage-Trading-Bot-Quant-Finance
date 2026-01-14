# Statistical Arbitrage Trading Bot (Quant Finance)

## Overview
The **Statistical Arbitrage Trading Bot** is a quantitative trading system that implements a **pairs trading strategy** based on **cointegration and mean reversion**.

It downloads historical price data, tests for cointegration using the **Augmented Dickey–Fuller (ADF) test**, constructs a market-neutral spread using **OLS regression**, and generates trading signals based on **Z-score thresholds**.

This project reflects real-world **quantitative finance** techniques used in **hedge funds, prop trading firms, and systematic trading desks**.

---

## Strategy Logic
1. Select two correlated assets from the same sector  
2. Estimate hedge ratio using **OLS regression**
3. Compute the price spread
4. Test spread stationarity using **ADF test**
5. Trade spread deviations using **Z-score mean reversion**
6. Maintain market-neutral exposure

---

## Key Concepts Used
- Statistical Arbitrage
- Pairs Trading
- Cointegration
- Mean Reversion
- Augmented Dickey-Fuller (ADF) Test
- Ordinary Least Squares (OLS)
- Z-Score Signal Generation

---

## Tech Stack
- **Python**
- **pandas / numpy** – Data processing
- **yfinance** – Market data
- **statsmodels** – Statistical modeling
- **matplotlib** – Visualization

---

## Data Source
- **Yahoo Finance** (via yFinance)

---

## How the Strategy Works

### Cointegration Test
- Linear regression is used to compute the hedge ratio
- Residuals (spread) are tested for stationarity using ADF
- Only cointegrated pairs (`p < 0.05`) are traded

### Trading Signals
| Z-Score | Action |
|-------|-------|
| Z < -2 | Long spread |
| Z > +2 | Short spread |
| Z → 0 | Exit position |

---

## How to Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/Statistical-Arbitrage-Trading-Bot.git
cd Statistical-Arbitrage-Trading-Bot
```
### 2️⃣ Install Dependencies
```bash
pip install pandas numpy matplotlib yfinance statsmodels
```

### 3️⃣ Run the Script
```bash
python stat_arb.py
```

## Output

--- Spread plot

--- Z-score plot with buy/sell signals

--- Automatically saved backtest visualization
