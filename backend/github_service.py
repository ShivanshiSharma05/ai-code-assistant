import requests

def get_repo_files(repo_url):
    parts = repo_url.split("/")
    owner = parts[-2]
    repo = parts[-1]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"

    response = requests.get(api_url)
    files = response.json()

    code_files = []

    for file in files:
        if file["name"].endswith(".py"):
            content = requests.get(file["download_url"]).text
            code_files.append({
                "name": file["name"],
                "code": content
            })

    return code_files