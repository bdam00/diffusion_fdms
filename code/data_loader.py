import pandas as pd
from pathlib import Path

def load_json(path):
    p = Path(path)
    if not p.exists():
        print(f"⚠ Le fichier {p} n'existe pas → un DataFrame vide sera retourné.")
        return pd.DataFrame()
    return pd.read_json(p, orient="records")
