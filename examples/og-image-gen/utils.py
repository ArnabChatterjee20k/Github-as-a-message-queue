from githubmq.github_manager import GithubManager
from dotenv import load_dotenv
import os , uuid
load_dotenv(".env")
def produce(url):
    github = GithubManager(repo_url=os.environ.get("repo_url"),
                        auth_token=os.environ.get("auth_token"))
    
    uid = str(uuid.uuid4()).split("-")[0]
    github.produce(uid,url,["scraper"])
    return uid