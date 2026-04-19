from fastapi import FastAPI, Body
from backend.model import generate_code, generate_comment
from backend.analyzer import analyze_code
from backend.github_integration import get_repo_files
from backend.model import generate_comments_inline

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Code Assistant Running"}

@app.post("/generate-code/")
def gen_code(data: dict = Body(...)):
    prompt = data.get("prompt", "")
    return {"output": generate_code(prompt)}

@app.post("/generate-comment/")
def gen_comment(data: dict = Body(...)):
    code = data.get("code", "")
    return {"output": generate_comment(code)}

@app.post("/generate-inline-comments/")
def inline_comments(data: dict):
    code = data.get("code", "")
    return {"output": generate_comments_inline(code)}

@app.post("/analyze/")
def analyze(data: dict = Body(...)):
    code = data.get("code", "")
    return analyze_code(code)

@app.post("/analyze-repo/")
def analyze_repo(data: dict = Body(...)):
    repo_name = data.get("repo", "")
    files = get_repo_files(repo_name)

    if "error" in files:
        return files

    result = {}
    for file, code in files.items():
        result[file] = analyze_code(code)

    return result