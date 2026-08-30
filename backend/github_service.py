import os
import base64
from pathlib import Path

import requests
from dotenv import load_dotenv


# ============================================================
# Load ROOT .env
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# ============================================================
# GitHub Token
# ============================================================

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


# ============================================================
# GitHub API Headers
# ============================================================

HEADERS = {
    "Accept": "application/vnd.github+json"
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


# ============================================================
# Get Repository Information
# ============================================================

def get_repository_info(owner, repo):
    """
    Get basic information about a GitHub repository.
    """

    url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    if response.status_code != 200:
        return {
            "error": f"GitHub API error: {response.status_code}",
            "details": response.text
        }

    return response.json()


# ============================================================
# Get Repository Files
# ============================================================

def get_repo_files(repo_name):
    """
    Fetch source-code files from a GitHub repository.

    Expected format:

        owner/repository

    Example:

        ShivanshiSharma05/ai-code-assistant
    """

    # --------------------------------------------------------
    # Validate repository format
    # --------------------------------------------------------

    repo_name = repo_name.strip()

    if repo_name.startswith("https://github.com/"):
        repo_name = repo_name.replace(
            "https://github.com/",
            "",
            1
        )

    repo_name = repo_name.rstrip("/")

    parts = repo_name.split("/")

    if len(parts) != 2 or not parts[0] or not parts[1]:
        return {
            "error": (
                "Invalid repository format. "
                "Use owner/repository or a GitHub URL."
            )
        }

    owner = parts[0]
    repo = parts[1]

    # --------------------------------------------------------
    # Get repository information
    # --------------------------------------------------------

    repo_info = get_repository_info(owner, repo)

    if "error" in repo_info:
        return repo_info

    # --------------------------------------------------------
    # Find default branch
    # --------------------------------------------------------

    default_branch = repo_info.get(
        "default_branch",
        "main"
    )

    # --------------------------------------------------------
    # Get repository tree
    # --------------------------------------------------------

    tree_url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/git/trees/"
        f"{default_branch}?recursive=1"
    )

    response = requests.get(
        tree_url,
        headers=HEADERS,
        timeout=30
    )

    if response.status_code != 200:
        return {
            "error": f"Unable to fetch repository tree: {response.status_code}",
            "details": response.text
        }

    tree_data = response.json()

    # --------------------------------------------------------
    # Check tree response
    # --------------------------------------------------------

    if "tree" not in tree_data:
        return {
            "error": "GitHub repository tree could not be retrieved."
        }

    files = {}

    # --------------------------------------------------------
    # Supported source-code extensions
    # --------------------------------------------------------

    allowed_extensions = (
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".cpp",
        ".c",
        ".h",
        ".hpp",
        ".cs",
        ".go",
        ".rs",
        ".php",
        ".rb",
        ".swift",
        ".kt",
        ".kts",
        ".html",
        ".css"
    )

    # --------------------------------------------------------
    # Files/folders we don't need to analyze
    # --------------------------------------------------------

    ignored_parts = {
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
        "build"
    }

    # --------------------------------------------------------
    # Fetch individual files
    # --------------------------------------------------------

    for item in tree_data["tree"]:

        if item.get("type") != "blob":
            continue

        path = item.get("path", "")

        # Ignore unnecessary directories
        path_parts = Path(path).parts

        if any(
            part in ignored_parts
            for part in path_parts
        ):
            continue

        # Only analyze supported source files
        if not path.lower().endswith(allowed_extensions):
            continue

        file_url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/contents/{path}"
        )

        file_response = requests.get(
            file_url,
            headers=HEADERS,
            timeout=30
        )

        if file_response.status_code != 200:
            continue

        file_data = file_response.json()

        # ----------------------------------------------------
        # GitHub normally returns Base64 content
        # ----------------------------------------------------

        if file_data.get("encoding") == "base64":

            try:
                content = base64.b64decode(
                    file_data["content"]
                ).decode(
                    "utf-8",
                    errors="ignore"
                )

                files[path] = content

            except Exception:
                continue

    # --------------------------------------------------------
    # No source files found
    # --------------------------------------------------------

    if not files:
        return {
            "error": "No supported source-code files found in repository."
        }

    return files