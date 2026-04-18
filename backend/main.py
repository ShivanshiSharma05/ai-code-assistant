from fastapi import FastAPI
from model import generate_code, generate_comment
from analyzer import analyze_code, project_analysis
from github_integration import get_repo_files

app = FastAPI()

request_count = 0
LIMIT = 200

def check_limit():
    global request_count
    request_count += 1
    if request_count > LIMIT:
        return {"error": "Rate limit exceeded"}
    return None

@app.get("/")
def home():
    return {"message": "AI Code Assistant Running"}

@app.post("/generate-code/")
def gen_code(prompt: str):
    limit = check_limit()
    if limit:
        return limit
    return {"output": generate_code(prompt)}

@app.post("/generate-comment/")
def gen_comment(code: str):
    return {"output": generate_comment(code)}

@app.post("/analyze/")
def analyze(code: str):
    return analyze_code(code)

@app.post("/project-analysis/")
def project_level(files: dict):
    return project_analysis(files)

@app.post("/analyze-repo/")
def analyze_repo(repo_name: str):
    files = get_repo_files(repo_name)
    return project_analysis(files)