import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings

warnings.filterwarnings('ignore')

# =====================================================================
# NÚCLEO: IMPLEMENTACIÓN DEL ALGORITMO K-RISK (Según el paper)
# =====================================================================
def calcular_k_risk(serie_temporal):
    """
    Calcula la métrica de complejidad K basándose en el modelado iterativo
    de Fourier y la Ganancia Explicativa descrita por Montojo y Rodríguez.
    """
    N = len(serie_temporal)
    if N < 4:
        return np.nan

    y = np.array(serie_temporal)
    # Centrar la serie
    y = y - np.mean(y)
    TSS = np.sum(y**2) # Total Sum of Squares

    if TSS == 0:
        return 1.0 # Complejidad mínima (línea recta plana)

    # 1. Transformada Discreta de Fourier (DFT)
    fft_coeffs = np.fft.fft(y)
    amplitudes = np.abs(fft_coeffs)

    mitad_n = N // 2

    # Ordenar las frecuencias por su amplitud (mayor a menor) para optimizar el ajuste
    # Solo miramos la mitad positiva del espectro
    idx_ordenados = np.argsort(amplitudes[1:mitad_n+1])[::-1] + 1

    G_p = [] # Bondad del ajuste por parámetro invertido

    # 2. Modelado iterativo añadiendo componentes (p)
    for p in range(1, mitad_n + 1):
        mask = np.zeros(N, dtype=bool)
        mask[0] = True # Mantener siempre el componente DC (media, que aquí es 0)

        # Añadir las mejores 'p' frecuencias
        for i in range(p):
            idx = idx_ordenados[i]
            mask[idx] = True
            if idx != N - idx: # Simetría para la IFFT real
                mask[N - idx] = True

        # Reconstruir la señal (IDFT)
        espectro_filtrado = np.zeros(N, dtype=complex)
        espectro_filtrado[mask] = fft_coeffs[mask]
        reconstruccion = np.real(np.fft.ifft(espectro_filtrado))

        # Calcular el ajuste (R^2 equivalente a RSS/TSS)
        RSS = np.sum((y - reconstruccion)**2)
        r_cuadrado = 1 - (RSS / TSS)
        G_p.append(max(0.0, r_cuadrado)) # Evitar R2 negativos por errores de coma flotante

    G_p = np.array(G_p)

    # 3. Enumeración Trivial T(p)
    # Función lineal desde 0 hasta 1
    p_array = np.arange(1, mitad_n + 1)
    T_p = p_array / mitad_n

    # 4. Cálculo de la Ganancia Explicativa (Lambda)
    ganancia = G_p - T_p
    Lambda = np.sum(ganancia) # Integral discreta

    # Ganancia máxima posible (cuando G_p es siempre 1)
    Lambda_Theta = np.sum(1 - T_p)

    # Cálculo final de K (Si Lambda es <= 0, no hay ganancia, complejidad tiende a infinito)
    if Lambda <= 0:
        return 100.0 # Tope arbitrario para representar "caos absoluto"

    K = Lambda_Theta / Lambda
    return K

# =====================================================================
# FASE 1: PRUEBAS CON DATOS SINTÉTICOS (Sanity Checks)
# =====================================================================
def fase_1_datos_sinteticos():
    print("--- FASE 1: CALIBRACIÓN CON DATOS SINTÉTICOS ---")
    x = np.linspace(0, 10, 200)

    recta = x
    senoidal = np.sin(x * np.pi)
    random_walk = np.cumsum(np.random.randn(200))
    ruido_blanco = np.random.randn(200)

    print(f"K-Risk (Línea Recta): {calcular_k_risk(recta):.4f} (Ideal: ~1.0)")
    print(f"K-Risk (Onda Senoidal): {calcular_k_risk(senoidal):.4f} (Ideal: bajo, cercano a 1)")
    print(f"K-Risk (Paseo Aleatorio): {calcular_k_risk(random_walk):.4f} (Ideal: medio)")
    print(f"K-Risk (Ruido Blanco): {calcular_k_risk(ruido_blanco):.4f} (Ideal: muy alto)\n")

# =====================================================================
# FASE 1b: SENSIBILIDAD AL RUIDO
# =====================================================================
def fase_1b_sensibilidad_ruido():
    print("--- FASE 1b: SENSIBILIDAD DEL K-RISK AL RUIDO INYECTADO ---")
    x = np.linspace(0, 10, 200)
    niveles_ruido = np.linspace(0, 2, 20)
    k_valores = []
    for ruido in niveles_ruido:
        senal_sucia = np.sin(x * np.pi) + (np.random.randn(200) * ruido)
        k_valores.append(calcular_k_risk(senal_sucia))

    plt.figure(figsize=(8, 4))
    plt.plot(niveles_ruido, k_valores, marker='o', color='blue')
    plt.title('Fase 1b: Sensibilidad del K-Risk al Ruido Blanco')
    plt.xlabel('Amplitud del Ruido Inyectado')
    plt.ylabel('Valor K-Risk Calculado')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('/tmp/k_risk_sensibilidad_ruido.png', dpi=150)
    plt.close()
    print("Gráfico guardado en /tmp/k_risk_sensibilidad_ruido.png")


# =====================================================================
# FASE 2: APLICACIÓN FINANCIERA (S&P 500)
# =====================================================================
def fase_2_mercado_financiero():
    print("--- FASE 2: APLICACIÓN EN MERCADOS FINANCIEROS (S&P 500) ---")
    print("Descargando datos de Yahoo Finance...")
    # Descargar datos del SPY (ETF del S&P 500) de los últimos 5 años
    spy = yf.download('SPY', start='2018-01-01', end='2023-01-01', progress=False)
    precios = spy['Close'].values.flatten()  # Asegurar que es un array 1D
    fechas = spy.index

    ventana = 30  # Ventana móvil de 30 días
    k_risk_historico = [np.nan] * ventana
    volatilidad_historica = [np.nan] * ventana

    print(f"Calculando K-Risk rodante (ventana de {ventana} días)... esto puede tardar unos segundos.")
    for i in range(ventana, len(precios)):
        segmento = precios[i-ventana:i]
        # Volatilidad tradicional (Desviación estándar de los retornos)
        retornos = np.diff(segmento) / segmento[:-1]
        volatilidad_historica.append(np.std(retornos))

        # Métrica K-Risk
        k_risk_historico.append(calcular_k_risk(segmento))

    spy['K_Risk'] = k_risk_historico
    spy['Volatilidad'] = volatilidad_historica

    # Normalizamos ambas métricas para compararlas en el mismo gráfico
    spy['K_Risk_Norm'] = (spy['K_Risk'] - spy['K_Risk'].mean()) / spy['K_Risk'].std()
    spy['Vol_Norm'] = (spy['Volatilidad'] - spy['Volatilidad'].mean()) / spy['Volatilidad'].std()

    correlacion = spy[['K_Risk', 'Volatilidad']].corr().iloc[0, 1]
    print(f"Correlación entre K-Risk y Volatilidad Tradicional: {correlacion:.4f}")

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(fechas, precios, color='black', label='Precio SPY')
    ax1.set_ylabel('Precio ($)')
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.plot(fechas, spy['K_Risk_Norm'], color='red', alpha=0.6, label='K-Risk (Normalizado)')
    ax2.plot(fechas, spy['Vol_Norm'], color='blue', alpha=0.6, label='Volatilidad (Normalizada)')
    ax2.set_ylabel('Métricas de Riesgo (Z-Score)')
    ax2.legend(loc='upper right')

    plt.title('Fase 2: K-Risk vs Volatilidad (S&P 500)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('/tmp/k_risk_vs_volatilidad.png', dpi=150)
    plt.close()
    print("Gráfico guardado en /tmp/k_risk_vs_volatilidad.png")


# =====================================================================
# FASE 3: RECONOCIMIENTO DE PATRONES EN IA
# =====================================================================
def fase_3_reconocimiento_patrones():
    print("--- FASE 3: UTILIDAD PARA MACHINE LEARNING (IA) ---")
    print("Generando dataset de clasificación binaria (Onda vs Ruido)...")

    X_features = []
    y_labels = []

    # Generar 500 muestras
    for _ in range(500):
        es_onda = np.random.choice([True, False])
        if es_onda:
            # Clase 1: Onda con ruido
            senal = np.sin(np.linspace(0, 4*np.pi, 50)) + np.random.randn(50) * 1.5
            etiqueta = 1
        else:
            # Clase 0: Ruido puro
            senal = np.random.randn(50) * 2.0
            etiqueta = 0

        volatilidad = np.std(senal)
        rango = np.max(senal) - np.min(senal)
        k_risk = calcular_k_risk(senal)

        X_features.append([volatilidad, rango, k_risk])
        y_labels.append(etiqueta)

    X_features = np.array(X_features)
    y_labels = np.array(y_labels)

    X_train, X_test, y_train, y_test = train_test_split(X_features, y_labels, test_size=0.3, random_state=42)

    # Entrenar modelo SIN K-Risk (solo Volatilidad y Rango)
    clf_base = RandomForestClassifier(random_state=42)
    clf_base.fit(X_train[:, :2], y_train)
    acc_base = accuracy_score(y_test, clf_base.predict(X_test[:, :2]))

    # Entrenar modelo CON K-Risk
    clf_k = RandomForestClassifier(random_state=42)
    clf_k.fit(X_train, y_train)
    acc_k = accuracy_score(y_test, clf_k.predict(X_test))

    print(f"Precisión (Accuracy) del modelo SIN K-Risk: {acc_base*100:.2f}%")
    print(f"Precisión (Accuracy) del modelo CON K-Risk: {acc_k*100:.2f}%")

    # Feature importance del modelo completo
    print(f"Importancia de características: Volatilidad={clf_k.feature_importances_[0]:.3f}, "
          f"Rango={clf_k.feature_importances_[1]:.3f}, K-Risk={clf_k.feature_importances_[2]:.3f}\n")


# =====================================================================
# FASE 4: SENSIBILIDAD AL TAMAÑO DE LA MUESTRA
# =====================================================================
def fase_4_limites_computacionales():
    print("--- FASE 4: SENSIBILIDAD AL TAMAÑO DE LA MUESTRA (N) ---")

    serie_larga = np.cumsum(np.random.randn(1000))  # Random Walk de 1000 periodos

    k_total = calcular_k_risk(serie_larga)

    # Cortar en 10 trozos de 100
    trozos = np.array_split(serie_larga, 10)
    k_trozos = [calcular_k_risk(trozo) for trozo in trozos]
    k_promedio = np.mean(k_trozos)

    print(f"K-Risk analizando la serie completa (N=1000): {k_total:.4f}")
    print(f"Promedio de K-Risk analizando 10 sub-series (N=100): {k_promedio:.4f}")
    diferencia = abs(k_total - k_promedio) / k_total * 100
    print(f"Diferencia porcentual por fragmentación: {diferencia:.2f}%")
    if diferencia > 15:
        print("AVISO: La diferencia es alta (>15%), el indicador no es fractalmente robusto.")
    else:
        print("OK: La diferencia es aceptable, el indicador es razonablemente robusto ante cambios de escala.")
    print()


# =====================================================================
# EJECUCIÓN PRINCIPAL
# =====================================================================
if __name__ == "__main__":
    print("Iniciando batería de pruebas para el Algoritmo K-Risk...")
    print("=" * 60)
    fase_1_datos_sinteticos()
    fase_1b_sensibilidad_ruido()
    fase_2_mercado_financiero()
    fase_3_reconocimiento_patrones()
    fase_4_limites_computacionales()
    print("=" * 60)
    print("Pruebas finalizadas con éxito.")
