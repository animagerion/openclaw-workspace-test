import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import warnings
from dateutil.relativedelta import relativedelta

warnings.filterwarnings('ignore')

# =====================================================================
# 1. FUNCIÓN CENTRAL: CÁLCULO DEL K-RISK
# =====================================================================
def calcular_k_risk(serie_temporal):
    """Calcula la complejidad K-Risk de una serie de precios."""
    N = len(serie_temporal)
    if N < 4: return np.nan

    y = np.array(serie_temporal)
    y = y - np.mean(y)
    TSS = np.sum(y**2)
    if TSS == 0: return 1.0

    fft_coeffs = np.fft.fft(y)
    amplitudes = np.abs(fft_coeffs)
    mitad_n = N // 2
    idx_ordenados = np.argsort(amplitudes[1:mitad_n+1])[::-1] + 1

    G_p = []
    for p in range(1, mitad_n + 1):
        mask = np.zeros(N, dtype=bool)
        mask[0] = True
        for i in range(p):
            idx = idx_ordenados[i]
            mask[idx] = True
            if idx != N - idx:
                mask[N - idx] = True

        espectro_filtrado = np.zeros(N, dtype=complex)
        espectro_filtrado[mask] = fft_coeffs[mask]
        reconstruccion = np.real(np.fft.ifft(espectro_filtrado))

        RSS = np.sum((y - reconstruccion)**2)
        r_cuadrado = 1 - (RSS / TSS)
        G_p.append(max(0.0, r_cuadrado))

    G_p = np.array(G_p)
    p_array = np.arange(1, mitad_n + 1)
    T_p = p_array / mitad_n

    ganancia = G_p - T_p
    Lambda = np.sum(ganancia)
    Lambda_Theta = np.sum(1 - T_p)

    if Lambda <= 0: return 100.0
    return Lambda_Theta / Lambda

# =====================================================================
# 2. DESCARGA DE DATOS
# =====================================================================
print("--- BACKTEST TRIMESTRAL: REBALANCEO CADA 3 MESES ---")
print("K-Risk ALTO (invertido) - Ventana 6 meses previos")

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'BRK-B', 'V', 'JNJ', 'WMT',
           'PG', 'JPM', 'UNH', 'MA', 'HD', 'CVX', 'ABBV', 'LLY', 'MRK', 'PEP']
benchmark = 'SPY'

# Descargamos desde 2021-07 para tener datos suficientes para la primera ventana de training
print("Descargando datos históricos (1999-01 a 2025-07)...")
datos = yf.download(tickers + [benchmark], start='1999-01-01', end='2025-07-01', progress=False)['Close']
datos = datos.dropna()
retornos_diarios = datos.pct_change().dropna()

print(f"Datos disponibles: {datos.index[0].date()} -> {datos.index[-1].date()}")
print(f"Ticker con datos: {sum(1 for t in tickers if datos[t].dropna().shape[0] > 100)}/{len(tickers)}")
print(f"Total de tickers: {len(tickers)} + 1 benchmark = {len(tickers)+1}")

# =====================================================================
# 3. TRIMESTRES A EVALUAR
# =====================================================================
# Trimestres: Q1=ene-mar, Q2=abr-jun, Q3=jul-sep, Q4=oct-dic
trimestres = [
    # (año, trimestre, fecha_inicio_test, fecha_fin_test)
    (2022, 1, '2022-01-01', '2022-03-31'),
    (2022, 2, '2022-04-01', '2022-06-30'),
    (2022, 3, '2022-07-01', '2022-09-30'),
    (2022, 4, '2022-10-01', '2022-12-31'),
    (2023, 1, '2023-01-01', '2023-03-31'),
    (2023, 2, '2023-04-01', '2023-06-30'),
    (2023, 3, '2023-07-01', '2023-09-30'),
    (2023, 4, '2023-10-01', '2023-12-31'),
    (2024, 1, '2024-01-01', '2024-03-31'),
    (2024, 2, '2024-04-01', '2024-06-30'),
    (2024, 3, '2024-07-01', '2024-09-30'),
    (2024, 4, '2024-10-01', '2024-12-31'),
    (2025, 1, '2025-01-01', '2025-03-31'),
]

curva_equity_cartera = pd.Series(dtype=float)
curva_equity_spy = pd.Series(dtype=float)

# Para cada trimestre: entrenamos con los 3 meses anteriores
ventana_train_meses = 6  # Ventana de training: 3 meses

detalles_por_trimestre = []

for año, q, fecha_inicio, fecha_fin in trimestres:
    # Determinar fecha de inicio de training: 3 meses antes del inicio del trimestre
    from datetime import datetime
    inicio_test_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_inicio_train_dt = inicio_test_dt - relativedelta(months=ventana_train_meses)
    fecha_inicio_train = fecha_inicio_train_dt.strftime('%Y-%m-%d')

    # Extraer datos de training (los 3 meses previos)
    datos_train = datos[(datos.index >= fecha_inicio_train) & (datos.index < fecha_inicio)]

    if len(datos_train) < 30:
        print(f"[{año} Q{q}] Datos insuficientes para training ({len(datos_train)} días), saltando.")
        continue

    resultados_train = []
    for ticker in tickers:
        precios = datos_train[ticker].values
        k_risk = calcular_k_risk(precios)
        peso_proxy = datos_train[ticker].iloc[-1]
        resultados_train.append({'Ticker': ticker, 'K_Risk': k_risk, 'Peso_Proxy': peso_proxy})

    df_res = pd.DataFrame(resultados_train).sort_values('K_Risk')

    # Filtro: mitad inferior (menos ruido) y las 5 más grandes
    mitad = len(df_res) // 2
    acciones_ruidosas = df_res.tail(mitad)
    cartera = cartera_base = acciones_ruidosas.sort_values('Peso_Proxy', ascending=False).head(5)['Ticker'].tolist()

    # Evaluar en el trimestre
    retornos_test = retornos_diarios[(retornos_diarios.index >= fecha_inicio) & (retornos_diarios.index <= fecha_fin)]
    retornos_cartera_q = retornos_test[cartera].mean(axis=1)
    retornos_spy_q = retornos_test[benchmark]

    rent_cartera_q = (1 + retornos_cartera_q).cumprod().iloc[-1] - 1
    rent_spy_q = (1 + retornos_spy_q).cumprod().iloc[-1] - 1

    diff = rent_cartera_q - rent_spy_q
    marca = "WIN" if diff > 0 else "LOSE"

    print(f"[{año} Q{q}] {fecha_inicio_train} a {fecha_inicio[:10]} | "
          f"SPY: {rent_spy_q*100:+.2f}% | K-Risk: {rent_cartera_q*100:+.2f}% | {marca} ({diff*100:+.2f}pp)")

    detalles_por_trimestre.append({
        'trimestre': f'{año} Q{q}',
        'cartera': cartera,
        'rent_spy': rent_spy_q,
        'rent_krisk': rent_cartera_q,
        'diff': diff
    })

    curva_equity_cartera = pd.concat([curva_equity_cartera, retornos_cartera_q])
    curva_equity_spy = pd.concat([curva_equity_spy, retornos_spy_q])

# =====================================================================
# 4. RESULTADOS FINALES
# =====================================================================
acumulado_cartera = (1 + curva_equity_cartera).cumprod() * 100
acumulado_spy = (1 + curva_equity_spy).cumprod() * 100

ret_total_cartera = (acumulado_cartera.iloc[-1] / 100) - 1
ret_total_spy = (acumulado_spy.iloc[-1] / 100) - 1

ganados = sum(1 for d in detalles_por_trimestre if d['diff'] > 0)
total_q = len(detalles_por_trimestre)

print("\n" + "=" * 60)
print(f"RENDIMIENTO ACUMULADO TRIMESTRAL (2022 Q1 - 2025 Q1)")
print(f"SPY: {ret_total_spy*100:+.2f}%")
print(f"Cartera K-Risk (trimestral): {ret_total_cartera*100:+.2f}%")
print(f"Trimestres ganados por K-Risk: {ganados}/{total_q}")
print("=" * 60)

vol_spy = curva_equity_spy.std() * np.sqrt(252) * 100
vol_cartera = curva_equity_cartera.std() * np.sqrt(252) * 100
sharpe_spy = (ret_total_spy * 100) / vol_spy if vol_spy > 0 else 0
sharpe_cartera = (ret_total_cartera * 100) / vol_cartera if vol_cartera > 0 else 0
maxdd_spy = ((acumulado_spy / acumulado_spy.cummax()) - 1).min() * 100
maxdd_cartera = ((acumulado_cartera / acumulado_cartera.cummax()) - 1).min() * 100

print(f"\nVolatilidad anualizada: SPY {vol_spy:.2f}%, Cartera {vol_cartera:.2f}%")
print(f"Sharpe simplificado: SPY {sharpe_spy:.2f}, Cartera {sharpe_cartera:.2f}")
print(f"Max Drawdown: SPY {maxdd_spy:.2f}%, Cartera {maxdd_cartera:.2f}%")

# =====================================================================
# 5. GRÁFICOS
# =====================================================================
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

ax1 = axes[0]
ax1.plot(acumulado_spy.index, acumulado_spy.values, label='S&P 500 (SPY)', color='black', linewidth=2)
ax1.plot(acumulado_cartera.index, acumulado_cartera.values, label='Cartera ALTO K-Risk (invertido) (ventana 6m)', color='green', linewidth=2)
ax1.set_title('Backtest Trimestral (2022 Q1 - 2025 Q1): K-Risk vs S&P 500\n'
              f'K-Risk ALTO (invertido) - Ventana 6 meses previos')
ax1.set_ylabel('Capital (Base 100)')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Tabla de detalle por trimestre
ax2 = axes[1]
ax2.axis('off')
table_data = []
for d in detalles_por_trimestre:
    signo = "+" if d['diff'] >= 0 else ""
    cartera_str = ", ".join(d['cartera'])
    table_data.append([
        d['trimestre'],
        f"{d['rent_spy']*100:+.2f}%",
        f"{d['rent_krisk']*100:+.2f}%",
        f"{signo}{d['diff']*100:.2f}pp",
        cartera_str
    ])

col_labels = ['Trimestre', 'SPY', 'K-Risk', 'Diff', 'Cartera']
table = ax2.table(cellText=table_data, colLabels=col_labels, loc='center',
                  cellLoc='center', colColours=['#e0e0e0']*5)
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1.1, 1.5)
ax2.set_title(f'Rendimiento por trimestre | K-Risk gana {ganados}/{total_q}', fontsize=11, pad=20)

# Color rows based on win/lose
for i, d in enumerate(table_data):
    if d[3].startswith('+'):
        table[(i+1, 3)].set_facecolor('#d4edda')
    else:
        table[(i+1, 3)].set_facecolor('#f8d7da')

plt.tight_layout()
plt.savefig('/home/gerion/.openclaw/workspace/k_risk_trimestral.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nGráfico guardado en /home/gerion/.openclaw/workspace/k_risk_trimestral.png")
