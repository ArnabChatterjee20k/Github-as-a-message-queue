from pathlib import Path
from .git import Git

def get_repo_name(repo_url):
    return repo_url.split('/')[-1].split(".")[0]

def clone_repo(repo_url):
    print("Cloning repo")
    repo_name = get_repo_name(repo_url)
    repo_path = Path(repo_name)
    if repo_path.exists():
        print("Already the repo is present")
        return
    Git.clone(repo_url)
    print("Repo is cloned")