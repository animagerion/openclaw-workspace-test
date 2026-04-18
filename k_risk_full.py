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
# 2. DATOS
# =====================================================================
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'BRK-B', 'V', 'JNJ', 'WMT',
           'PG', 'JPM', 'UNH', 'MA', 'HD', 'CVX', 'ABBV', 'LLY', 'MRK', 'PEP']
benchmark = 'SPY'

print("Descargando datos históricos completos (1999-2025)...")
datos = yf.download(tickers + [benchmark], start='1999-01-01', end='2025-07-01', progress=False)['Close']
datos = datos.dropna()
retornos_diarios = datos.pct_change().dropna()

# Encontrar el primer día con datos para TODOS los tickers
primero_todos = datos.dropna().index[0]
print(f"Datos disponibles con todos los tickers desde: {primero_todos.date()}")

# =====================================================================
# 3. GENERAR TRIMESTRES DESDE QUE HAY DATOS (6m de training antes)
# =====================================================================
from datetime import datetime

# Primer test posible: 6 meses después del primer día con todos los datos
inicio_train_dt = primero_todos
fecha_primer_test_dt = inicio_train_dt + relativedelta(months=6)

# Generar todos los trimestres desde fecha_primer_test_dt hasta 2025-Q1
trimestres = []
año = fecha_primer_test_dt.year
mes_actual = fecha_primer_test_dt.month

# Alinear al inicio del trimestre siguiente
q_map = {1: (1, '01-01', '03-31'), 2: (4, '04-01', '06-30'),
         3: (7, '07-01', '09-30'), 4: (10, '10-01', '12-31')}
# Determinar en qué Q estamos
for q_num, (q_start, q_start_d, q_end) in q_map.items():
    if q_start <= mes_actual <= (q_map[q_num][0] + 2 if q_num > 1 else 3):
        q_actual = q_num
        break

# Generar desde el siguiente trimestre al actual
next_q = q_actual + 1 if q_actual < 4 else 1
next_año = año if q_actual < 4 else año + 1

while not (next_año > 2025 or (next_año == 2025 and next_q > 1)):
    q_start, q_start_d, q_end = q_map[next_q]
    fecha_inicio = f'{next_año}-{q_start_d}'
    fecha_fin = f'{next_año}-{q_end}'
    trimestres.append((next_año, next_q, fecha_inicio, fecha_fin))
    next_q += 1
    if next_q > 4:
        next_q = 1
        next_año += 1

print(f"Total de trimestres a evaluar: {len(trimestres)} (desde {trimestres[0][0]} Q{trimestres[0][1]} hasta {trimestres[-1][0]} Q{trimestres[-1][1]})")

# =====================================================================
# 4. SIMULACIÓN: BAJO K-RISK Y ALTO K-RISK
# =====================================================================
ventana_train_meses = 6

resultados_bajo = []
resultados_alto = []

for año, q, fecha_inicio, fecha_fin in trimestres:
    inicio_test_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_inicio_train_dt = inicio_test_dt - relativedelta(months=ventana_train_meses)
    fecha_inicio_train = fecha_inicio_train_dt.strftime('%Y-%m-%d')

    datos_train = datos[(datos.index >= fecha_inicio_train) & (datos.index < fecha_inicio)]

    if len(datos_train) < 60:
        continue

    resultados_train = []
    for ticker in tickers:
        precios = datos_train[ticker].values
        k_risk = calcular_k_risk(precios)
        peso_proxy = datos_train[ticker].iloc[-1]
        resultados_train.append({'Ticker': ticker, 'K_Risk': k_risk, 'Peso_Proxy': peso_proxy})

    df_res = pd.DataFrame(resultados_train).sort_values('K_Risk')
    mitad = len(df_res) // 2

    # BAJO: mitad inferior (menos ruido)
    cartera_bajo = df_res.head(mitad).sort_values('Peso_Proxy', ascending=False).head(5)['Ticker'].tolist()
    # ALTO: mitad superior (más ruido)
    cartera_alto = df_res.tail(mitad).sort_values('Peso_Proxy', ascending=False).head(5)['Ticker'].tolist()

    retornos_test = retornos_diarios[(retornos_diarios.index >= fecha_inicio) & (retornos_diarios.index <= fecha_fin)]
    retornos_spy_q = retornos_test[benchmark]
    rent_spy_q = (1 + retornos_spy_q).cumprod().iloc[-1] - 1

    rent_bajo_q = (1 + retornos_test[cartera_bajo].mean(axis=1)).cumprod().iloc[-1] - 1
    rent_alto_q = (1 + retornos_test[cartera_alto].mean(axis=1)).cumprod().iloc[-1] - 1

    resultado = {
        'trimestre': f'{año} Q{q}',
        'rent_spy': rent_spy_q,
        'rent_bajo': rent_bajo_q,
        'rent_alto': rent_alto_q,
        'cartera_bajo': cartera_bajo,
        'cartera_alto': cartera_alto,
        'diff_bajo': rent_bajo_q - rent_spy_q,
        'diff_alto': rent_alto_q - rent_spy_q,
    }

    resultados_bajo.append(resultado)
    resultados_alto.append(resultado)

    diff_b = resultado['diff_bajo']
    diff_a = resultado['diff_alto']
    print(f"[{año} Q{q}] SPY: {rent_spy_q*100:+.1f}% | BAJO: {rent_bajo_q*100:+.1f}% ({diff_b*100:+.1f}pp) | ALTO: {rent_alto_q*100:+.1f}% ({diff_a*100:+.1f}pp)")

# =====================================================================
# 5. CURVAS DE EQUITY
# =====================================================================
curva_bajo = pd.Series(dtype=float)
curva_alto = pd.Series(dtype=float)
curva_spy = pd.Series(dtype=float)

for r in resultados_bajo:
    mes_map = {'Q1': '01', 'Q2': '04', 'Q3': '07', 'Q4': '10'}
    q = r['trimestre'][5:]
    año = int(r['trimestre'][:4])
    fecha_inicio = f"{año}-{mes_map[q]}-01"
    q_end_map = {'Q1': '03-31', 'Q2': '06-30', 'Q3': '09-30', 'Q4': '12-31'}
    fecha_fin = f"{año}-{q_end_map[q]}"

    ret_test = retornos_diarios[(retornos_diarios.index >= fecha_inicio) & (retornos_diarios.index <= fecha_fin)]
    cartera_b = r['cartera_bajo']
    cartera_a = r['cartera_alto']
    curva_bajo = pd.concat([curva_bajo, ret_test[cartera_b].mean(axis=1)])
    curva_alto = pd.concat([curva_alto, ret_test[cartera_a].mean(axis=1)])
    curva_spy = pd.concat([curva_spy, ret_test[benchmark]])

acum_bajo = (1 + curva_bajo).cumprod() * 100
acum_alto = (1 + curva_alto).cumprod() * 100
acum_spy = (1 + curva_spy).cumprod() * 100

# =====================================================================
# 6. RESULTADOS FINALES
# =====================================================================
ret_total_bajo = (acum_bajo.iloc[-1] / 100) - 1
ret_total_alto = (acum_alto.iloc[-1] / 100) - 1
ret_total_spy = (acum_spy.iloc[-1] / 100) - 1

ganados_bajo = sum(1 for r in resultados_bajo if r['diff_bajo'] > 0)
ganados_alto = sum(1 for r in resultados_alto if r['diff_alto'] > 0)
total_q = len(resultados_bajo)

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
print(f"RESULTADOS COMPLETOS ({resultados_bajo[0]['trimestre']} - {resultados_bajo[-1]['trimestre']})")
print(f"{'='*70}")
print(f"SPY:              {ret_total_spy*100:+.2f}%  | Sharpe: {sharpe_spy:.2f} | Vol: {vol_spy:.1f}% | MaxDD: {maxdd_spy:.1f}%")
print(f"K-Risk BAJO:      {ret_total_bajo*100:+.2f}%  | Sharpe: {sharpe_bajo:.2f} | Vol: {vol_bajo:.1f}% | MaxDD: {maxdd_bajo:.1f}% | Wins: {ganados_bajo}/{total_q}")
print(f"K-Risk ALTO:      {ret_total_alto*100:+.2f}%  | Sharpe: {sharpe_alto:.2f} | Vol: {vol_alto:.1f}% | MaxDD: {maxdd_alto:.1f}% | Wins: {ganados_alto}/{total_q}")
print(f"{'='*70}")

# Por décadas
decadas_resultados = {}
for r in resultados_bajo:
    año = int(r['trimestre'][:4])
    decada = f"{(año//10)*10}s"
    if decada not in decadas_resultados:
        decadas_resultados[decada] = {'bajo': [], 'alto': [], 'spy': []}
    decadas_resultados[decada]['bajo'].append(r['rent_bajo'])
    decadas_resultados[decada]['alto'].append(r['rent_alto'])
    decadas_resultados[decada]['spy'].append(r['rent_spy'])

print("\nRendimiento por período:")
for decada, datos_d in sorted(decadas_resultados.items()):
    acum_b = (1 + pd.Series(datos_d['bajo'])).prod() - 1
    acum_a = (1 + pd.Series(datos_d['alto'])).prod() - 1
    acum_s = (1 + pd.Series(datos_d['spy'])).prod() - 1
    n = len(datos_d['spy'])
    wins_b = sum(1 for b, s in zip(datos_d['bajo'], datos_d['spy']) if b > s)
    wins_a = sum(1 for a, s in zip(datos_d['alto'], datos_d['spy']) if a > s)
    print(f"  {decada} ({n}q): SPY {acum_s*100:+.1f}% | BAJO {acum_b*100:+.1f}% ({wins_b}/{n}) | ALTO {acum_a*100:+.1f}% ({wins_a}/{n})")

# =====================================================================
# 7. GRÁFICOS
# =====================================================================
fig, axes = plt.subplots(2, 1, figsize=(16, 10))

ax1 = axes[0]
ax1.plot(acum_spy.index, acum_spy.values, label=f'SPY ({ret_total_spy*100:+.1f}%)', color='black', linewidth=2)
ax1.plot(acum_bajo.index, acum_bajo.values, label=f'K-Risk BAJO ({ret_total_bajo*100:+.1f}%)', color='blue', linewidth=1.5, alpha=0.8)
ax1.plot(acum_alto.index, acum_alto.values, label=f'K-Risk ALTO ({ret_total_alto*100:+.1f}%)', color='red', linewidth=1.5, alpha=0.8)
ax1.set_title(f'Backtest Completo K-Risk: {resultados_bajo[0]["trimestre"]} - {resultados_bajo[-1]["trimestre"]}\nRebalanceo trimestral, ventana 6 meses')
ax1.set_ylabel('Capital (Base 100)')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Tabla resumen por período
ax2 = axes[1]
ax2.axis('off')
table_data = []
for r in resultados_bajo:
    table_data.append([
        r['trimestre'],
        f"{r['rent_spy']*100:+.1f}%",
        f"{r['rent_bajo']*100:+.1f}%",
        f"{r['diff_bajo']*100:+.1f}pp",
        f"{r['rent_alto']*100:+.1f}%",
        f"{r['diff_alto']*100:+.1f}pp",
        r['cartera_alto'][0] if r['diff_alto'] > r['diff_bajo'] else r['cartera_bajo'][0]
    ])

col_labels = ['Trimestre', 'SPY', 'K-Bajo', 'Diff-B', 'K-Alto', 'Diff-A', 'Mejor']
table = ax2.table(cellText=table_data, colLabels=col_labels, loc='center',
                  cellLoc='center', colColours=['#e0e0e0']*7)
table.auto_set_font_size(False)
table.set_fontsize(7)
table.scale(1.0, 1.2)

# Color mejor columna
for i, r in enumerate(resultados_bajo):
    if r['diff_alto'] > r['diff_bajo']:
        table[(i+1, 4)].set_facecolor('#ffcccc')
    else:
        table[(i+1, 2)].set_facecolor('#cce5ff')

ax2.set_title(f'Rendimiento por trimestre | BAJO gana {ganados_bajo}/{total_q} | ALTO gana {ganados_alto}/{total_q}', fontsize=10, pad=20)

plt.tight_layout()
plt.savefig('/home/gerion/.openclaw/workspace/k_risk_full_backtest.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nGráfico guardado en /home/gerion/.openclaw/workspace/k_risk_full_backtest.png")
