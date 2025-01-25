import os, shutil
from pathlib import Path
import importlib.resources as pkg_resources
from .utils import get_repo_name,clone_repo
from .git import Git
from urllib.parse import urlparse
from github import Github
from github.GithubException import UnknownObjectException
class GithubManager:
    # ideally the auth_token will be set through env variable or github secrets
    def __init__(self,auth_token,repo_url,origin="master"):
        self.auth_token = auth_token
        self.repo_url = repo_url
        self.origin = origin
        self.repo_name = get_repo_name(self.repo_url)
        clone_repo(self.repo_url)

    def create_labels(self):
        repo_name = urlparse(self.repo_url).path.strip('/').split(".")[0]
        github = Github(self.auth_token)
        repo = github.get_repo(repo_name)
        consumers_dir = "consumers"
        if not Path(consumers_dir).exists():
            raise Exception("Create consumers directory. ex-> consumers/label_name/main.py")
        for folder in os.listdir(consumers_dir):
            # labels are the folder names only
            # and not if individual files are present
            folder_path = os.path.join(consumers_dir,folder)
            if os.path.isdir(folder_path):
                try:
                    repo.get_label(folder) # will throw error if not exists so create that
                except UnknownObjectException as e:
                    repo.create_label(name=folder,color="f1c40f")
                    pass
    def upload_consumer_scripts(self):
        """
            Workflow:
            each consumer is mapped to a label.
            And each consumer resides in a folder <label> 
            example -> consumer/sentiment_calculate/main.py
            when an issue sentiment_calculate is published the main.py would be called
        """
        consumers_dir = "consumers"
        if not Path(consumers_dir).exists():
            raise Exception("Create consumers directory. ex-> consumers/label_name/main.py")
        repo_consumers_dir = f"{self.repo_name}/consumers"
        os.makedirs(os.path.dirname(repo_consumers_dir), exist_ok=True)
        shutil.copytree(consumers_dir,repo_consumers_dir,dirs_exist_ok=True)
        os.chdir(self.repo_name)
        Git.push(self.origin,commit_message="Updated the consumer scripts")
        # needed for concurrent usage
        # otherwise when some other path opertion is performed in some other functions as well they will work in the repo dir
        os.chdir("..")

    def upload_workflow_files(self):
        """
            update the workflow file
        """
        current_package = __name__.split('.')[0]
        workflows_dir = pkg_resources.files(current_package).joinpath("workflows")
        repo_workflows_dir = os.path.join(self.repo_name, '.github', 'workflows')
        os.makedirs(repo_workflows_dir,exist_ok=True)
        shutil.copytree(workflows_dir,repo_workflows_dir,dirs_exist_ok=True)
        os.chdir(self.repo_name)
        Git.push(self.origin,"updated workflows")
        os.chdir("..")