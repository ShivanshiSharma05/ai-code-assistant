import requests


def get_repo_files(repo_name: str):
    """
    Fetch Python files from a public GitHub repository.

    repo_name examples:
        "ShivanshiSharma05/ai-code-assistant"
        "https://github.com/ShivanshiSharma05/ai-code-assistant"
    """

    # Convert full GitHub URL to owner/repository format
    if repo_name.startswith("https://github.com/"):
        repo_name = repo_name.replace(
            "https://github.com/",
            ""
        )

    if repo_name.startswith("http://github.com/"):
        repo_name = repo_name.replace(
            "http://github.com/",
            ""
        )

    # Remove trailing slash
    repo_name = repo_name.rstrip("/")

    # Remove .git if user provides it
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    # Validate repository format
    parts = repo_name.split("/")

    if len(parts) != 2:
        return {
            "error": (
                "Invalid repository format. "
                "Use owner/repository or a GitHub URL."
            )
        }

    owner = parts[0]
    repo = parts[1]

    # GitHub API URL
    api_url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/git/trees/HEAD?recursive=1"
    )

    try:
        response = requests.get(
            api_url,
            timeout=15
        )

        if response.status_code == 404:
            return {
                "error": "GitHub repository not found."
            }

        if response.status_code != 200:
            return {
                "error": (
                    f"GitHub API request failed: "
                    f"{response.status_code}"
                )
            }

        data = response.json()

        if "tree" not in data:
            return {
                "error": "Could not retrieve repository files."
            }

        files = {}

        # Find Python files
        for item in data["tree"]:

            if item["type"] != "blob":
                continue

            file_path = item["path"]

            if not file_path.endswith(".py"):
                continue

            # Ignore unnecessary folders
            if any(
                folder in file_path.split("/")
                for folder in [
                    ".git",
                    "__pycache__",
                    "venv",
                    ".venv",
                    "node_modules"
                ]
            ):
                continue

            # Download file content
            raw_url = (
                f"https://raw.githubusercontent.com/"
                f"{owner}/{repo}/HEAD/{file_path}"
            )

            file_response = requests.get(
                raw_url,
                timeout=15
            )

            if file_response.status_code == 200:
                files[file_path] = file_response.text

        return files

    except requests.exceptions.Timeout:
        return {
            "error": "GitHub request timed out."
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": f"GitHub request failed: {str(e)}"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }