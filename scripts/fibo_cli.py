#!/usr/bin/env python3
"""
CLI para generar gráficos Fibonacci+ de activos financieros.
Uso: fibo <TICKER> [FECHA_INICIO] [FECHA_FIN]
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Always resolve relative to workspace root
WORKSPACE_DIR = os.path.expanduser('~/.openclaw/workspace')
CHART_SCRIPT = os.path.join(WORKSPACE_DIR, 'fibo_chart.py')
OUTPUT_DIR = '/tmp'

def generar_fibo(ticker, fecha_inicio=None, fecha_fin=None):
    """Genera el gráfico Fibo+ para un ticker."""
    # Determinar fechas
    if not fecha_fin:
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
    if not fecha_inicio:
        fecha_inicio = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
    
    print(f"Generando Fibo+ para {ticker} ({fecha_inicio} → {fecha_fin})...")
    
    # Ejecutar el script de gráficos
    cmd = [sys.executable, CHART_SCRIPT, ticker, fecha_inicio, fecha_fin]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return 1
    
    # Mostrar resultado
    output_file = f"/tmp/{ticker}_chart.png"
    if os.path.exists(output_file):
        print(f"Gráfico generado: {output_file}")
        print(f"Tamaño: {os.path.getsize(output_file) / 1024:.1f} KB")
    else:
        # Buscar archivo generado
        for f in os.listdir(OUTPUT_DIR):
            if f.startswith(ticker) and f.endswith('.png'):
                print(f"Gráfico generado: {os.path.join(OUTPUT_DIR, f)}")
                break
    
    return 0

def main():
    parser = argparse.ArgumentParser(
        description='Generador de gráficos Fibonacci+',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Ejemplos:
  fibo SAN.MC                    # 2 años por defecto
  fibo SAN.MC 2024-01-01        # Desde fecha específica
  fibo SAN.MC 2024-01-01 2025-01-01  # Rango de fechas
  fibo AAPL 2023-01-01          # Apple
  fibo BTC-USD                   # Bitcoin
        '''
    )
    
    parser.add_argument('ticker', help='Símbolo del activo (ej: SAN.MC, AAPL, BTC-USD)')
    parser.add_argument('fecha_inicio', nargs='?', default=None, 
                        help='Fecha inicio (YYYY-MM-DD). Por defecto: hace 2 años')
    parser.add_argument('fecha_fin', nargs='?', default=None,
                        help='Fecha fin (YYYY-MM-DD). Por defecto: hoy')
    
    args = parser.parse_args()
    
    return generar_fibo(args.ticker, args.fecha_inicio, args.fecha_fin)

if __name__ == '__main__':
    sys.exit(main() or 0)
