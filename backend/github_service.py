import os
import requests
from dotenv import load_dotenv


# Load .env from project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


HEADERS = {
    "Accept": "application/vnd.github+json"
}


# Add token only if available
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


# =========================================================
# GET REPOSITORY INFORMATION
# =========================================================

def get_repository_info(repo_name):

    url = f"https://api.github.com/repos/{repo_name}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    if response.status_code != 200:

        raise Exception(
            f"GitHub API error: {response.status_code} - "
            f"{response.text}"
        )

    return response.json()


# =========================================================
# GET REPOSITORY FILE TREE
# =========================================================

def get_repository_tree(repo_name):

    url = (
        f"https://api.github.com/repos/"
        f"{repo_name}/git/trees/HEAD?recursive=1"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    if response.status_code != 200:

        raise Exception(
            f"GitHub API error while fetching tree: "
            f"{response.status_code} - {response.text}"
        )

    data = response.json()

    return data.get("tree", [])


# =========================================================
# GET SINGLE FILE CONTENT
# =========================================================

def get_file_content(repo_name, file_path):

    url = (
        f"https://api.github.com/repos/"
        f"{repo_name}/contents/{file_path}"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    if response.status_code != 200:

        return None

    data = response.json()

    # GitHub gives download_url for files
    download_url = data.get("download_url")

    if not download_url:
        return None

    file_response = requests.get(
        download_url,
        headers=HEADERS,
        timeout=20
    )

    if file_response.status_code != 200:
        return None

    return file_response.text


# =========================================================
# GET ALL SUPPORTED REPOSITORY FILES
# =========================================================

def get_repository_files(repo_name):

    tree = get_repository_tree(repo_name)

    supported_extensions = (
        ".py",
        ".js",
        ".ts",
        ".java",
        ".cpp",
        ".c"
    )

    files = {}

    for item in tree:

        # Only files
        if item.get("type") != "blob":
            continue

        file_path = item.get("path")

        # Skip unsupported files
        if not file_path.endswith(supported_extensions):
            continue

        # Skip unnecessary folders
        if (
            "node_modules/" in file_path
            or ".git/" in file_path
            or "venv/" in file_path
            or "__pycache__/" in file_path
        ):
            continue

        try:

            content = get_file_content(
                repo_name,
                file_path
            )

            if content:

                files[file_path] = content

        except Exception as e:

            print(
                f"Could not fetch {file_path}: {str(e)}"
            )

    return files