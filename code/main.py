import os
import random
import sys


# ============================================================
# AJOUT DU DOSSIER RACINE AU PYTHONPATH
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


from github_scraper import scrape_github
from data_loader import load_json
from graph_builder import (
    build_github_graph,
    show_graph_simple,
    show_graph_plotly,
    export_graph_gephi
    )

from ic_model import (
    independent_cascade,
    visualize_ic_plotly
)

from lt_model import (
    linear_threshold,
    print_lt_summary,
    visualize_lt_plotly
)

# ================= ANALYSES =================
from analysis.ic_vs_lt import (
    compare_ic_lt,
    plot_ic_lt_comparison
)

from analysis.influence_analysis import (
    top_influencers,
    structure_vs_diffusion,
    plot_structure_vs_diffusion
)

from analysis.sensitivity_analysis import (
    sensitivity_ic,
    sensitivity_lt,
    plot_sensitivity
)

from analysis.config_menu import configure_experiment

DATA_DIR = "../data_github"


# ============================================================
# MENUS
# ============================================================

def choose_repo():
    repos = {
        "1": "pallets/flask",
        "2": "tensorflow/tensorflow",
        "3": "torvalds/linux",
        "4": "microsoft/vscode",
        "5": "scikit-learn/scikit-learn",
        "6": "django/django",
        "7": "pytorch/pytorch"
    }

    print("\n=== Choix du repository ===")
    for k, v in repos.items():
        print(f"{k}. {v}")

    return repos.get(input("Choix : "), "pallets/flask")


def ask_regenerate():
    return input("\nRégénérer dataset ? (o/n) : ").lower() == "o"

def choose_visualization(G):
    print("\n=== Choisissez une méthode de visualisation ===")
    print("1. Visualisation simple (matplotlib)")
    print("2. Visualisation interactive Plotly")
    print("3. Export pour Gephi (GEXF)")
    print("4. Aucune visualisation")

    choice = input("Votre choix (1-4) : ").strip()

    if choice == "1":
        show_graph_simple(G)

    elif choice == "2":
        show_graph_plotly(G)

    elif choice == "3":
        export_graph_gephi(G)

    else:
        print("➡ Aucune visualisation sélectionnée.")


def choose_model():
    print("\n=== Choix du mode ===")
    print("1. Simulation IC")
    print("2. Simulation LT")
    print("3. Analyses (IC / LT)")
    return input("Choix : ")


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n=== TP Diffusion de l'information – GitHub ===")

    repo = choose_repo()

    if ask_regenerate():
        from pathlib import Path
        scrape_github(repo, Path(DATA_DIR))
    else:
        print("✔ Dataset existant utilisé.")

    commits, issues, comments, stars = (
        load_json(os.path.join(DATA_DIR, f))
        for f in ["commits.json", "issues.json", "comments.json", "stars.json"]
    )

    for df in [issues, comments, stars]:
        if "user" in df.columns:
            df.rename(columns={"user": "author"}, inplace=True)

    G = build_github_graph(commits, issues, comments, stars)
    print(f"\nGraphe : {G.number_of_nodes()} nœuds / {G.number_of_edges()} arcs")

    choose_visualization(G)

    mode = choose_model()

    # ========================================================
    # IC
    # ========================================================
    if mode == "1":
        seed = random.choice(list(G.nodes()))
        p = float(input("Probabilité p : "))

        activated, _ = independent_cascade(G, seed, p)
        print(f"\nIC → {len(activated)} nœuds activés")
        visualize_ic_plotly(G, activated, seed)

    # ========================================================
    # LT
    # ========================================================
    elif mode == "2":
        k = int(input("Nombre de seeds : "))
        seeds = random.sample(list(G.nodes()), k)

        activated, steps, thresholds, activation_step = linear_threshold(G, seeds)
        print_lt_summary(G, thresholds, activated, activation_step)
        visualize_lt_plotly(G, activated, seeds)

    # ========================================================
    # ANALYSES
    # ========================================================
    elif mode == "3":

    # ==============================
    # Configuration interactive
    # ==============================
        config = configure_experiment(G)

        print("\nConfiguration utilisée :")
        print(config)

    # ==============================
    # Comparaison IC vs LT
    # ==============================
        df_comp = compare_ic_lt(
            G,
            seeds=config["IC"]["seeds"],
            p=config["IC"]["p"]
    )

    # Ajout des labels de config
        df_comp["config"] = df_comp["model"].apply(
            lambda m: config[m]["label"]
    )

        print("\n=== Comparaison IC vs LT ===")
        print(df_comp)

        plot_ic_lt_comparison(df_comp)

    # ==============================
    # Top influenceurs structurels
    # ==============================
        top_influencers(G, k=5)

    # ==============================
    # Analyse de sensibilité IC
    # ==============================
        seed_ic = config["IC"]["seeds"][0]
        p_values = [0.05, 0.1, 0.2, 0.3, 0.5]

        df_ic = sensitivity_ic(G, seed_ic, p_values)
        print("\n=== Sensibilité IC (p) ===")
        print(df_ic)
        plot_sensitivity(df_ic, "Effet de p sur IC")

    # ==============================
    # Analyse de sensibilité LT
    # ==============================
        thresholds = [0.1, 0.2, 0.3, 0.4, 0.5]

        df_lt = sensitivity_lt(G, config["LT"]["seeds"], thresholds)
        print("\n=== Sensibilité LT (seuils) ===")
        print(df_lt)
        plot_sensitivity(df_lt, "Effet des seuils sur LT")

    else:
        print("Choix invalide.")


if __name__ == "__main__":
    main()
