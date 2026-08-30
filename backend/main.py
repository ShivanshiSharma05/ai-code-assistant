from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from model import generate_code, generate_comment, generate_comments_inline
from analyzer import analyze_code
from github_service import get_repo_files

from core.database import Base, engine, get_db

from models.user import User
from models.repository import Repository
from models.analysis import Analysis
from models.issue import Issue

from api.auth import router as auth_router
from api.repositories import router as repository_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Code Assistant",
    description="AI-powered code generation and repository analysis platform",
    version="2.0.0"
)


# Routers
app.include_router(auth_router)
app.include_router(repository_router)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "AI Code Assistant Running",
        "version": "2.0.0"
    }


# --------------------------------------------------
# CODE GENERATION
# --------------------------------------------------

@app.post("/generate-code/")
def gen_code(data: dict = Body(...)):
    prompt = data.get("prompt", "")

    if not prompt:
        raise HTTPException(
            status_code=400,
            detail="Prompt is required"
        )

    return {
        "output": generate_code(prompt)
    }


# --------------------------------------------------
# COMMENT GENERATION
# --------------------------------------------------

@app.post("/generate-comment/")
def gen_comment(data: dict = Body(...)):
    code = data.get("code", "")

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Code is required"
        )

    return {
        "output": generate_comment(code)
    }


# --------------------------------------------------
# INLINE COMMENTS
# --------------------------------------------------

@app.post("/generate-inline-comments/")
def inline_comments(data: dict = Body(...)):
    code = data.get("code", "")

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Code is required"
        )

    return {
        "output": generate_comments_inline(code)
    }


# --------------------------------------------------
# SINGLE FILE ANALYSIS
# --------------------------------------------------

@app.post("/analyze/")
def analyze(data: dict = Body(...)):
    code = data.get("code", "")

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Code is required"
        )

    return {
        "output": analyze_code(code)
    }


# --------------------------------------------------
# REPOSITORY ANALYSIS
# --------------------------------------------------

@app.post("/analyze-repo/")
def analyze_repo(
    data: dict = Body(...),
    db: Session = Depends(get_db)
):
    repo_name = data.get("repo", "")

    if not repo_name:
        raise HTTPException(
            status_code=400,
            detail="Repository is required"
        )

    # ----------------------------------------------
    # Validate repository format
    # ----------------------------------------------

    if "/" not in repo_name:
        return {
            "error": "Invalid repository format. Use owner/repository or a GitHub URL."
        }

    # ----------------------------------------------
    # Find repository in database
    # ----------------------------------------------

    repository = (
        db.query(Repository)
        .filter(Repository.url.contains(repo_name))
        .first()
    )

    if not repository:
        return {
            "error": "Repository not found in database"
        }

    # ----------------------------------------------
    # Get files from GitHub
    # ----------------------------------------------

    files = get_repo_files(repo_name)

    if "error" in files:
        return files

    results = {}

    # ----------------------------------------------
    # Analyze every Python file
    # ----------------------------------------------

    for file_name, code in files.items():

        try:
            result = analyze_code(code)

            results[file_name] = result

            # --------------------------------------
            # Save analysis result
            # --------------------------------------

            analysis = Analysis(
                repository_id=repository.id,
                file_name=file_name,
                bugs=result.get("bugs"),
                complexity=result.get("complexity"),
                optimization=result.get("optimization"),
                quality_score=result.get("quality_score")
            )

            db.add(analysis)

        except Exception as e:

            results[file_name] = {
                "error": str(e)
            }

    # Save all analysis records
    db.commit()

    return {
        "repository": repository.name,
        "repository_id": repository.id,
        "files_analyzed": len(results),
        "output": results
    }