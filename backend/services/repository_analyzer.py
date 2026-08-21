import os
from analyzer import analyze_code


def analyze_repository(repo_path: str):
    results = []

    for root, dirs, files in os.walk(repo_path):

        # Ignore unnecessary directories
        dirs[:] = [
            d for d in dirs
            if d not in {
                ".git",
                "__pycache__",
                "venv",
                ".venv",
                "node_modules"
            }
        ]

        for file in files:

            if not file.endswith(".py"):
                continue

            file_path = os.path.join(root, file)

            try:
                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as f:
                    code = f.read()

                analysis = analyze_code(code)

                results.append({
                    "file": os.path.relpath(
                        file_path,
                        repo_path
                    ),
                    "analysis": analysis
                })

            except Exception as e:

                results.append({
                    "file": os.path.relpath(
                        file_path,
                        repo_path
                    ),
                    "error": str(e)
                })

    return results