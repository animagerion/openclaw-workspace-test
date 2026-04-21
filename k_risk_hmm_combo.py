#!/usr/bin/env python3
"""
K-Risk + HMM — Walk-Forward Clean (sin look-ahead bias)
Version con features multidimensionales: returns, volumen, volatilidad, K-Risk
"""

import argparse
import warnings
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

warnings.filterwarnings('ignore')

try:
    from hmmlearn import hmm
    HAS_HMM = True
except ImportError:
    HAS_HMM = False
    print("ERROR: hmmlearn no instalado. Ejecuta: pip3 install hmmlearn")
    exit(1)


# ─── K-RISK ─────────────────────────────────────────────────────────────────

def calcular_k_risk(serie_precios, max_iter=20):
    """K-Risk original de Montojo & Rodriguez (2013). K = Lambda_total / Lambda_Theta."""
    serie_precios = np.array(serie_precios, dtype=float)
    n = len(serie_precios)
    if n < 20:
        return None
    serie_precios = serie_precios - np.mean(serie_precios)
    fft = np.fft.fft(serie_precios)
    espectro = np.abs(fft[:n//2]) ** 2
    if np.sum(espectro) == 0:
        return None
    spect_norm = espectro / np.sum(espectro)
    Theta = 2.0 * np.pi * np.arange(n//2) / n
    M1 = np.sum(Theta * spect_norm)
    M2 = np.sum(Theta**2 * spect_norm)
    Lambda_total = 2.0 * np.pi / n
    Lambda_theta = np.sqrt(max(0, M2 - M1**2))
    if Lambda_theta == 0:
        return None
    K = Lambda_total / Lambda_theta
    for _ in range(max_iter):
        f = 1.0 - np.exp(-Theta * K)
        numer = np.sum(f * spect_norm * Theta)
        denom = np.sum(f * spect_norm * Theta**2)
        if denom == 0:
            break
        K_new = numer / denom
        if abs(K_new - K) < 1e-6:
            break
        K = K_new
    return float(K)


# ─── FEATURES ────────────────────────────────────────────────────────────────

def compute_features(precios, volumenes=None, k_ventana=60):
    """
    Computa matriz de features para HMM (n-1 elementos, alineados con returns).
    Features: [returns_z, volatilidad_z, k_risk_z, volumen_ratio_z]
    """
    precios = np.array(precios, dtype=float)
    n_orig = len(precios)
    n = n_orig - 1  # returns tienen n-1

    # Returns diarios
    returns = np.diff(np.log(precios))
    ret_z = (returns - np.mean(returns)) / (np.std(returns) + 1e-10)

    # Volatilidad rolling 20d
    vol_rolling = pd.Series(returns).rolling(20, min_periods=5).std().fillna(0).values
    vol_z = (vol_rolling - np.mean(vol_rolling)) / (np.std(vol_rolling) + 1e-10)

    # K-Risk rolling (devuelve n-1 elementos)
    k_risk_arr = np.full(n, np.nan)
    for i in range(k_ventana+1, n_orig):
        kr = calcular_k_risk(precios[max(0, i-k_ventana):i])
        k_risk_arr[i-1] = kr if kr is not None and kr < 10 else np.nan
    k_z = np.zeros(n)
    k_valid = ~np.isnan(k_risk_arr)
    if k_valid.any():
        k_z[k_valid] = (k_risk_arr[k_valid] - np.mean(k_risk_arr[k_valid])) / (np.std(k_risk_arr[k_valid]) + 1e-10)

    # Volumen ratio (si disponible)
    if volumenes is not None and len(volumenes) == n_orig:
        vol_data = np.array(volumenes, dtype=float)
        vol_data = np.nan_to_num(vol_data, nan=1.0)
        vol_ma = pd.Series(vol_data).rolling(20, min_periods=5).mean().fillna(1.0).values
        vol_ratio = (vol_data / (vol_ma + 1e-10))[1:]  # alinear a n-1
        vr_z = (vol_ratio - np.mean(vol_ratio)) / (np.std(vol_ratio) + 1e-10)
    else:
        vr_z = np.zeros(n)

    # Matriz features (n-1, 4)
    X = np.column_stack([ret_z, vol_z, k_z, vr_z])
    X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    return X, returns


FEATURE_NAMES = ['Returns', 'Volatilidad', 'K-Risk', 'Volumen']


# ─── HMM ────────────────────────────────────────────────────────────────────

def train_hmm_and_signal(X_hist, n_states=2):
    """Entrena HMM con features multidimensionales. X_hist: (n, n_features)."""
    if X_hist.shape[0] < 30:
        return 0, 0, list(range(n_states)), list(range(n_states))
    model = hmm.GaussianHMM(n_components=n_states, covariance_type='full', n_iter=200, random_state=42)
    try:
        model.fit(X_hist)
        all_states = model.predict(X_hist)
        last_state = int(all_states[-1])
    except Exception:
        return 0, 0, list(range(n_states)), list(range(n_states))
    state_means = {}
    for s in range(n_states):
        mask = all_states == s
        state_means[s] = float(np.mean(X_hist[mask, 0])) if np.sum(mask) > 0 else 0.0
    sorted_states = sorted(state_means.keys(), key=lambda s: state_means[s], reverse=True)
    best_state, worst_state = sorted_states[0], sorted_states[-1]
    try:
        tomorrow_state = int(np.argmax(model.transmat_[last_state]))
    except Exception:
        tomorrow_state = last_state
    if tomorrow_state == best_state and state_means[best_state] > 0.05:
        signal = 1
    elif tomorrow_state == worst_state and state_means[worst_state] < -0.05:
        signal = -1
    else:
        signal = 0
    return signal, tomorrow_state, best_state, worst_state


# ─── WALK-FORWARD ───────────────────────────────────────────────────────────

def walk_forward_krisk_hmm(data_df, k_ventana=60, k_umbral=2.0,
                            train_min=252, retest_every=21,
                            reducir_alto=True, hmm_estados=2,
                            feature_set=None):
    """
    Walk-forward con HMM multidimensional.
    feature_set: lista de indices o None para todas.
    """
    precios_raw = data_df['Close'].values
    if precios_raw.ndim == 2 and precios_raw.shape[1] == 1:
        precios = precios_raw.flatten()
    else:
        precios = np.array(precios_raw, dtype=float)
    vol_raw = data_df['Volume'].values if 'Volume' in data_df.columns else None
    if vol_raw is not None and vol_raw.ndim == 2 and vol_raw.shape[1] == 1:
        volumenes = vol_raw.flatten()
    else:
        volumenes = vol_raw

    X_full, returns_full = compute_features(precios, volumenes, k_ventana)
    n_total = len(returns_full)

    # K-Risk full para filtro
    k_risk_full = np.full(n_total, np.nan)
    for i in range(k_ventana+1, len(precios)):
        kr = calcular_k_risk(precios[max(0, i-k_ventana):i])
        k_risk_full[i-1] = kr if kr is not None and kr < 10 else np.nan

    # Filtrar features
    if feature_set is not None:
        X_full = X_full[:, feature_set]

    signals, k_risk_vals, estados, positions = [], [], [], []
    pos = 0

    for t in range(n_total):
        if t < train_min:
            signals.append(0); k_risk_vals.append(np.nan); estados.append(-1); positions.append(0); continue

        kr = k_risk_full[t]
        k_risk_vals.append(kr)
        X_hist = X_full[max(0, t-train_min):t]

        if t % retest_every == 0 or t == train_min:
            sig, estado, _, _ = train_hmm_and_signal(X_hist, n_states=hmm_estados)
        else:
            sig = signals[-1] if signals else 0
            estado = estados[-1] if estados else 0

        signals.append(sig); estados.append(estado)
        pos = int(sig * 0.5) if (not np.isnan(kr) and kr > k_umbral and reducir_alto) else sig if not np.isnan(kr) else pos
        positions.append(pos)

    df = pd.DataFrame({'returns': returns_full, 'k_risk': k_risk_vals,
                        'hmm_state': estados, 'signal_raw': signals, 'position': positions})
    df['strategy_returns'] = df['position'].shift(1) * df['returns']
    return df


# ─── BACKTEST ────────────────────────────────────────────────────────────────

def backtest_wf(df, nombre=''):
    df = df.dropna(subset=['strategy_returns'])
    if len(df) == 0:
        print("Sin datos"); return df
    ret_total = (1 + df['returns']).prod() - 1
    ret_strat = (1 + df['strategy_returns']).prod() - 1
    vol = df['returns'].std() * np.sqrt(252)
    vol_s = df['strategy_returns'].std() * np.sqrt(252)
    sharpe = ret_strat / vol_s if vol_s > 0 else 0
    sharpe_bnh = ret_total / vol if vol > 0 else 0
    cumret = (1 + df['strategy_returns'].fillna(0)).cumprod()
    dd = ((cumret - cumret.expanding().max()) / cumret.expanding().max()).min()
    pct = (df['position'].abs() > 0).mean() * 100
    print(f"\n{'='*55}")
    print(f"{nombre}")
    print(f"{'='*55}")
    print(f"Periodo: {len(df)/252:.1f} anyos ({len(df)} dias)")
    print(f"\n{'Metric':<22} {'Buy&Hold':>12} {'Estrategia':>12}")
    print("-"*48)
    print(f"{'Return total':<22} {ret_total*100:>11.1f}% {ret_strat*100:>11.1f}%")
    print(f"{'Return anualizado':<22} {ret_total/len(df)*252*100:>11.1f}% {ret_strat/len(df)*252*100:>11.1f}%")
    print(f"{'Sharpe ratio':<22} {sharpe_bnh:>12.2f} {sharpe:>12.2f}")
    print(f"{'Max Drawdown':<22} {'':>12} {dd*100:>11.1f}%")
    print(f"\n  vs B&H: {(ret_strat-ret_total)*100:+.1f}pp | Sharpe diff: {sharpe-sharpe_bnh:+.2f}")
    print(f"  Tiempo activo: {pct:.0f}%")
    return df


# ─── FEATURE IMPORTANCE ──────────────────────────────────────────────────────

def feature_importance(data_df, k_ventana, train_min, retest_every, hmm_estados, k_umbral):
    print(f"\n{'='*65}")
    print("FEATURE IMPORTANCE")
    print(f"{'='*65}")
    print(f"{'Feature':<18} {'Return':>10} {'Sharpe':>8} {'MaxDD':>9} {'Activo':>7}")
    print("-"*65)

    resultados = {}

    for i, name in enumerate(FEATURE_NAMES):
        df = walk_forward_krisk_hmm(data_df, k_ventana=k_ventana, k_umbral=k_umbral,
                                     train_min=train_min, retest_every=retest_every,
                                     hmm_estados=hmm_estados, feature_set=[i])
        df = df.dropna(subset=['strategy_returns'])
        ret = (1 + df['strategy_returns']).prod() - 1
        vol = df['strategy_returns'].std() * np.sqrt(252)
        sh = ret / vol if vol > 0 else 0
        cr = (1 + df['strategy_returns'].fillna(0)).cumprod()
        dd = ((cr - cr.expanding().max()) / cr.expanding().max()).min()
        pct = (df['position'].abs() > 0).mean() * 100
        resultados[name] = (ret, sh, dd, pct)
        marker = ' ***' if sh > 3 else ''
        print(f"{name:<18} {ret*100:>9.1f}% {sh:>8.2f} {dd*100:>8.1f}% {pct:>6.0f}%{marker}")

    # Todas
    df_all = walk_forward_krisk_hmm(data_df, k_ventana=k_ventana, k_umbral=k_umbral,
                                     train_min=train_min, retest_every=retest_every,
                                     hmm_estados=hmm_estados, feature_set=None)
    df_all = df_all.dropna(subset=['strategy_returns'])
    ret_a = (1 + df_all['strategy_returns']).prod() - 1
    vol_a = df_all['strategy_returns'].std() * np.sqrt(252)
    sh_a = ret_a / vol_a if vol_a > 0 else 0
    cr_a = (1 + df_all['strategy_returns'].fillna(0)).cumprod()
    dd_a = ((cr_a - cr_a.expanding().max()) / cr_a.expanding().max()).min()
    pct_a = (df_all['position'].abs() > 0).mean() * 100
    resultados['ALL (4)'] = (ret_a, sh_a, dd_a, pct_a)
    print(f"{'ALL (4 features)':<18} {ret_a*100:>9.1f}% {sh_a:>8.2f} {dd_a*100:>8.1f}% {pct_a:>6.0f}% <<")

    # B&H
    ret_b = (1 + df_all['returns']).prod() - 1
    vol_b = df_all['returns'].std() * np.sqrt(252)
    sh_b = ret_b / vol_b if vol_b > 0 else 0
    print(f"{'Buy&Hold':<18} {ret_b*100:>9.1f}% {sh_b:>8.2f}")
    resultados['B&H'] = (ret_b, sh_b, None, 100)

    return resultados


# ─── PLOT ───────────────────────────────────────────────────────────────────

def plot_evolution(df, ticker, k_umbral, dates=None, output_path='/tmp/krisk_hmm.png'):
    df_plot = df.copy()
    if dates is not None and len(dates) >= len(df_plot):
        df_plot.index = dates[-len(df_plot):]
    else:
        df_plot.index = range(len(df_plot))

    fig, axes = plt.subplots(4, 1, figsize=(16, 14), sharex=True,
                               gridspec_kw={'height_ratios': [3, 3, 1.5, 1.5]})

    ax1 = axes[0]
    cumret_bnh = (1 + df_plot['returns']).cumprod() * 100
    cumret_strat = (1 + df_plot['strategy_returns'].fillna(0)).cumprod() * 100
    ax1.plot(df_plot.index, cumret_bnh, label='Buy&Hold', color='gray', linewidth=1.5, alpha=0.8)
    ax1.plot(df_plot.index, cumret_strat, label=f'Estrategia (K<{k_umbral})', color='blue', linewidth=1.5)
    ax1.set_ylabel('Indice (base 100)')
    ax1.set_title(f'{ticker} — K-Risk + HMM Multifeature (walk-forward, sin look-ahead bias)')
    ax1.legend(loc='upper left'); ax1.grid(True, alpha=0.3); ax1.set_yscale('log')

    ax2 = axes[1]
    price_norm = df_plot['returns'].cumsum() * 100 + 100
    ax2.plot(df_plot.index, price_norm, color='black', linewidth=1, alpha=0.7)
    states = df_plot['hmm_state'].values
    for sv in sorted(set(s for s in states if s >= 0)):
        mask = states == sv
        if mask.any():
            ax2.fill_between(df_plot.index, price_norm.min()*0.95, price_norm.max()*1.05,
                           where=mask, alpha=0.25, label=f'Estado {sv}')
    ax2.set_ylabel('Precio norm.'); ax2.legend(loc='upper left', ncol=3); ax2.grid(True, alpha=0.3)

    ax3 = axes[2]
    kr_p = df_plot['k_risk'].where(df_plot['k_risk'] < 10)
    ax3.plot(df_plot.index, kr_p, color='purple', linewidth=0.8, alpha=0.8)
    ax3.axhline(y=k_umbral, color='red', linestyle='--', linewidth=1.5, label=f'Umbral={k_umbral}')
    ax3.axhline(y=1.0, color='green', linestyle=':', linewidth=1, alpha=0.7, label='K=1.0')
    ax3.set_ylabel('K-Risk'); ax3.set_title('K-Risk'); ax3.legend(loc='upper right'); ax3.grid(True, alpha=0.3)

    ax4 = axes[3]
    ax4.plot(df_plot.index, df_plot['position'], color='darkblue', linewidth=0.8)
    ax4.axhline(y=0, color='black', linewidth=0.5)
    ax4.axhline(y=1, color='green', linestyle='--', alpha=0.5)
    ax4.axhline(y=-1, color='red', linestyle='--', alpha=0.5)
    ax4.set_ylabel('Posicion'); ax4.set_xlabel('Fecha'); ax4.set_title('Posicion'); ax4.grid(True, alpha=0.3)
    ax4.set_ylim(-1.5, 1.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"\nGrafico: {output_path}")
    return output_path


# ─── MAIN ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='K-Risk + HMM Multifeature Walk-Forward')
    p.add_argument('--ticker', default='SPY')
    p.add_argument('--start', default='2008-01-01')
    p.add_argument('--end', default='2020-01-01')
    p.add_argument('--k-ventana', type=int, default=40)
    p.add_argument('--k-umbral', type=float, default=2.0)
    p.add_argument('--train-min', type=int, default=180)
    p.add_argument('--retest-every', type=int, default=10)
    p.add_argument('--hmm-estados', type=int, default=3)
    p.add_argument('--no-feature-importance', action='store_true')
    args = p.parse_args()

    print(f"\n{'#'*60}")
    print(f"# {args.ticker} — K-Risk + HMM Multifeature")
    print(f"# Periodo: {args.start} a {args.end}")
    print(f"# Features: Returns + Volatilidad + K-Risk + Volumen")
    print(f"# HMM estados: {args.hmm_estados}")
    print(f"{'#'*60}")

    data = yf.download(args.ticker, start=args.start, end=args.end, progress=False)
    if data.empty:
        print(f"ERROR: sin datos"); exit(1)

    if not args.no_feature_importance:
        feature_importance(data, k_ventana=args.k_ventana, train_min=args.train_min,
                           retest_every=args.retest_every, hmm_estados=args.hmm_estados,
                           k_umbral=args.k_umbral)

    df = walk_forward_krisk_hmm(data, k_ventana=args.k_ventana, k_umbral=args.k_umbral,
                                 train_min=args.train_min, retest_every=args.retest_every,
                                 hmm_estados=args.hmm_estados, feature_set=None)
    backtest_wf(df, f"{args.ticker} WF (3 estados, umbral={args.k_umbral})")

    dates = pd.to_datetime(data.index)
    output = f'/tmp/{args.ticker}_krisk_hmm_mf.png'
    plot_evolution(df, args.ticker, args.k_umbral, dates=dates, output_path=output)
