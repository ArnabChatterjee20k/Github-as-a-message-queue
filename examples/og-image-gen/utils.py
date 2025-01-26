from githubmq.github_manager import GithubManager
from dotenv import load_dotenv
import os , uuid
load_dotenv(".env")
def produce(uid,url):
    github = GithubManager(repo_url=os.environ.get("repo_url"),
                        auth_token=os.environ.get("auth_token"))
    
    github.produce(uid,url,["scraper"])
    return uid

import hashlib

def generate_url_hash(url: str) -> str:
    """
    Generate a consistent 6-character hash for a given URL.

    Args:
        url (str): The input URL.

    Returns:
        str: A 6-character hash.
    """
    # Hash the URL using sha256
    hash_object = hashlib.sha256(url.encode())
    # Convert the hash to a hexadecimal string
    hex_digest = hash_object.hexdigest()
    # Convert the hexadecimal to an integer, then to base-62
    base62_characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    hash_int = int(hex_digest, 16)
    hash_base62 = ""
    
    # Generate a 6-character base-62 string
    while len(hash_base62) < 6:
        hash_base62 = base62_characters[hash_int % 62] + hash_base62
        hash_int //= 62

    return hash_base62
