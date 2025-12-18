import json
from github import Github
from pathlib import Path
from time import sleep

# ------------------------------------------------------
# PARAMÈTRES MODIFIABLES PAR L'ÉTUDIANT
# ------------------------------------------------------

GITHUB_TOKEN = "# PUT YOUR GITHUB API TOKEN"   # ← Mets ton token ici

MAX_COMMITS = 100               # nombre maximum de commits
MAX_ISSUES = 100                # nombre maximum d'issues
MAX_COMMENTS_PER_ISSUE = 5      # nombre max de commentaires par issue
MAX_STARS = 100                 # nombre max de stargazers

# ------------------------------------------------------
# FONCTIONS UTILES
# ------------------------------------------------------

def save_json(path, data):
    """Sauvegarde un fichier JSON avec indentation."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def try_request(request_fn, max_retries=3, wait=10):
    """Exécute une requête GitHub API avec retry automatique."""
    for attempt in range(max_retries):
        try:
            return request_fn()
        except Exception as e:
            print(f"⚠ Erreur API : {e} — nouvelle tentative dans {wait}s...")
            sleep(wait)

    print("❌ Échec après plusieurs tentatives.")
    return None


# ------------------------------------------------------
# SCRAPER PRINCIPAL
# ------------------------------------------------------

def scrape_github(repo_name: str, output_folder):
    """
    Scrape commits, issues, comments et stargazers d’un repo GitHub.
    """

    print(f"=== Scraping du repo {repo_name} ===")

    # 🔥 Correction : forcer output_folder → Path
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    # Auth GitHub
    g = Github(GITHUB_TOKEN)
    repo = try_request(lambda: g.get_repo(repo_name))

    if repo is None:
        print("❌ Impossible d'accéder au repository. Vérifie ton token.")
        return

    # ==============================
    # 📌 1. Récupération des commits
    # ==============================

    print(f"→ Récupération des commits… (max = {MAX_COMMITS})")
    commits = []
    try:
        for i, commit in enumerate(repo.get_commits()):
            if i >= MAX_COMMITS:
                break
            commits.append({
                "sha": commit.sha,
                "author": commit.author.login if commit.author else None,
                "date": commit.commit.author.date.isoformat(),
                "message": commit.commit.message
            })
    except Exception as e:
        print("⚠ Erreur commits :", e)

    # ============================
    # 📌 2. Récupération des issues
    # ============================

    print(f"→ Récupération des issues… (max = {MAX_ISSUES})")
    issues = []
    try:
        for i, issue in enumerate(repo.get_issues(state="all")):
            if i >= MAX_ISSUES:
                break
            issues.append({
                "id": issue.id,
                "number": issue.number,
                "user": issue.user.login if issue.user else None,
                "state": issue.state,
                "title": issue.title,
                "body": issue.body,
                "created_at": issue.created_at.isoformat()
            })
    except Exception as e:
        print("⚠ Erreur issues :", e)

    # ==========================================
    # 📌 3. Récupération des commentaires d’issues
    # ==========================================

    print(f"→ Récupération des commentaires… (max {MAX_COMMENTS_PER_ISSUE} par issue)")
    comments = []
    try:
        for issue in repo.get_issues(state="all")[:MAX_ISSUES]:
            c_list = issue.get_comments()
            for i, c in enumerate(c_list):
                if i >= MAX_COMMENTS_PER_ISSUE:
                    break
                comments.append({
                    "issue_number": issue.number,
                    "user": c.user.login if c.user else None,
                    "body": c.body,
                    "created_at": c.created_at.isoformat()
                })
    except Exception as e:
        print("⚠ Erreur commentaires :", e)

    # ================================
    # 📌 4. Récupération des stargazers
    # ================================

    print(f"→ Récupération des stargazers… (max = {MAX_STARS})")
    stars = []
    try:
        for i, user in enumerate(repo.get_stargazers()):
            if i >= MAX_STARS:
                break
            stars.append({
                "user": user.login,
            })
    except Exception as e:
        print("⚠ Erreur stargazers :", e)

    # =====================
    # 📁 Sauvegarde JSON
    # =====================

    save_json(output_folder / "commits.json", commits)
    save_json(output_folder / "issues.json", issues)
    save_json(output_folder / "comments.json", comments)
    save_json(output_folder / "stars.json", stars)

    # =====================
    # 📊 Récap
    # =====================

    print("\nRésumé du dataset :")
    print(" - Commits      :", len(commits))
    print(" - Issues       :", len(issues))
    print(" - Commentaires :", len(comments))
    print(" - Stars        :", len(stars))

    print(f"\n✔ Scraping terminé ! Données disponibles dans : {output_folder}\n")
