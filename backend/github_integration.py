from github import Github

GITHUB_TOKEN = "your_token_here"

g = Github(GITHUB_TOKEN)

def get_repo_files(repo_name):
    repo = g.get_repo(repo_name)
    contents = repo.get_contents("")

    files_data = {}

    while contents:
        file = contents.pop(0)

        if file.type == "dir":
            contents.extend(repo.get_contents(file.path))
        else:
            if file.name.endswith(".py"):
                files_data[file.path] = file.decoded_content.decode()

    return files_data