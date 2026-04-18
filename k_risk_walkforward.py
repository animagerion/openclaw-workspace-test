import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import warnings

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
# 2. DESCARGA DE DATOS MULTIANUAL
# =====================================================================
print("--- BACKTEST WALK-FORWARD (SIN SESGO DE ANTICIPACIÓN) ---")

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'BRK-B', 'V', 'JNJ', 'WMT',
           'PG', 'JPM', 'UNH', 'MA', 'HD', 'CVX', 'ABBV', 'LLY', 'MRK', 'PEP']
benchmark = 'SPY'

# Descargamos desde 2021 para poder predecir 2022
print("Descargando datos históricos (2021 - 2024)...")
datos = yf.download(tickers + [benchmark], start='2021-01-01', end='2025-01-01', progress=False)['Close']
datos = datos.dropna()
retornos_diarios = datos.pct_change().dropna()

# =====================================================================
# 3. LÓGICA DE VENTANA MÓVIL (WALK-FORWARD)
# =====================================================================
años_inversion = [2022, 2023, 2024]
curva_equity_cartera = pd.Series(dtype=float)
curva_equity_spy = pd.Series(dtype=float)

detalles_por_año = {}

for año_target in años_inversion:
    año_train = año_target - 1
    print(f"\n[{año_target}] Calculando K-Risk con datos del año {año_train}...")

    # Extraer datos del año de entrenamiento (T-1)
    datos_train = datos[datos.index.year == año_train]

    resultados_train = []
    for ticker in tickers:
        precios = datos_train[ticker].values
        k_risk = calcular_k_risk(precios)
        peso_proxy = datos_train[ticker].iloc[-1]  # Precio a final de año

        resultados_train.append({
            'Ticker': ticker,
            'K_Risk': k_risk,
            'Peso_Proxy': peso_proxy
        })

    df_res = pd.DataFrame(resultados_train).sort_values('K_Risk')

    # Filtro: Descartar la mitad más ruidosa y quedarse con las 5 más grandes
    mitad = len(df_res) // 2
    acciones_limpias = df_res.head(mitad)
    cartera_seleccionada = acciones_limpias.sort_values('Peso_Proxy', ascending=False).head(5)['Ticker'].tolist()

    print(f"  Ranking K-Risk ({año_train}):")
    for _, row in df_res.iterrows():
        marca = " <<<" if row['Ticker'] in cartera_seleccionada else ""
        print(f"  {row['Ticker']:6s} K={row['K_Risk']:.4f}{marca}")

    print(f"  -> Cartera para {año_target}: {cartera_seleccionada}")

    # Evaluar rendimiento en el año de inversión (T)
    retornos_test = retornos_diarios[retornos_diarios.index.year == año_target]

    retornos_cartera_año = retornos_test[cartera_seleccionada].mean(axis=1)
    retornos_spy_año = retornos_test[benchmark]

    rent_cartera_año = (1 + retornos_cartera_año).cumprod().iloc[-1] - 1
    rent_spy_año = (1 + retornos_spy_año).cumprod().iloc[-1] - 1

    detalles_por_año[año_target] = {
        'cartera': cartera_seleccionada,
        'rent_cartera': rent_cartera_año,
        'rent_spy': rent_spy_año
    }

    print(f"  -> Rentabilidad {año_target}: SPY {rent_spy_año*100:.2f}%, Cartera {rent_cartera_año*100:.2f}%")

    # Concatenar para la curva final
    curva_equity_cartera = pd.concat([curva_equity_cartera, retornos_cartera_año])
    curva_equity_spy = pd.concat([curva_equity_spy, retornos_spy_año])

# =====================================================================
# 4. RESULTADOS FINALES Y GRÁFICO
# =====================================================================
# Calcular el valor acumulado (Base 100)
acumulado_cartera = (1 + curva_equity_cartera).cumprod() * 100
acumulado_spy = (1 + curva_equity_spy).cumprod() * 100

retorno_total_cartera = (acumulado_cartera.iloc[-1] / 100) - 1
retorno_total_spy = (acumulado_spy.iloc[-1] / 100) - 1

print("\n" + "=" * 50)
print(f"RENDIMIENTO ACUMULADO (2022 - 2024)")
print(f"SPY (S&P 500): {retorno_total_spy*100:.2f}%")
print(f"Cartera K-Risk (Walk-Forward): {retorno_total_cartera*100:.2f}%")
print("=" * 50)

# Volatilidad y Sharpe
vol_spy = curva_equity_spy.std() * np.sqrt(252) * 100
vol_cartera = curva_equity_cartera.std() * np.sqrt(252) * 100
sharpe_spy = (retorno_total_spy * 100) / vol_spy if vol_spy > 0 else 0
sharpe_cartera = (retorno_total_cartera * 100) / vol_cartera if vol_cartera > 0 else 0
maxdd_spy = ((acumulado_spy / acumulado_spy.cummax()) - 1).min() * 100
maxdd_cartera = ((acumulado_cartera / acumulado_cartera.cummax()) - 1).min() * 100

print(f"\nVolatilidad anualizada: SPY {vol_spy:.2f}%, Cartera {vol_cartera:.2f}%")
print(f"Sharpe simplificado: SPY {sharpe_spy:.2f}, Cartera {sharpe_cartera:.2f}")
print(f"Max Drawdown: SPY {maxdd_spy:.2f}%, Cartera {maxdd_cartera:.2f}%")

# Gráfico
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

ax1 = axes[0]
ax1.plot(acumulado_spy.index, acumulado_spy.values, label='S&P 500 (SPY)', color='black', linewidth=2)
ax1.plot(acumulado_cartera.index, acumulado_cartera.values, label='Cartera K-Risk (Walk-Forward)', color='green', linewidth=2)
ax1.set_title('Backtest Realista (Walk-Forward 2022-2024): K-Risk vs S&P 500')
ax1.set_ylabel('Capital (Base 100)')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Añadir líneas verticales para cada año
for año in años_inversion:
    inicio_año = acumulado_spy[acumulado_spy.index.year == año].index[0]
    ax1.axvline(x=inicio_año, color='gray', linestyle='--', alpha=0.5)
    ax1.text(inicio_año, ax1.get_ylim()[1] * 0.98, str(año), fontsize=8, color='gray')

# Detalle por año como tabla
ax2 = axes[1]
ax2.axis('off')
table_data = []
for año, datos_año in detalles_por_año.items():
    diff = datos_año['rent_cartera'] - datos_año['rent_spy']
    signo = "+" if diff >= 0 else ""
    table_data.append([
        str(año),
        ", ".join(datos_año['cartera']),
        f"{datos_año['rent_spy']*100:.2f}%",
        f"{datos_año['rent_cartera']*100:.2f}%",
        f"{signo}{diff*100:.2f}pp"
    ])

col_labels = ['Año', 'Cartera', 'SPY', 'K-Risk', 'Diferencia']
table = ax2.table(cellText=table_data, colLabels=col_labels, loc='center',
                  cellLoc='center', colColours=['#f0f0f0']*5)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.8)
ax2.set_title('Detalle por año (Cartera K-Risk vs SPY)', fontsize=11, pad=20)

plt.tight_layout()
plt.savefig('/home/gerion/.openclaw/workspace/k_risk_walkforward.png', dpi=150)
plt.close()
print("\nGráfico guardado en /home/gerion/.openclaw/workspace/k_risk_walkforward.png")
