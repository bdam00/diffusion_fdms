# graph_builder.py

import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# -------------------------------------------------------------
# 1) Construction du graphe GitHub
# -------------------------------------------------------------
def build_github_graph(commits, issues, comments, stars):
    G = nx.DiGraph()

    # Fusion de toutes les sources d'auteurs
    authors = set(commits["author"].dropna()) \
            | set(issues["author"].dropna()) \
            | set(comments["author"].dropna()) \
            | set(stars["author"].dropna())

    # Ajout des nœuds
    for a in authors:
        if a is not None:
            G.add_node(a)

    # ------------------------
    # Liens Commits → Issues
    # ------------------------
    issue_pairs = []
    for i, row in issues.iterrows():
        issue_author = row["author"]
        for _, c in commits.iterrows():
            if issue_author and c["author"] and issue_author != c["author"]:
                issue_pairs.append((issue_author, c["author"]))

    for a, b in issue_pairs:
        G.add_edge(a, b)

    # ------------------------
    # Liens Issues → Comments
    # ------------------------
    for _, row in comments.iterrows():
        G.add_edge(row["author"], row["issue_number"])

    # ------------------------
    # Liens Stars (utilisateur → repo)
    # ------------------------
    for _, row in stars.iterrows():
        G.add_edge(row["author"], "repo_starred")

    return G


# -------------------------------------------------------------
# 2) Visualisation simple (matplotlib)
# -------------------------------------------------------------
def show_graph_simple(G):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)

    nx.draw(G, pos, with_labels=False, node_size=50, edge_color="gray")
    plt.title("Graphe GitHub – Visualisation Simple")
    plt.show()


# -------------------------------------------------------------
# 3) Visualisation interactive Plotly (compatible Python 3.13)
# -------------------------------------------------------------
def show_graph_plotly(G):
    pos = nx.spring_layout(G, seed=42)

    # Edges
    edge_x = []
    edge_y = []
    for src, dst in G.edges():
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=1),
        hoverinfo='none'
    )

    # Nodes
    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(str(node))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        text=node_text,
        hoverinfo='text',
        marker=dict(size=8, line_width=1)
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Graph GitHub – Visualisation Interactive (Plotly)",
            title_x=0.5,
            hovermode='closest'
        )
    )

    fig.show()
    fig.write_html("graph_plotly.html")   # Fichier exporté automatiquement


# -------------------------------------------------------------
# 4) Export Gephi (GEXF)
# -------------------------------------------------------------
def export_graph_gephi(G):
    nx.write_gexf(G, "graph_export.gexf")
    print("✔ Fichier GEXF exporté : graph_export.gexf")
