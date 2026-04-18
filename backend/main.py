from fastapi import FastAPI
from pydantic import BaseModel

from model import generate_code, generate_comment
from analyzer import analyze_code
from github_service import get_repo_files

app = FastAPI(title="AI Code Assistant")

class CodeRequest(BaseModel):
    prompt: str

class CommentRequest(BaseModel):
    code: str

class AnalyzeRequest(BaseModel):
    code: str

class RepoRequest(BaseModel):
    repo_url: str


@app.get("/")
def home():
    return {"message": "AI Code Assistant Running 🚀"}


@app.post("/generate-code/")
def gen_code(request: CodeRequest):
    return {"output": generate_code(request.prompt)}


@app.post("/generate-comment/")
def gen_comment(request: CommentRequest):
    return {"output": generate_comment(request.code)}


@app.post("/analyze/")
def analyze(request: AnalyzeRequest):
    return analyze_code(request.code)


@app.post("/analyze-repo/")
def analyze_repo(request: RepoRequest):
    files = get_repo_files(request.repo_url)

    results = []
    for file in files:
        analysis = analyze_code(file["code"])
        results.append({
            "file": file["name"],
            "analysis": analysis
        })

    return results