import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# =========================================================
# LINEAR THRESHOLD MODEL
# =========================================================

def linear_threshold(G, seeds, fixed_threshold=None):

    """
    Simulation du modèle Linear Threshold (LT)

    Returns:
    - activated: set des noeuds activés
    - steps: liste des activations par étape
    - thresholds: dict {node: seuil}
    - activation_step: dict {node: étape}
    """

    # ----------------------------
    # Initialisation
    # ----------------------------
    if fixed_threshold is None:
        thresholds = {v: random.uniform(0, 1) for v in G.nodes()}
    else:
        thresholds = {v: fixed_threshold for v in G.nodes()}
    activated = set(seeds)
    activation_step = {v: 0 for v in seeds}
    steps = [set(seeds)]

    step = 0
    newly_active = set(seeds)

    # ----------------------------
    # Propagation
    # ----------------------------
    while newly_active:
        step += 1
        next_active = set()

        for v in G.nodes():
            if v in activated:
                continue

            neighbors = list(G.predecessors(v)) + list(G.successors(v))
            if not neighbors:
                continue

            active_neighbors = sum(1 for u in neighbors if u in activated)
            influence = active_neighbors / len(neighbors)

            if influence >= thresholds[v]:
                next_active.add(v)
                activation_step[v] = step

        newly_active = next_active - activated
        activated |= newly_active

        if newly_active:
            steps.append(newly_active)

    return activated, steps, thresholds, activation_step


# =========================================================
# TABLEAU FINAL CONSOLE
# =========================================================

def print_lt_summary(G, thresholds, activated, activation_step):
    rows = []

    for v in G.nodes():
        rows.append({
            "node": v,
            "degree": G.degree(v),
            "threshold": round(thresholds[v], 3),
            "activated": v in activated,
            "activation_step": activation_step.get(v, "-")
        })

    df = pd.DataFrame(rows)
    print("\n=== RÉSUMÉ LINEAR THRESHOLD ===")
    print(df.to_string(index=False))


# =========================================================
# VISUALISATION MATPLOTLIB
# =========================================================

def visualize_lt_matplotlib(G, activated, seeds):
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10, 8))

    nx.draw_networkx_nodes(
        G, pos,
        nodelist=G.nodes(),
        node_color=["red" if n in seeds else "orange" if n in activated else "lightgray" for n in G.nodes()],
        node_size=40
    )

    nx.draw_networkx_edges(G, pos, alpha=0.3)

    plt.title("Linear Threshold – propagation finale")
    plt.axis("off")
    plt.show()


# =========================================================
# VISUALISATION PLOTLY
# =========================================================

def visualize_lt_plotly(G, activated, seeds):
    pos = nx.spring_layout(G, seed=42)

    edge_x, edge_y = [], []
    for u, v in G.edges():
        edge_x += [pos[u][0], pos[v][0], None]
        edge_y += [pos[u][1], pos[v][1], None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode="lines",
        line=dict(width=0.5),
        hoverinfo="none"
    )

    node_x, node_y, colors = [], [], []
    for n in G.nodes():
        node_x.append(pos[n][0])
        node_y.append(pos[n][1])

        if n in seeds:
            colors.append("red")
        elif n in activated:
            colors.append("orange")
        else:
            colors.append("lightgray")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers",
        marker=dict(size=6, color=colors),
        text=list(G.nodes())
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(title="Linear Threshold – propagation finale")
    fig.show()
