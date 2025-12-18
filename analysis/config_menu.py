import random
import networkx as nx


def configure_experiment(G):
    """
    Menu interactif pour configurer IC et LT avant analyse.
    Retourne un dictionnaire de configuration.
    """

    config = {}

    # ==================================================
    # CONFIGURATION IC
    # ==================================================
    print("\n==============================")
    print(" CONFIGURATION IC ")
    print("==============================")

    print("\nChoix des seeds IC :")
    print("1. Aléatoire")
    print("2. Degré maximal")
    seed_mode = input("Choix (1-2) : ")

    if seed_mode == "2":
        seeds_ic = sorted(G.degree, key=lambda x: x[1], reverse=True)
        seeds_ic = [n for n, _ in seeds_ic[:5]]
        seed_label = "degree"
    else:
        seeds_ic = random.sample(list(G.nodes()), 5)
        seed_label = "random"

    print("\nProbabilité IC :")
    print("1. Manuelle")
    print("2. Aléatoire")
    p_mode = input("Choix (1-2) : ")

    if p_mode == "1":
        p = float(input("Valeur de p (ex: 0.1) : "))
        p_label = f"p={p}"
    else:
        p = round(random.uniform(0.05, 0.5), 2)
        p_label = f"p~{p}"

    config["IC"] = {
        "seeds": seeds_ic,
        "p": p,
        "label": f"IC_{seed_label}_{p_label}"
    }

    # ==================================================
    # CONFIGURATION LT
    # ==================================================
    print("\n==============================")
    print(" CONFIGURATION LT ")
    print("==============================")

    k = int(input("Nombre de seeds LT : "))
    seeds_lt = random.sample(list(G.nodes()), k)

    print("\nSeuils LT :")
    print("1. Automatiques")
    print("2. Fixes")
    t_mode = input("Choix (1-2) : ")

    if t_mode == "2":
        t = float(input("Valeur du seuil (0-1) : "))
        threshold_mode = f"fixed_{t}"
    else:
        threshold_mode = "auto"

    config["LT"] = {
        "seeds": seeds_lt,
        "threshold_mode": threshold_mode,
        "label": f"LT_k{k}_{threshold_mode}"
    }

    return config
