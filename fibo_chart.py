#!/usr/bin/env python3
"""
Technical Analysis Chart Generator
Generates professional charts with Bollinger Bands, Fibonacci, SMA, MACD, and RSI.

Usage:
    python3 fibo_chart.py <TICKER> <START_DATE> [END_DATE]
    
Example:
    python3 fibo_chart.py AAPL 2025-01-01
    python3 fibo_chart.py AAPL 2025-01-01 2026-01-01
"""

import sys
import argparse
from datetime import datetime, timedelta

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator
from PIL import Image
import io


def normalize_columns(df):
    """Normalize column names from yfinance MultiIndex"""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def calculate_bollinger_bands(df, window=20, num_std=2):
    """Calculate Bollinger Bands"""
    close = df['Close']
    df['BB_Middle'] = close.rolling(window=window).mean()
    df['BB_Std'] = close.rolling(window=window).std()
    df['BB_Upper'] = df['BB_Middle'] + (df['BB_Std'] * num_std)
    df['BB_Lower'] = df['BB_Middle'] - (df['BB_Std'] * num_std)
    return df


def calculate_fibonacci_retracements(df):
    """Calculate Fibonacci retracement levels"""
    max_price = float(df['High'].max())
    min_price = float(df['Low'].min())
    diff = max_price - min_price
    
    levels = {
        'Fib_0': max_price,
        'Fib_236': max_price - 0.236 * diff,
        'Fib_382': max_price - 0.382 * diff,
        'Fib_500': max_price - 0.500 * diff,
        'Fib_618': max_price - 0.618 * diff,
        'Fib_786': max_price - 0.786 * diff,
        'Fib_100': min_price
    }
    return levels


def calculate_sma(df, period):
    """Calculate Simple Moving Average"""
    return df['Close'].rolling(window=period).mean()


def calculate_macd(df, fast=12, slow=26, signal=9):
    """Calculate MACD"""
    close = df['Close']
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    df['MACD'] = ema_fast - ema_slow
    df['MACD_Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
    return df


def calculate_rsi(df, period=14):
    """Calculate RSI"""
    close = df['Close']
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df


def get_fibonacci_colors():
    """Return professional Fibonacci colors"""
    return {
        'Fib_0': '#1a1a2e',      # Dark navy
        'Fib_236': '#e94560',    # Red
        'Fib_382': '#f39c12',   # Orange
        'Fib_500': '#9b59b6',   # Purple
        'Fib_618': '#3498db',   # Blue
        'Fib_786': '#2ecc71',   # Green
        'Fib_100': '#e74c3c'    # Red
    }


def create_chart(ticker, start_date, end_date=None):
    """Generate technical analysis chart"""
    
    # Download data
    if end_date:
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)
    else:
        df = yf.download(ticker, start=start_date, progress=False)
    
    # Normalize columns if MultiIndex
    df = normalize_columns(df)
    
    if df.empty:
        print(f"Error: No data found for {ticker}")
        return None
    
    # Calculate indicators
    df = calculate_bollinger_bands(df)
    df['SMA90'] = calculate_sma(df, 90)
    df['SMA200'] = calculate_sma(df, 200)
    df = calculate_macd(df)
    df = calculate_rsi(df)
    fib_levels = calculate_fibonacci_retracements(df)
    
    # Create figure with custom styling
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(16, 12), facecolor='#0d1117')
    
    # Create grid
    gs = gridspec.GridSpec(4, 1, height_ratios=[3, 1, 1, 1], hspace=0.1)
    
    # Colors
    price_color = '#00d4ff'
    bb_color = '#888888'
    sma90_color = '#f39c12'
    sma200_color = '#e74c3c'
    volume_color = '#2d3436'
    macd_color = '#00d4ff'
    signal_color = '#e74c3c'
    rsi_color = '#9b59b6'
    fib_colors = get_fibonacci_colors()
    
    # ========== MAIN CHART (Price) ==========
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor('#0d1117')
    
    # Price line
    ax1.plot(df.index, df['Close'], color=price_color, linewidth=1.5, label='Price')
    
    # Bollinger Bands
    ax1.fill_between(df.index, df['BB_Upper'], df['BB_Lower'], 
                     alpha=0.1, color=bb_color, label='Bollinger Bands')
    ax1.plot(df.index, df['BB_Upper'], color=bb_color, linewidth=0.5, alpha=0.5)
    ax1.plot(df.index, df['BB_Lower'], color=bb_color, linewidth=0.5, alpha=0.5)
    
    # SMA
    ax1.plot(df.index, df['SMA90'], color=sma90_color, linewidth=1, 
             label='SMA 90', linestyle='--')
    ax1.plot(df.index, df['SMA200'], color=sma200_color, linewidth=1, 
             label='SMA 200', linestyle='-.')
    
    # Fibonacci levels (horizontal lines)
    for level, price in fib_levels.items():
        ax1.axhline(y=price, color=fib_colors[level], linestyle='-', 
                    linewidth=0.8, alpha=0.6)
    
    # Add Fibonacci labels
    for level, price in fib_levels.items():
        if level not in ['Fib_0', 'Fib_100']:
            ax1.annotate(f'Fib {level.replace("Fib_", "")}', xy=(0.005, price), 
                        xycoords=('axes fraction', 'data'),
                        fontsize=7, color=fib_colors[level], alpha=0.8,
                        verticalalignment='center')
    
    # Title and labels
    current_price = float(df['Close'].iloc[-1])
    start_price = float(df['Close'].iloc[0])
    price_change = ((current_price - start_price) / start_price) * 100
    
    ax1.set_title(f'{ticker} • {current_price:.2f} ({price_change:+.2f}%) • {start_date} to {df.index[-1].strftime("%Y-%m-%d")}', 
                  fontsize=14, fontweight='bold', color='white', pad=10)
    ax1.set_ylabel('Price', fontsize=10, color='white')
    ax1.legend(loc='upper left', fontsize=8, facecolor='#1a1a2e', edgecolor='none')
    ax1.grid(True, alpha=0.1, color='white')
    ax1.set_xlim(df.index[0], df.index[-1])
    
    # ========== VOLUME ==========
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax2.set_facecolor('#0d1117')
    
    # Color volume bars based on price direction
    closes = df['Close'].values
    opens = df['Open'].values
    colors = ['#e74c3c' if closes[i] < opens[i] else '#2ecc71' for i in range(len(closes))]
    volumes = df['Volume'].values
    ax2.bar(df.index, volumes/1e6, color=colors, alpha=0.7, width=1)
    ax2.set_ylabel('Volume (M)', fontsize=8, color='white')
    ax2.yaxis.set_major_locator(MaxNLocator(nbins=3))
    ax2.grid(True, alpha=0.1, color='white')
    ax2.set_xticklabels([])
    
    # ========== MACD ==========
    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    ax3.set_facecolor('#0d1117')
    
    ax3.bar(df.index, df['MACD_Histogram'], color=macd_color, alpha=0.3, width=1)
    ax3.plot(df.index, df['MACD'], color=macd_color, linewidth=1, label='MACD')
    ax3.plot(df.index, df['MACD_Signal'], color=signal_color, linewidth=1, label='Signal')
    ax3.axhline(y=0, color='white', linestyle='-', linewidth=0.5, alpha=0.3)
    ax3.set_ylabel('MACD', fontsize=8, color='white')
    ax3.legend(loc='upper left', fontsize=7, facecolor='#1a1a2e', edgecolor='none')
    ax3.yaxis.set_major_locator(MaxNLocator(nbins=3))
    ax3.grid(True, alpha=0.1, color='white')
    ax3.set_xticklabels([])
    
    # ========== RSI ==========
    ax4 = fig.add_subplot(gs[3], sharex=ax1)
    ax4.set_facecolor('#0d1117')
    
    ax4.plot(df.index, df['RSI'], color=rsi_color, linewidth=1)
    ax4.axhline(y=70, color='red', linestyle='--', linewidth=0.5, alpha=0.5)
    ax4.axhline(y=30, color='green', linestyle='--', linewidth=0.5, alpha=0.5)
    ax4.axhline(y=50, color='white', linestyle='-', linewidth=0.3, alpha=0.3)
    ax4.fill_between(df.index, df['RSI'], 70, where=(df['RSI'] > 70), 
                     alpha=0.3, color='red')
    ax4.fill_between(df.index, df['RSI'], 30, where=(df['RSI'] < 30), 
                     alpha=0.3, color='green')
    ax4.set_ylabel('RSI', fontsize=8, color='white')
    ax4.set_ylim(0, 100)
    ax4.yaxis.set_major_locator(MaxNLocator(nbins=3))
    ax4.grid(True, alpha=0.1, color='white')
    ax4.set_xlabel('Date', fontsize=10, color='white')
    
    # Format x-axis dates
    fig.autofmt_xdate()
    
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    buf.seek(0)
    
    plt.close(fig)
    
    return buf


def save_chart(buf, ticker):
    """Save chart to file"""
    # Using /tmp which is allowed for Telegram media paths
    filename = f'/tmp/{ticker}_chart.png'
    
    # Ensure directory exists
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'wb') as f:
        f.write(buf.getvalue())
    
    return filename


if __name__ == '__main__':
    from datetime import datetime, timedelta
    
    parser = argparse.ArgumentParser(description='Generate technical analysis charts')
    parser.add_argument('ticker', help='Stock ticker symbol (e.g., AAPL, BTC-USD)')
    parser.add_argument('start_date', nargs='?', default=None, help='Start date (YYYY-MM-DD). Default: 2 years ago')
    parser.add_argument('end_date', nargs='?', default=None, help='End date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    # Default to 2 years ago if no start date
    if args.start_date is None:
        two_years_ago = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
        args.start_date = two_years_ago
        print(f"No start date provided, using default: {args.start_date}")
    
    print(f"Generating chart for {args.ticker} from {args.start_date}...")
    buf = create_chart(args.ticker, args.start_date, args.end_date)
    
    if buf:
        filename = save_chart(buf, args.ticker)
        print(f"Chart saved to: {filename}")
    else:
        print("Failed to generate chart")
        sys.exit(1)
