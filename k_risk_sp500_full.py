import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import warnings
from dateutil.relativedelta import relativedelta

warnings.filterwarnings('ignore')

# =====================================================================
# 1. FUNCIÓN K-RISK
# =====================================================================
def calcular_k_risk(serie_temporal):
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
# 2. CARGAR COMPOSICIÓN HISTÓRICA DEL S&P 500
# =====================================================================
print("Cargando composición histórica del S&P 500 desde 1996...")
hist = pd.read_csv('/home/gerion/.openclaw/workspace/sp500_historical.csv')
hist.columns = ['date', 'tickers']
hist['date'] = pd.to_datetime(hist['date'])
hist = hist.sort_values('date')

def get_base_tickers(ticker_string):
    tickers_raw = ticker_string.split(',')
    base_tickers = set()
    for t in tickers_raw:
        t = t.strip()
        if '-' in t:
            base = t.split('-')[0]
        else:
            base = t
        base_tickers.add(base)
    return base_tickers

all_tickers_raw = set()
for _, row in hist.iterrows():
    all_tickers_raw.update(get_base_tickers(row['tickers']))

# Limpiar tickers problemáticos (guiones, puntos, muy largos)
problematic = {'BRK-B', 'BF.B', 'RDS.A', 'OGE', 'STI', 'LYB', 'SYY', 'ETR', 'AIV'}
all_tickers = sorted(t for t in all_tickers_raw
                      if t not in problematic
                      and len(t) <= 5
                      and t.isalpha()
                      and t not in {'T', 'V', 'P', 'C', 'K', 'I', 'S', 'X', 'O', 'M', 'N', 'H', 'L', 'J', 'G', 'F', 'D', 'B', 'A', 'W', 'Y', 'U', 'Z', 'Q'})

print(f"Ticker históricos únicos (tras limpieza): {len(all_tickers)}")

# =====================================================================
# 3. DESCARGA DE DATOS DE YFINANCE
# =====================================================================
# Descargamos con un rango que maximise datos disponibles
# Para tickers modernos (post-2000), empieza desde 2000 es suficiente
# Para simular desde 1996, necesitamos datos desde entonces

print("Descargando datos (esto puede tardar varios minutos)...")
datos = yf.download(all_tickers + ['SPY'], start='1996-01-01', end='2025-07-01',
                    progress=True)['Close']
datos = datos.dropna(axis=1, how='all')
print(f"Tickers con datos: {datos.shape[1]}/{len(all_tickers)+1}")

retornos_diarios = datos.pct_change().dropna()

# =====================================================================
# 4. GENERAR TRIMESTRES
# =====================================================================
trimestres = []
for year in range(2000, 2026):
    for q_num, (m_start, m_end) in enumerate([(1,3),(4,6),(7,9),(10,12)], 1):
        if year == 2025 and q_num > 1:
            continue
        date_start = pd.Timestamp(f'{year}-{m_start:02d}-01')
        date_end = pd.Timestamp(f'{year}-{m_end:02d}-01')
        trimestres.append((year, q_num, date_start, date_end))

print(f"\nTrimestres a evaluar: {len(trimestres)}")

# =====================================================================
# 5. BACKTEST
# =====================================================================
ventana_train_meses = 6
N_TOP = 50

resultados = []

for idx_t, (año, q, fecha_inicio, fecha_fin) in enumerate(trimestres):
    train_end = fecha_inicio - pd.Timedelta(days=1)
    train_start = train_end - relativedelta(months=ventana_train_meses)

    # Composición del quarter
    comps = hist[hist['date'] <= train_end]
    if len(comps) == 0:
        continue
    comp_row = comps.iloc[-1]
    tickers_q = get_base_tickers(comp_row['tickers'])

    # Filtrar a los que tenemos datos
    tickers_q = [t for t in tickers_q if t in datos.columns]

    if len(tickers_q) < 20:
        continue

    # Capitalización proxificada (precio final del periodo de training)
    try:
        datos_train = datos[tickers_q][(datos.index >= train_start) & (datos.index <= train_end)]
        if len(datos_train) < 30:
            continue
        cap_proxy = datos_train.iloc[-1]
    except Exception:
        continue

    # Top N por capitalización
    top_tickers = cap_proxy.sort_values(ascending=False).head(N_TOP).index.tolist()

    # K-Risk para cada uno
    k_vals = {}
    for t in top_tickers:
        serie = datos_train[t].dropna().values
        if len(serie) >= 30:
            k_vals[t] = calcular_k_risk(serie)

    if len(k_vals) < 10:
        continue

    df_k = pd.DataFrame(list(k_vals.items()), columns=['Ticker', 'K_Risk']).sort_values('K_Risk')
    mitad = len(df_k) // 2

    cartera_bajo = df_k.head(mitad)['Ticker'].tolist()
    cartera_alto = df_k.tail(mitad)['Ticker'].tolist()

    # Returns del quarter
    ret_test = retornos_diarios[(retornos_diarios.index >= fecha_inicio) & (retornos_diarios.index <= fecha_fin)]
    if len(ret_test) < 10:
        continue

    # SPY benchmark
    spy_ok = 'SPY' in retornos_diarios.columns and ret_test['SPY'].dropna().shape[0] > 10
    rent_spy_q = (1 + ret_test['SPY'].dropna()).cumprod().iloc[-1] - 1 if spy_ok else np.nan

    rent_bajo = (1 + ret_test[cartera_bajo].mean(axis=1).dropna()).cumprod().iloc[-1] - 1
    rent_alto = (1 + ret_test[cartera_alto].mean(axis=1).dropna()).cumprod().iloc[-1] - 1

    diff_bajo = rent_bajo - rent_spy_q if spy_ok else np.nan
    diff_alto = rent_alto - rent_spy_q if spy_ok else np.nan

    resultados.append({
        'trimestre': f'{año} Q{q}',
        'fecha': fecha_inicio,
        'rent_spy': rent_spy_q,
        'rent_bajo': rent_bajo,
        'rent_alto': rent_alto,
        'diff_bajo': diff_bajo,
        'diff_alto': diff_alto,
        'cartera_bajo': cartera_bajo,
        'cartera_alto': cartera_alto,
    })

    spy_str = f"{rent_spy_q*100:+.1f}%" if spy_ok else "N/A"
    diff_b_str = f"{diff_bajo*100:+.1f}pp" if spy_ok else "N/A"
    diff_a_str = f"{diff_alto*100:+.1f}pp" if spy_ok else "N/A"
    print(f"[{año} Q{q}] SPY: {spy_str} | BAJO: {rent_bajo*100:+.1f}% ({diff_b_str}) | ALTO: {rent_alto*100:+.1f}% ({diff_a_str})")

# =====================================================================
# 6. RESULTADOS
# =====================================================================
if len(resultados) == 0:
    print("ERROR: No se generó ningún resultado. Revisar datos.")
    exit(1)

# Curvas equity
curva_bajo = pd.Series(dtype=float)
curva_alto = pd.Series(dtype=float)
curva_spy = pd.Series(dtype=float)

for r in resultados:
    ret_test = retornos_diarios[(retornos_diarios.index >= r['fecha']) & (retornos_diarios.index <= r['fecha'] + relativedelta(months=3))]
    curva_bajo = pd.concat([curva_bajo, ret_test[r['cartera_bajo']].mean(axis=1).dropna()])
    curva_alto = pd.concat([curva_alto, ret_test[r['cartera_alto']].mean(axis=1).dropna()])
    if not np.isnan(r['rent_spy']):
        curva_spy = pd.concat([curva_spy, ret_test['SPY'].dropna()])

acum_bajo = (1 + curva_bajo).cumprod() * 100
acum_alto = (1 + curva_alto).cumprod() * 100
acum_spy = (1 + curva_spy).cumprod() * 100

ret_total_bajo = (acum_bajo.iloc[-1] / 100) - 1
ret_total_alto = (acum_alto.iloc[-1] / 100) - 1
ret_total_spy = (acum_spy.iloc[-1] / 100) - 1

spy_results = [r for r in resultados if not np.isnan(r['rent_spy'])]
total_q = len(resultados)
ganados_bajo = sum(1 for r in spy_results if r['diff_bajo'] > 0)
ganados_alto = sum(1 for r in spy_results if r['diff_alto'] > 0)
total_spy = len(spy_results)

vol_bajo = curva_bajo.std() * np.sqrt(252) * 100
vol_alto = curva_alto.std() * np.sqrt(252) * 100
vol_spy = curva_spy.std() * np.sqrt(252) * 100

sharpe_bajo = (ret_total_bajo * 100) / vol_bajo if vol_bajo > 0 else 0
sharpe_alto = (ret_total_alto * 100) / vol_alto if vol_alto > 0 else 0
sharpe_spy = (ret_total_spy * 100) / vol_spy if vol_spy > 0 else 0

maxdd_bajo = ((acum_bajo / acum_bajo.cummax()) - 1).min() * 100
maxdd_alto = ((acum_alto / acum_alto.cummax()) - 1).min() * 100
maxdd_spy = ((acum_spy / acum_spy.cummax()) - 1).min() * 100

print(f"\n{'='*70}")
print(f"BACKTEST S&P 500 COMPLETO — {resultados[0]['trimestre']} a {resultados[-1]['trimestre']}")
print(f"{'='*70}")
print(f"SPY:          {ret_total_spy*100:+.2f}%  | Sharpe: {sharpe_spy:.2f} | Vol: {vol_spy:.1f}% | MaxDD: {maxdd_spy:.1f}%")
print(f"K-Risk BAJO:  {ret_total_bajo*100:+.2f}%  | Sharpe: {sharpe_bajo:.2f} | Vol: {vol_bajo:.1f}% | MaxDD: {maxdd_bajo:.1f}% | Wins: {ganados_bajo}/{total_spy}")
print(f"K-Risk ALTO:  {ret_total_alto*100:+.2f}%  | Sharpe: {sharpe_alto:.2f} | Vol: {vol_alto:.1f}% | MaxDD: {maxdd_alto:.1f}% | Wins: {ganados_alto}/{total_spy}")
print(f"{'='*70}")

# Por décadas
decadas = {}
for r in spy_results:
    año = int(r['trimestre'][:4])
    decada = f"{(año//10)*10}s"
    if decada not in decadas:
        decadas[decada] = {'bajo': [], 'alto': [], 'spy': []}
    decadas[decada]['bajo'].append(r['rent_bajo'])
    decadas[decada]['alto'].append(r['rent_alto'])
    decadas[decada]['spy'].append(r['rent_spy'])

print("\nPor década:")
for decada in sorted(decadas.keys()):
    d = decadas[decada]
    acum_b = (1 + pd.Series(d['bajo'])).prod() - 1
    acum_a = (1 + pd.Series(d['alto'])).prod() - 1
    acum_s = (1 + pd.Series(d['spy'])).prod() - 1
    n = len(d['spy'])
    wins_b = sum(1 for b, s in zip(d['bajo'], d['spy']) if b > s)
    wins_a = sum(1 for a, s in zip(d['alto'], d['spy']) if a > s)
    print(f"  {decada} ({n}q): SPY {acum_s*100:+.1f}% | BAJO {acum_b*100:+.1f}% ({wins_b}/{n}) | ALTO {acum_a*100:+.1f}% ({wins_a}/{n})")

# =====================================================================
# 7. GRÁFICOS
# =====================================================================
fig, axes = plt.subplots(2, 1, figsize=(16, 10))

ax1 = axes[0]
ax1.plot(acum_spy.index, acum_spy.values, label=f'SPY ({ret_total_spy*100:+.0f}%)', color='black', linewidth=2)
ax1.plot(acum_bajo.index, acum_bajo.values, label=f'K-Risk BAJO ({ret_total_bajo*100:+.0f}%)', color='blue', linewidth=1.5, alpha=0.8)
ax1.plot(acum_alto.index, acum_alto.values, label=f'K-Risk ALTO ({ret_total_alto*100:+.0f}%)', color='red', linewidth=1.5, alpha=0.8)
ax1.set_title(f'K-Risk en S&P 500: {resultados[0]["trimestre"]} → {resultados[-1]["trimestre"]}\nTop 50 componentes por capitalización | Ventana 6m | Rebalanceo trimestral')
ax1.set_ylabel('Capital (Base 100)')
ax1.grid(True, alpha=0.3)
ax1.legend()

ax2 = axes[1]
ax2.axis('off')
table_data = []
for r in spy_results:
    table_data.append([
        r['trimestre'],
        f"{r['rent_spy']*100:+.1f}%",
        f"{r['rent_bajo']*100:+.1f}%",
        f"{r['diff_bajo']*100:+.1f}pp",
        f"{r['rent_alto']*100:+.1f}%",
        f"{r['diff_alto']*100:+.1f}pp",
    ])

col_labels = ['Trimestre', 'SPY', 'K-Bajo', 'Diff-B', 'K-Alto', 'Diff-A']
table = ax2.table(cellText=table_data, colLabels=col_labels, loc='center',
                  cellLoc='center', colColours=['#e0e0e0']*6)
table.auto_set_font_size(False)
table.set_fontsize(6)
table.scale(1.0, 1.1)
ax2.set_title(f'BAJO gana {ganados_bajo}/{total_spy} quarters | ALTO gana {ganados_alto}/{total_spy}', fontsize=10, pad=20)

plt.tight_layout()
plt.savefig('/home/gerion/.openclaw/workspace/k_risk_sp500_full.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"\nGráfico guardado en /home/gerion/.openclaw/workspace/k_risk_sp500_full.png")
