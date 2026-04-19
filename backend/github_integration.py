import os
from dotenv import load_dotenv
from github import Github

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

g = Github(token) if token else Github()

def get_repo_files(repo_name):
    try:
        repo = g.get_repo(repo_name)
        contents = repo.get_contents("")

        files = {}

        while contents:
            file = contents.pop(0)

            if file.type == "dir":
                contents.extend(repo.get_contents(file.path))
            else:
                if file.name.endswith(".py"):
                    files[file.path] = file.decoded_content.decode()

        return files

    except Exception as e:
        return {"error": str(e)}