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
    y = y - np.mean(y)  # Centrar la serie
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
# 2. DESCARGA DE DATOS Y CÁLCULO DE MÉTRICAS
# =====================================================================
print("--- INICIANDO EXPERIMENTO DE RÉPLICA DE ÍNDICE CON K-RISK ---")

# Usamos el SPY como benchmark y una lista de las mayores empresas tecnológicas/financieras (proxys del top del S&P)
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'BRK-B', 'V', 'JNJ', 'WMT',
           'PG', 'JPM', 'UNH', 'MA', 'HD', 'CVX', 'ABBV', 'LLY', 'MRK', 'PEP']

benchmark = 'SPY'
start_date = '2024-01-01'
end_date = '2025-01-01'  # 2024 — mercado alcista

print(f"Descargando datos históricos (2024) para {len(tickers)} activos y el SPY...")
datos = yf.download(tickers + [benchmark], start=start_date, end=end_date)['Close']
datos = datos.dropna()

resultados = []

print("Calculando K-Risk para cada acción...")
for ticker in tickers:
    precios = datos[ticker].values
    k_risk = calcular_k_risk(precios)
    # Aproximación del peso en el índice (usamos el precio inicial como proxy de capitalización para simplificar en este test)
    peso_proxy = datos[ticker].iloc[0]

    resultados.append({
        'Ticker': ticker,
        'K_Risk': k_risk,
        'Peso_Proxy': peso_proxy
    })

df_res = pd.DataFrame(resultados)

# =====================================================================
# 3. EL FILTRO DE LIMPIEZA (HEURÍSTICA DIRECTA)
# =====================================================================
print("\nAplicando Filtro de Limpieza...")

# Paso A: Ordenar por K-Risk (de más limpio a más ruidoso)
df_res = df_res.sort_values('K_Risk')

# Paso B: Cortar por la mitad (Nos quedamos solo con la mitad más "ordenada" estructuralmente)
mitad = len(df_res) // 2
acciones_limpias = df_res.head(mitad)
print(f"Descartadas las {mitad} acciones con mayor K-Risk (más ruido estructural).")

# Paso C: Seleccionar los "Drivers" (Las 5 más grandes de las que pasaron el filtro)
cartera_final = acciones_limpias.sort_values('Peso_Proxy', ascending=False).head(5)['Ticker'].tolist()

print(f"\nCartera Final Seleccionada (Las 5 más grandes dentro del grupo de bajo K-Risk):")
print(cartera_final)

# =====================================================================
# 4. ANÁLISIS COMPARATIVO CON SPY
# =====================================================================
print("\n--- ANÁLISIS COMPARATIVO ---")

# Mostrar ranking completo de K-Risk
print("\nRanking de K-Risk (de menor a mayor):")
print(df_res[['Ticker', 'K_Risk', 'Peso_Proxy']].to_string(index=False))

# Calcular rentabilidad de la cartera filtrada vs SPY
precios_cartera = datos[cartera_final]
precios_spy = datos[benchmark]

rent_cartera = (precios_cartera.iloc[-1] / precios_cartera.iloc[0] - 1).mean() * 100
rent_spy = (precios_spy.iloc[-1] / precios_spy.iloc[0] - 1) * 100

print(f"\nRentabilidad SPY (2024): {rent_spy:.2f}%")
print(f"Rentabilidad promedio cartera filtrada (2024): {rent_cartera:.2f}%")

# Volatilidad comparada
vol_cartera = precios_cartera.pct_change().std().mean() * 100
vol_spy = precios_spy.pct_change().std() * 100

print(f"\nVolatilidad SPY (2024): {vol_spy:.2f}%")
print(f"Volatilidad promedio cartera filtrada (2024): {vol_cartera:.2f}%")

# sharpe简易
sharpe_cartera = rent_cartera / vol_cartera if vol_cartera > 0 else 0
sharpe_spy = rent_spy / vol_spy if vol_spy > 0 else 0

print(f"\nRatio Sharpe simplificado SPY: {sharpe_spy:.2f}")
print(f"Ratio Sharpe simplificado cartera: {sharpe_cartera:.2f}")

# Gráfico comparativo
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Normalizar precios para comparar
precios_cartera_norm = precios_cartera / precios_cartera.iloc[0] * 100
precios_spy_norm = precios_spy / precios_spy.iloc[0] * 100

ax1 = axes[0]
ax1.plot(precios_spy_norm.index, precios_spy_norm.values, label='SPY (Benchmark)', color='black', linewidth=2)
for ticker in cartera_final:
    ax1.plot(precios_cartera_norm[ticker].index, precios_cartera_norm[ticker].values, alpha=0.5, label=f'{ticker}')
ax1.set_title('Cartera Filtrada por K-Risk vs SPY (2022, normalizado a 100)')
ax1.set_ylabel('Índice de precio (base 100)')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)

# Gráfico de barras K-Risk
ax2 = axes[1]
colores = ['green' if t in cartera_final else 'red' for t in df_res['Ticker']]
ax2.bar(df_res['Ticker'], df_res['K_Risk'], color=colores)
ax2.axhline(y=df_res['K_Risk'].median(), color='orange', linestyle='--', label='Mediana')
ax2.set_title('K-Risk por acción (verde = en cartera, rojo = descartada)')
ax2.set_ylabel('K-Risk')
ax2.tick_params(axis='x', rotation=45)
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('/home/gerion/.openclaw/workspace/k_risk_cartera_vs_spy_2024.png', dpi=150)
plt.close()
print("\nGráfico guardado en /home/gerion/.openclaw/workspace/k_risk_cartera_vs_spy_2024.png")

# =====================================================================
# 4. BACKTEST Y COMPARACIÓN CON EL S&P 500
# =====================================================================
print("\n--- BACKTEST 2022 ---")

# Retornos diarios
retornos = datos.pct_change().dropna()

# Retorno del SPY (Benchmark)
retorno_acumulado_spy = (1 + retornos[benchmark]).cumprod()

# Retorno de nuestra Cartera (Equiponderada para simplificar)
retornos_cartera = retornos[cartera_final].mean(axis=1)
retorno_acumulado_cartera = (1 + retornos_cartera).cumprod()

# Gráfico de resultados
plt.figure(figsize=(10, 5))
plt.plot(retorno_acumulado_spy.index, retorno_acumulado_spy.values, label='S&P 500 (SPY)', color='black', linewidth=2)
plt.plot(retorno_acumulado_cartera.index, retorno_acumulado_cartera.values, label='Réplica Limpia K-Risk (5 Activos)', color='blue', linewidth=2)

plt.title('Backtest 2024: Réplica del S&P 500 vs Filtro K-Risk')
plt.ylabel('Retorno Acumulado')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('/home/gerion/.openclaw/workspace/k_risk_backtest_2024.png', dpi=150)
plt.close()
print("Gráfico guardado en /home/gerion/.openclaw/workspace/k_risk_backtest_2024.png")

# Cálculo del Tracking Error
diferencia_retornos = retornos_cartera - retornos[benchmark]
tracking_error = diferencia_retornos.std() * np.sqrt(252) * 100
print(f"\nTracking Error Anualizado: {tracking_error:.2f}%")

# Más métricas
print(f"\nMáximo Drawdown SPY: {(retorno_acumulado_spy / retorno_acumulado_spy.cummax() - 1).min() * 100:.2f}%")
print(f"Máximo Drawdown Cartera K-Risk: {(retorno_acumulado_cartera / retorno_acumulado_cartera.cummax() - 1).min() * 100:.2f}%")
print(f"Retorno acumulado SPY: {(retorno_acumulado_spy.iloc[-1] - 1) * 100:.2f}%")
print(f"Retorno acumulado Cartera K-Risk: {(retorno_acumulado_cartera.iloc[-1] - 1) * 100:.2f}%")
print(f"Volatilidad SPY (anualizada): {retornos[benchmark].std() * np.sqrt(252) * 100:.2f}%")
print(f"Volatilidad Cartera K-Risk (anualizada): {retornos_cartera.std() * np.sqrt(252) * 100:.2f}%")
