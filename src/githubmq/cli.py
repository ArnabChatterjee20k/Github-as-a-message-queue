import click
from .github_manager import GithubManager

@click.group()
def cli():
    pass

@cli.command()
@click.option('--repo-url', prompt='GitHub repo URL', help='URL of the GitHub repository')
@click.option('--auth-token', prompt='GitHub access token', help='GitHub access token')
@click.option("--origin",prompt="Origin name, ex-> master,main,etc",help="enter the origin name")
def setup(repo_url, auth_token,origin="main"):
    """Setup the GitHub repo with consumers and workflows."""
    github = GithubManager(repo_url=repo_url,auth_token=auth_token,origin=origin)
    
    # Upload consumers and workflow files
    github.upload_consumer_scripts()
    github.upload_workflow_files()
    github.create_labels()
    print("Setup complete!")