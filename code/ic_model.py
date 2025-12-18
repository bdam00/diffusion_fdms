import random
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# =====================================================================
# 🧠 1. SIMULATION INDEPENDENT CASCADE (IC)
# =====================================================================

def independent_cascade(G, seed, p=0.1, max_steps=20):
    """
    Modèle IC classique.
    G : graphe NetworkX
    seed : nœud initial
    p : probabilité d’influence
    Retour :
      activated_nodes : set() de tous les nœuds activés
      steps : liste des couches (activation par étape)
    """
    active = {seed}
    newly_active = {seed}
    all_steps = [list(newly_active)]

    for step in range(max_steps):
        next_active = set()

        for node in newly_active:
            for neighbor in G.neighbors(node):
                if neighbor not in active:
                    if random.random() < p:
                        next_active.add(neighbor)

        if not next_active:
            break

        active |= next_active
        newly_active = next_active
        all_steps.append(list(next_active))

    return active, all_steps



# =====================================================================
# 🎨 2. VISUALISATION MATPLOTLIB (statique)
# =====================================================================

def visualize_ic_matplotlib(G, activated, seed):
    pos = nx.spring_layout(G, seed=42)

    colors = []
    for n in G.nodes():
        if n == seed:
            colors.append("red")
        elif n in activated:
            colors.append("orange")
        else:
            colors.append("lightgray")

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, node_color=colors, with_labels=False, node_size=60)
    plt.title("Propagation IC (Matplotlib)")
    plt.show()



# =====================================================================
# 🌐 3. VISUALISATION PLOTLY (interactive)
# =====================================================================

def visualize_ic_plotly(G, activated, seed):
    pos = nx.spring_layout(G, seed=42)

    x_nodes = [pos[n][0] for n in G.nodes()]
    y_nodes = [pos[n][1] for n in G.nodes()]

    node_colors = []
    for n in G.nodes():
        if n == seed:
            node_colors.append("red")
        elif n in activated:
            node_colors.append("orange")
        else:
            node_colors.append("lightgray")

    # Edges
    edge_x, edge_y = [], []
    for u, v in G.edges():
        edge_x += [pos[u][0], pos[v][0], None]
        edge_y += [pos[u][1], pos[v][1], None]

    fig = go.Figure()

    # lignes
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode="lines",
        line=dict(width=0.5, color="gray"),
        hoverinfo="none"
    ))

    # noeuds
    fig.add_trace(go.Scatter(
        x=x_nodes,
        y=y_nodes,
        mode="markers",
        marker=dict(size=8, color=node_colors),
        text=[str(n) for n in G.nodes()],
        hoverinfo="text"
    ))

    fig.update_layout(
        title="Propagation IC – Plotly Interactive",
        width=900,
        height=700,
        showlegend=False,
        plot_bgcolor="white"
    )

    fig.show()



# =====================================================================
# 🎬 4. ANIMATION PLOTLY étape par étape (nouveau)
# =====================================================================

def animate_ic_plotly(G, steps, seed):
    """
    steps : liste [étape1, étape2, ...] contenant les noeuds activés par step.
    """

    pos = nx.spring_layout(G, seed=42)

    # Coordonnées des noeuds
    all_x = [pos[n][0] for n in G.nodes()]
    all_y = [pos[n][1] for n in G.nodes()]
    labels = list(G.nodes())

    # Coordonnées des arêtes
    edge_x, edge_y = [], []
    for u, v in G.edges():
        edge_x += [pos[u][0], pos[v][0], None]
        edge_y += [pos[u][1], pos[v][1], None]

    # Couleur initiale (seed rouge uniquement)
    current_colors = ["red" if n == seed else "lightgray" for n in G.nodes()]

    # ================================
    # 🎞 FRAMES DE L’ANIMATION
    # ================================
    frames = []
    activated_set = set([seed])

    for step_nodes in steps:
        # Mettre en orange les nœuds activés à cette étape
        for n in step_nodes:
            activated_set.add(n)

        frame_colors = []
        for n in G.nodes():
            if n == seed:
                frame_colors.append("red")
            elif n in activated_set:
                frame_colors.append("orange")
            else:
                frame_colors.append("lightgray")

        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=all_x,
                        y=all_y,
                        mode="markers",
                        marker=dict(size=8, color=frame_colors),
                        text=labels,
                        hoverinfo="text"
                    )
                ],
                name=f"step_{len(frames)}"
            )
        )

    # ================================
    # 🎨 FIGURE FINALE AVEC SLIDER
    # ================================
    fig = go.Figure(
        data=[
            # edges
            go.Scatter(
                x=edge_x, y=edge_y,
                mode="lines",
                line=dict(width=0.5, color="gray"),
                hoverinfo="none"
            ),
            # initial nodes
            go.Scatter(
                x=all_x, y=all_y,
                mode="markers",
                marker=dict(size=8, color=current_colors),
                text=labels,
                hoverinfo="text"
            )
        ],
        layout=go.Layout(
            title="Animation IC – Plotly",
            width=900,
            height=700,
            showlegend=False,
            plot_bgcolor="white",
            updatemenus=[dict(
                type="buttons",
                showactive=True,
                buttons=[
                    dict(label="▶ Play",
                        method="animate",
                        args=[None, {"frame": {"duration": 600, "redraw": True}}]
                    ),
                    dict(label="⏸ Pause",
                        method="animate",
                        args=[[None], {"frame": {"duration": 0, "redraw": False}}]
                    )
                ]
            )]
        ),
        frames=frames
    )

    fig.show()
