from fastapi import FastAPI, Body

# Existing AI features
from model import generate_code, generate_comment, generate_comments_inline
from analyzer import analyze_code
from github_service import get_repo_files

# Database
from core.database import Base, engine

# Database models
from models.user import User
from models.repository import Repository
from models.analysis import Analysis
from models.issue import Issue

# API routers
from api.auth import router as auth_router
from api.repositories import router as repository_router


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="AI Code Assistant",
    description="AI-powered code generation, analysis and repository management API",
    version="1.0.0"
)


# Include API routers
app.include_router(auth_router)
app.include_router(repository_router)


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "AI Code Assistant Running"
    }


# --------------------------------------------------
# Generate Code
# --------------------------------------------------

@app.post("/generate-code/")
def gen_code(data: dict = Body(...)):
    prompt = data.get("prompt", "")

    return {
        "output": generate_code(prompt)
    }


# --------------------------------------------------
# Generate Comment
# --------------------------------------------------

@app.post("/generate-comment/")
def gen_comment(data: dict = Body(...)):
    code = data.get("code", "")

    return {
        "output": generate_comment(code)
    }


# --------------------------------------------------
# Generate Inline Comments
# --------------------------------------------------

@app.post("/generate-inline-comments/")
def inline_comments(data: dict = Body(...)):
    code = data.get("code", "")

    return {
        "output": generate_comments_inline(code)
    }


# --------------------------------------------------
# Analyze Code
# --------------------------------------------------

@app.post("/analyze/")
def analyze(data: dict = Body(...)):
    code = data.get("code", "")

    return {
        "output": analyze_code(code)
    }


# --------------------------------------------------
# Analyze GitHub Repository
# --------------------------------------------------

@app.post("/analyze-repo/")
def analyze_repo(data: dict = Body(...)):
    repo_name = data.get("repo", "")

    files = get_repo_files(repo_name)

    # GitHub service returned an error
    if "error" in files:
        return files

    result = {}

    for file, code in files.items():
        result[file] = analyze_code(code)

    return {
        "output": result
    }