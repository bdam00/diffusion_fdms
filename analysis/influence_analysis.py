import pandas as pd
import networkx as nx
import plotly.express as px

from ic_model import independent_cascade


# ============================================================
# TOP INFLUENCEURS STRUCTURELS
# ============================================================

def top_influencers(G, k=5):
    """
    Top influenceurs structurels du réseau
    """
    degree = dict(G.degree())
    betweenness = nx.betweenness_centrality(G)

    rows = []
    top_nodes = sorted(degree.items(), key=lambda x: x[1], reverse=True)[:k]

    for node, deg in top_nodes:
        rows.append({
            "node": node,
            "degree": deg,
            "betweenness": round(betweenness[node], 4)
        })

    df = pd.DataFrame(rows)

    print("\n=== Top influenceurs structurels du réseau ===")
    print(df.to_string(index=False))

    return df


# ============================================================
# STRUCTURE VS DIFFUSION
# ============================================================

def structure_vs_diffusion(G, seeds, p=0.3):
    """
    Compare centralité structurelle et diffusion réelle (IC)
    """
    degree = dict(G.degree())
    betweenness = nx.betweenness_centrality(G)

    rows = []

    for s in seeds:
        activated, _ = independent_cascade(G, s, p)

        rows.append({
            "node": s,
            "degree": degree.get(s, 0),
            "betweenness": round(betweenness.get(s, 0), 4),
            "influence_ic": len(activated)
        })

    return pd.DataFrame(rows)


def plot_structure_vs_diffusion(df):
    """
    Scatter plot : structure vs diffusion
    """
    fig = px.scatter(
        df,
        x="degree",
        y="influence_ic",
        size="betweenness",
        hover_name="node",
        title="Structure vs Diffusion (IC)",
        labels={
            "degree": "Degré",
            "influence_ic": "Nœuds activés (IC)"
        }
    )
    fig.show()
