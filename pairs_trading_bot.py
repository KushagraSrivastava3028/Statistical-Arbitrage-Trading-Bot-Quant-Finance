import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt

def download_data(ticker1, ticker2, start='2020-01-01', end='2023-01-01'):
    """
    Download historical adjusted close prices for two tickers.
    """
    tickers = f"{ticker1} {ticker2}"
    data = yf.download(tickers, start=start, end=end)
    print("Columns:", data.columns)
    print(data.head())
    if 'Adj Close' in data.columns:
        return data['Adj Close']
    elif 'Close' in data.columns:
        return data['Close']
    else:
        return data

def check_cointegration(series1, series2):
    """
    Perform Augmented Dickey-Fuller test on the residuals of the linear relationship.
    Returns the p-value and the hedge ratio.
    """
    # Calculate hedge ratio using OLS
    series1 = sm.add_constant(series1)
    model = sm.OLS(series2, series1).fit()
    hedge_ratio = model.params.iloc[1]
    
    # Calculate residuals (spread)
    spread = series2 - hedge_ratio * series1['Adj Close'] if 'Adj Close' in series1 else series2 - hedge_ratio * series1.iloc[:, 1]
    
    # Perform ADF test
    adf_result = adfuller(spread)
    p_value = adf_result[1]
    
    return p_value, hedge_ratio, spread

def calculate_zscore(series, window=30):
    """
    Calculate Z-Score of the series based on a rolling mean and standard deviation.
    """
    r_mean = series.rolling(window=window).mean()
    r_std = series.rolling(window=window).std()
    z_score = (series - r_mean) / r_std
    return z_score

def backtest(spread, z_score, entry_threshold=2.0, exit_threshold=0.5):
    """
    Simple backtest engine.
    Long Spread (Short B, Long A) when Z-Score < -entry_threshold
    Short Spread (Long B, Short A) when Z-Score > entry_threshold
    Exit position when Z-Score crosses exit_threshold
    """
    positions = pd.DataFrame(index=spread.index)
    positions['Long'] = (z_score < -entry_threshold) * 1.0
    positions['Short'] = (z_score > entry_threshold) * -1.0
    positions['Total'] = positions['Long'] + positions['Short']
    
    return positions

def plot_results(spread, z_score, positions, pair_names):
    """
    Plot the spread, Z-Score and trade signals.
    """
    plt.figure(figsize=(14, 10))
    
    # Plot Spread
    plt.subplot(2, 1, 1)
    plt.plot(spread, label='Spread')
    plt.title(f'Spread Calculation: {pair_names[1]} - Hedge * {pair_names[0]}')
    plt.legend()
    
    # Plot Z-Score with signals
    plt.subplot(2, 1, 2)
    plt.plot(z_score, label='Z-Score')
    plt.axhline(2.0, color='r', linestyle='--', label='Entry Threshold (+2)')
    plt.axhline(-2.0, color='g', linestyle='--', label='Entry Threshold (-2)')
    plt.axhline(0, color='black', linestyle='-')
    
    # Add trade markers
    # Long Spread (Buy)
    buy_signals = positions[positions['Total'] == 1].index
    plt.scatter(buy_signals, z_score[buy_signals], marker='^', color='g', label='Long Spread')
    
    # Short Spread (Sell)
    sell_signals = positions[positions['Total'] == -1].index
    plt.scatter(sell_signals, z_score[sell_signals], marker='v', color='r', label='Short Spread')
    
    plt.title('Z-Score & Trade Signals')
    plt.legend()
    plt.savefig('backtest_results.png')
    print("Plot saved to 'backtest_results.png'")

if __name__ == "__main__":
    # 1. Select Pair
    # Generally, good pairs are in the same sector (e.g., KO & PEP, GLD & GDX)
    ticker_a = 'PEP'
    ticker_b = 'KO'
    
    print(f"Downloading data for {ticker_a} and {ticker_b}...")
    data = download_data(ticker_a, ticker_b)
    
    if data.empty:
        print("No data downloaded. Check your internet connection or ticker names.")
    else:
        # Drop NaNs
        data = data.dropna()
        series_a = data[ticker_a]
        series_b = data[ticker_b]

        # 2. Check Cointegration
        print("Checking cointegration...")
        p_value, hedge_ratio, spread = check_cointegration(series_a, series_b)
        print(f"P-Value: {p_value:.5f}")
        print(f"Hedge Ratio: {hedge_ratio:.5f}")
        
        if p_value < 0.05:
            print("Pair is cointegrated (p < 0.05). Proceeding with strategy.")
            
            # 3. Calculate Signals
            z_score = calculate_zscore(spread, window=30)
            
            # 4. Backtest
            positions = backtest(spread, z_score)
            
            # Simple PnL display (Conceptual)
            print("Backtest complete. Plotting results...")
            plot_results(spread, z_score, positions, (ticker_a, ticker_b))
        else:
            print("Pair is NOT cointegrated. Mean reversion strategy may not be suitable.")
