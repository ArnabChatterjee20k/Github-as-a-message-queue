### setting up the workers with cli
```bash
githubmq setup --repo-url "https://github.com/ArnabChatterjee20k/github-queue-test.git" --auth-token "<get it from github personal access token>" --origin "main"
```
If getting error consumers folder does not exists
Format - consumers/{label}/main.py
for the <label> the main.py will be triggered

Then rerun
### Accessing the message in consumers
```
import os
os.environ.get("ISSUE_TITLE")
os.environ.get("ISSUE_BODY")
os.environ.get("ISSUE_NUMBER")
```

### Env setting
If any consumer is using keys, please set it manually in the github actions secret manager.
Then use the function to grab the secrets
Upper case as all secrets are saved in form of upper case only
```python
def get_secret_val(key:str):
    all_secrets = json.loads(os.environ.get('ALL_SECRETS', '{}'))
    # Get the entire variables context
    # all_vars = json.loads(os.environ.get('ALL_VARS', '{}'))
    
    return all_secrets.get(key.upper())
```