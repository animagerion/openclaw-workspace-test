#!/usr/bin/env python3
"""
Bot de Trading Simulado
=======================
Estrategias técnicas implementadas:
- SMA Crossover (cruce de medias móviles simples)
- RSI (Relative Strength Index)

ADVERTENCIA: Esto es SIMULACIÓN. NO es asesoramiento financiero.
Los resultados pasados NO garantizan resultados futuros.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import argparse
import sys

# ============================================================================
# CONFIGURACIÓN - Modifica estos parámetros según necesites
# ============================================================================

DEFAULT_CONFIG = {
    "ticker": "AAPL",
    "start_date": "2023-01-01",
    "end_date": "2024-12-31",
    # SMA Crossover
    "sma_short": 20,    # Período media móvil corta
    "sma_long": 50,     # Período media móvil larga
    # RSI
    "rsi_period": 14,   # Período RSI
    "rsi_oversold": 30,  # Nivel de sobreventa
    "rsi_overbought": 70, # Nivel de sobrecompra
    # Capital inicial
    "initial_capital": 10000.0,
}

# ============================================================================
# FUNCIONES DE ESTRATEGIAS
# ============================================================================

def calculate_sma(data: pd.Series, period: int) -> pd.Series:
    """Calcula la media móvil simple."""
    return data.rolling(window=period).mean()


def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
    """
    Calcula el Relative Strength Index (RSI).
    RSI = 100 - (100 / (1 + RS))
    donde RS = promedio de ganancias / promedio de pérdidas
    """
    delta = data.diff()
    
    # Separar ganancias y pérdidas
    gains = delta.where(delta > 0, 0.0)
    losses = (-delta).where(delta < 0, 0.0)
    
    # Promedios móviles exponenciales (usando media móvil simple para simplicity)
    avg_gain = gains.rolling(window=period).mean()
    avg_loss = losses.rolling(window=period).mean()
    
    # Calcular RS y RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def generate_sma_signals(data: pd.DataFrame, short_period: int, long_period: int) -> pd.DataFrame:
    """
    Genera señales de trading basadas en cruce de SMAs.
    - Señal = 1 (COMPRAR) cuando SMA corta cruza encima de SMA larga
    - Señal = -1 (VENDER) cuando SMA corta cruza debajo de SMA larga
    - Señal = 0 (MANTENER) en caso contrario
    """
    df = data.copy()
    
    # Calcular SMAs
    df['SMA_Short'] = calculate_sma(df['Close'], short_period)
    df['SMA_Long'] = calculate_sma(df['Close'], long_period)
    
    # Generar señales
    df['Signal'] = 0
    
    # Cruce hacia arriba = compra
    df.loc[(df['SMA_Short'] > df['SMA_Long']) & 
           (df['SMA_Short'].shift(1) <= df['SMA_Long'].shift(1)), 'Signal'] = 1
    
    # Cruce hacia abajo = venta
    df.loc[(df['SMA_Short'] < df['SMA_Long']) & 
           (df['SMA_Short'].shift(1) >= df['SMA_Long'].shift(1)), 'Signal'] = -1
    
    # Posición: 1 = comprado, 0 = sin posición
    # Posición: mantener 1 (comprado) desde señal de compra hasta señal de venta
    position = 0
    positions = []
    for signal in df['Signal']:
        if signal == 1:
            position = 1  # Comprar
        elif signal == -1:
            position = 0  # Vender
        positions.append(position)
    df['Position'] = positions
    
    return df


def generate_rsi_signals(data: pd.DataFrame, period: int, oversold: float, overbought: float) -> pd.DataFrame:
    """
    Genera señales de trading basadas en RSI.
    - COMPRAR cuando RSI < nivel de sobreventa (el activo está infravalorado)
    - VENDER cuando RSI > nivel de sobrecompra (el activo está sobrevalorado)
    """
    df = data.copy()
    
    # Calcular RSI
    df['RSI'] = calculate_rsi(df['Close'], period)
    
    # Generar señales
    df['Signal_RSI'] = 0
    
    # Entrada: RSI sale de sobreventa (cruce hacia arriba)
    df.loc[(df['RSI'] < oversold) & (df['RSI'].shift(1) >= oversold), 'Signal_RSI'] = 1
    
    # Salida: RSI entra en sobrecompra (cruce hacia abajo)
    df.loc[(df['RSI'] > overbought) & (df['RSI'].shift(1) <= overbought), 'Signal_RSI'] = -1
    
    return df


# ============================================================================
# FUNCIÓN DE BACKTESTING
# ============================================================================

def backtest_strategy(data: pd.DataFrame, initial_capital: float, position_col: str = 'Position') -> dict:
    """
    Realiza backtesting de una estrategia.
    
    Returns:
        dict con métricas de rendimiento
    """
    df = data.copy()
    
    # Inicializar variables
    capital = initial_capital
    shares = 0
    position = 0  # 0 = sin posición, 1 = comprado
    
    trades = []
    portfolio_values = []
    
    for i, (idx, row) in enumerate(df.iterrows()):
        price = row['Close']
        signal = row.get('Signal', 0)
        signal_rsi = row.get('Signal_RSI', 0)
        
        # Combinar señales (usamos Signal principal)
        if signal == 1 and position == 0:
            # COMPRAR
            shares = capital / price
            capital = 0
            position = 1
            trades.append({
                'date': idx,
                'type': 'BUY',
                'price': price,
                'shares': shares
            })
        elif signal == -1 and position == 1:
            # VENDER
            capital = shares * price
            trades.append({
                'date': idx,
                'type': 'SELL',
                'price': price,
                'value': capital
            })
            shares = 0
            position = 0
        
        # Valor del portfolio
        portfolio_value = capital + (shares * price)
        portfolio_values.append(portfolio_value)
    
    df['Portfolio_Value'] = portfolio_values
    
    # Calcular métricas
    final_value = portfolio_values[-1]
    total_return = (final_value - initial_capital) / initial_capital * 100
    
    # Buy & Hold
    initial_price = df['Close'].iloc[0]
    final_price = df['Close'].iloc[-1]
    buy_hold_return = (final_price - initial_price) / initial_price * 100
    buy_hold_final = initial_capital * (1 + buy_hold_return / 100)
    
    # Máximo drawdown
    portfolio_series = pd.Series(portfolio_values)
    rolling_max = portfolio_series.expanding().max()
    drawdowns = (portfolio_series - rolling_max) / rolling_max * 100
    max_drawdown = drawdowns.min()
    
    # Número de trades
    num_trades = len([t for t in trades if t['type'] == 'BUY'])
    
    # Win rate (si hay ventas)
    sells = [t for t in trades if t['type'] == 'SELL']
    if len(sells) >= 2:
        buy_prices = [t['price'] for t in trades if t['type'] == 'BUY']
        sell_prices = [t['price'] for t in sells]
        wins = sum(1 for b, s in zip(buy_prices[:len(sell_prices)], sell_prices) if s > b)
        win_rate = wins / len(sells) * 100 if sells else 0
    else:
        win_rate = 0
    
    return {
        'final_value': final_value,
        'total_return': total_return,
        'buy_hold_return': buy_hold_return,
        'buy_hold_final': buy_hold_final,
        'max_drawdown': max_drawdown,
        'num_trades': num_trades,
        'win_rate': win_rate,
        'trades': trades,
        'portfolio_values': portfolio_values
    }


# ============================================================================
# FUNCIÓN DE GRÁFICOS
# ============================================================================

def create_trading_chart(data: pd.DataFrame, results: dict, config: dict, output_path: str = '/tmp/trading_chart.png'):
    """Genera gráficos de la estrategia de trading."""
    
    fig, axes = plt.subplots(4, 1, figsize=(14, 16), sharex=True)
    fig.suptitle(f'Análisis de Trading: {config["ticker"]}\n'
                 f'Período: {config["start_date"]} a {config["end_date"]}', 
                 fontsize=14, fontweight='bold')
    
    #Color scheme
    colors = {
        'price': '#1f77b4',
        'sma_short': '#ff7f0e',
        'sma_long': '#2ca02c',
        'buy': '#2ecc71',
        'sell': '#e74c3c',
        'rsi_oversold': '#27ae60',
        'rsi_overbought': '#c0392b',
    }
    
    # ---------- GRÁFICO 1: PRECIO Y SMAs ----------
    ax1 = axes[0]
    ax1.plot(data.index, data['Close'], label='Precio', color=colors['price'], linewidth=1.5, alpha=0.8)
    ax1.plot(data.index, data['SMA_Short'], label=f'SMA {config["sma_short"]}', 
             color=colors['sma_short'], linewidth=1.2, linestyle='--')
    ax1.plot(data.index, data['SMA_Long'], label=f'SMA {config["sma_long"]}', 
             color=colors['sma_long'], linewidth=1.2, linestyle='--')
    
    # Marcar señales de compra/venta
    buy_signals = data[data['Signal'] == 1]
    sell_signals = data[data['Signal'] == -1]
    ax1.scatter(buy_signals.index, buy_signals['Close'], color=colors['buy'], 
                marker='^', s=100, label='Compra', zorder=5)
    ax1.scatter(sell_signals.index, sell_signals['Close'], color=colors['sell'], 
                marker='v', s=100, label='Venta', zorder=5)
    
    ax1.set_ylabel('Precio ($)')
    ax1.set_title('Precio y Medias Móviles (SMA Crossover)')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # ---------- GRÁFICO 2: RSI ----------
    ax2 = axes[1]
    ax2.plot(data.index, data['RSI'], label='RSI', color='#9b59b6', linewidth=1.5)
    ax2.axhline(y=config['rsi_oversold'], color=colors['rsi_oversold'], 
                linestyle='--', label=f'Sobreventa ({config["rsi_oversold"]})')
    ax2.axhline(y=config['rsi_overbought'], color=colors['rsi_overbought'], 
                linestyle='--', label=f'Sobrecompra ({config["rsi_overbought"]})')
    ax2.axhline(y=50, color='gray', linestyle=':', alpha=0.5)
    
    # Zonas sombreadas
    ax2.fill_between(data.index, config['rsi_oversold'], 0, alpha=0.1, color=colors['rsi_oversold'])
    ax2.fill_between(data.index, config['rsi_overbought'], 100, alpha=0.1, color=colors['rsi_overbought'])
    
    ax2.set_ylabel('RSI')
    ax2.set_title('Relative Strength Index (RSI)')
    ax2.set_ylim(0, 100)
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    # ---------- GRÁFICO 3: POSICIÓN Y SEÑALES ----------
    ax3 = axes[2]
    ax3.fill_between(data.index, data['Position'], 0, step='post', 
                     alpha=0.3, color=colors['sma_short'], label='Posición (1=comprado)')
    ax3.set_ylabel('Posición')
    ax3.set_title('Posición en el Mercado')
    ax3.set_ylim(-0.1, 1.1)
    ax3.legend(loc='upper left')
    ax3.grid(True, alpha=0.3)
    
    # ---------- GRÁFICO 4: VALOR DEL PORTFOLIO ----------
    ax4 = axes[3]
    portfolio_values = results['portfolio_values']
    ax4.plot(data.index, portfolio_values, label='Estrategia', 
             color=colors['sma_short'], linewidth=2)
    
    # Buy & Hold
    initial_price = data['Close'].iloc[0]
    buy_hold_values = (data['Close'] / initial_price) * config['initial_capital']
    ax4.plot(data.index, buy_hold_values, label='Buy & Hold', 
             color=colors['sma_long'], linewidth=1.5, linestyle='--', alpha=0.8)
    
    ax4.axhline(y=config['initial_capital'], color='gray', linestyle=':', alpha=0.5)
    ax4.set_ylabel('Valor ($)')
    ax4.set_title('Comparación: Estrategia vs Buy & Hold')
    ax4.legend(loc='upper left')
    ax4.grid(True, alpha=0.3)
    
    # Formato eje x
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax4.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Gráfico guardado en: {output_path}")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal del bot de trading."""
    
    print("=" * 60)
    print("🤖 BOT DE TRADING SIMULADO")
    print("=" * 60)
    print()
    
    # Parsear argumentos
    parser = argparse.ArgumentParser(description='Bot de Trading Simulado')
    parser.add_argument('--ticker', type=str, default=DEFAULT_CONFIG['ticker'], 
                        help='Símbolo del activo (ej: AAPL, MSFT, SPY)')
    parser.add_argument('--start', type=str, default=DEFAULT_CONFIG['start_date'],
                        help='Fecha de inicio (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, default=DEFAULT_CONFIG['end_date'],
                        help='Fecha de fin (YYYY-MM-DD)')
    parser.add_argument('--capital', type=float, default=DEFAULT_CONFIG['initial_capital'],
                        help='Capital inicial')
    
    args = parser.parse_args()
    
    # Configuración
    config = {
        "ticker": args.ticker,
        "start_date": args.start,
        "end_date": args.end,
        "sma_short": DEFAULT_CONFIG['sma_short'],
        "sma_long": DEFAULT_CONFIG['sma_long'],
        "rsi_period": DEFAULT_CONFIG['rsi_period'],
        "rsi_oversold": DEFAULT_CONFIG['rsi_oversold'],
        "rsi_overbought": DEFAULT_CONFIG['rsi_overbought'],
        "initial_capital": args.capital,
    }
    
    print(f"📈 Descargando datos de {config['ticker']}...")
    print(f"   Período: {config['start_date']} a {config['end_date']}")
    print(f"   Capital inicial: ${config['initial_capital']:,.2f}")
    print()
    
    try:
        # Descargar datos
        ticker = yf.Ticker(config['ticker'])
        df = ticker.history(start=config['start_date'], end=config['end_date'])
        
        if df.empty:
            print(f"❌ Error: No se encontraron datos para {config['ticker']}")
            sys.exit(1)
        
        print(f"✅ Datos descargados: {len(df)} días de trading")
        
        # Asegurar que Close es Series
        if isinstance(df, pd.DataFrame):
            if 'Close' not in df.columns:
                print("❌ Error: Columna 'Close' no encontrada")
                sys.exit(1)
        
        # Generar señales
        print(f"\n📊 Generando señales...")
        print(f"   SMA Crossover: corta={config['sma_short']}, larga={config['sma_long']}")
        print(f"   RSI: período={config['rsi_period']}, sobreventa={config['rsi_oversold']}, sobrecompra={config['rsi_overbought']}")
        
        df = generate_sma_signals(df, config['sma_short'], config['sma_long'])
        df = generate_rsi_signals(df, config['rsi_period'], 
                                  config['rsi_oversold'], config['rsi_overbought'])
        
        # Backtesting
        print("\n🔄 Ejecutando backtesting...")
        results = backtest_strategy(df, config['initial_capital'])
        
        # Mostrar resultados
        print("\n" + "=" * 60)
        print("📈 RESULTADOS DEL BACKTESTING")
        print("=" * 60)
        
        print(f"\n💰 VALOR FINAL DEL PORTFOLIO: ${results['final_value']:,.2f}")
        print(f"📊 RETORNO DE LA ESTRATEGIA: {results['total_return']:.2f}%")
        print(f"📊 RETORNO BUY & HOLD: {results['buy_hold_return']:.2f}%")
        print(f"📉 MÁXIMO DRAWDOWN: {results['max_drawdown']:.2f}%")
        print(f"🔢 NÚMERO DE TRADES: {results['num_trades']}")
        print(f"🎯 WIN RATE: {results['win_rate']:.1f}%")
        
        # Comparación
        diff = results['total_return'] - results['buy_hold_return']
        if diff > 0:
            print(f"\n✅ La estrategia supera a Buy & Hold por {diff:.2f}%")
        else:
            print(f"\n⚠️ Buy & Hold supera a la estrategia por {-diff:.2f}%")
        
        # Lista de trades
        if results['trades']:
            print(f"\n📋 ÚLTIMOS TRADES:")
            for trade in results['trades'][-5:]:
                print(f"   {trade['date'].strftime('%Y-%m-%d')} | {trade['type']} | ${trade['price']:.2f}")
        
        # Generar gráfico
        output_path = f'/tmp/trading_{config["ticker"].lower()}_{datetime.now().strftime("%Y%m%d")}.png'
        create_trading_chart(df, results, config, output_path)
        
        print("\n" + "=" * 60)
        print("⚠️ DISCLAIMER: Esto es SIMULACIÓN. NO es asesoramiento financiero.")
        print("   Los resultados pasados NO garantizan resultados futuros.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
