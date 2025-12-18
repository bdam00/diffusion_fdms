import pandas as pd
import plotly.express as px

from ic_model import independent_cascade
from lt_model import linear_threshold


# ============================================================
# ANALYSE IC — Influence individuelle
# ============================================================

def analyze_ic_influence(
    G,
    seeds,
    p=0.1,
    config_label="default"
):
    results = []

    for s in seeds:
        activated, _ = independent_cascade(G, s, p)

        results.append({
            "seed": s,
            "model": "IC",
            "activated_nodes": len(activated),
            "p": p,
            "config": config_label
        })

    return pd.DataFrame(results)


# ============================================================
# ANALYSE LT — Influence collective
# ============================================================

def analyze_lt_influence(
    G,
    seeds,
    threshold_mode="auto",
    fixed_threshold=None,
    config_label="default"
):
    activated, _, thresholds, _ = linear_threshold(G, seeds)

    rows = []
    for s in seeds:
        rows.append({
            "seed": s,
            "model": "LT",
            "activated_nodes": len(activated),
            "threshold": round(thresholds[s], 3),
            "threshold_mode": threshold_mode,
            "config": config_label
        })

    return pd.DataFrame(rows)


# ============================================================
# COMPARAISON IC vs LT
# ============================================================

def compare_ic_lt(G, seeds, p=0.1):
    df_ic = analyze_ic_influence(G, seeds, p)
    df_lt = analyze_lt_influence(G, seeds)
    return pd.concat([df_ic, df_lt], ignore_index=True)


# ============================================================
# VISUALISATION — IC vs LT
# ============================================================

def plot_ic_lt_comparison(df):
    """
    Affiche un graphe comparatif IC vs LT
    (nombre de nœuds activés par seed)
    """

    fig = px.bar(
        df,
        x="seed",
        y="activated_nodes",
        color="model",
        barmode="group",
        title="Comparaison IC vs LT — Influence des seeds",
        labels={
            "activated_nodes": "Nombre de nœuds activés",
            "seed": "Seed"
        }
    )

    fig.show()
