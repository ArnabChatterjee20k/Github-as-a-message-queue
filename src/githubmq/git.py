import subprocess
class Git:
    def clone(repo_url):
        subprocess.run(["git","clone",repo_url])
    
    def push(origin,commit_message="Updates"):
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", commit_message])
        subprocess.run(["git", "push","origin",origin],check=True)