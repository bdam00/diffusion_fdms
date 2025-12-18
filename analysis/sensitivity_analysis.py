import pandas as pd
import plotly.express as px

from ic_model import independent_cascade
from lt_model import linear_threshold


# ============================================================
# SENSIBILITÉ IC — effet de p
# ============================================================

def sensitivity_ic(G, seed, p_values):
    """
    Analyse de sensibilité du paramètre p (IC)
    """
    rows = []

    for p in p_values:
        activated, steps = independent_cascade(G, seed, p)
        rows.append({
            "model": "IC",
            "parameter": "p",
            "value": p,
            "activated_nodes": len(activated),
            "steps": len(steps)
        })

    return pd.DataFrame(rows)


# ============================================================
# SENSIBILITÉ LT — effet des seuils
# ============================================================

def sensitivity_lt(G, seeds, threshold_values):
    """
    Analyse de sensibilité des seuils (LT)
    """
    rows = []

    for t in threshold_values:
        activated, steps, _, _ = linear_threshold(G, seeds)

        rows.append({
            "model": "LT",
            "parameter": "threshold",
            "value": t,
            "activated_nodes": len(activated),
            "steps": len(steps)
        })

    return pd.DataFrame(rows)


# ============================================================
# VISUALISATION SENSIBILITÉ
# ============================================================

def plot_sensitivity(df, title):
    """
    Courbe de sensibilité
    """
    fig = px.line(
        df,
        x="value",
        y="activated_nodes",
        markers=True,
        title=title
    )
    fig.show()
