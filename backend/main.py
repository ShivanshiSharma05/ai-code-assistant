from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Database
from core.database import Base, engine, get_db

# Models
from models.repository import Repository
from models.analysis import Analysis

# Authentication Router
from api.auth import router as auth_router

# Repository Router
from api.repositories import router as repository_router

# Existing Code Analyzer
from analyzer import analyze_code

# GitHub Service
from github_service import get_repository_files

# Repository Intelligence Engine
from services.repository_analyzer import (
    analyze_repository_files,
    calculate_repository_summary
)


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="AI Code Assistant",
    version="2.0.0",
    description=(
        "AI-powered repository intelligence platform that analyzes "
        "GitHub repositories, detects risks, prioritizes files, and "
        "generates actionable recommendations for developers."
    )
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# INCLUDE ROUTERS
# =========================================================

app.include_router(auth_router)
app.include_router(repository_router)


# =========================================================
# REQUEST MODELS
# =========================================================

class CodeRequest(BaseModel):
    code: str


class CommentRequest(BaseModel):
    code: str


class RepoRequest(BaseModel):
    repo: str


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to AI Code Assistant",
        "version": "2.0.0",
        "features": [
            "AI Code Analysis",
            "Code Generation",
            "Code Comments",
            "Repository Analysis",
            "Risk Detection",
            "Developer Priority Queue"
        ]
    }


# =========================================================
# GENERATE CODE
# =========================================================

@app.post("/generate-code/")
def gen_code(request: CodeRequest):

    """
    Basic code generation endpoint.
    """

    return {
        "message": "Code generation endpoint",
        "prompt": request.code,
        "generated_code": (
            "# AI-generated code placeholder\n"
            "# Integrate your existing LLM/code generation logic here."
        )
    }


# =========================================================
# GENERATE COMMENTS
# =========================================================

@app.post("/generate-comment/")
def gen_comment(request: CommentRequest):

    """
    Generate general explanation/comments for code.
    """

    code = request.code

    lines = code.splitlines()

    comments = []

    for index, line in enumerate(lines, start=1):

        stripped = line.strip()

        if stripped.startswith("def "):

            function_name = (
                stripped
                .replace("def ", "")
                .split("(")[0]
            )

            comments.append({
                "line": index,
                "comment": (
                    f"Function '{function_name}' "
                    "contains reusable program logic."
                )
            })

        elif stripped.startswith("for "):

            comments.append({
                "line": index,
                "comment": "Loop iterates over a collection."
            })

        elif stripped.startswith("while "):

            comments.append({
                "line": index,
                "comment": "Loop continues while the condition is true."
            })

        elif stripped.startswith("if "):

            comments.append({
                "line": index,
                "comment": "Conditional logic controls program flow."
            })

    return {
        "comments": comments
    }


# =========================================================
# GENERATE INLINE COMMENTS
# =========================================================

@app.post("/generate-inline-comments/")
def inline_comments(request: CommentRequest):

    """
    Generate simple inline comments for detected structures.
    """

    code = request.code

    lines = code.splitlines()

    result = []

    for line in lines:

        stripped = line.strip()

        if stripped.startswith("def "):

            result.append(
                "# Defines a reusable function"
            )

        elif stripped.startswith("for "):

            result.append(
                "# Iterate through the collection"
            )

        elif stripped.startswith("while "):

            result.append(
                "# Continue execution while condition is true"
            )

        elif stripped.startswith("if "):

            result.append(
                "# Check condition before executing block"
            )

        result.append(line)

    commented_code = "\n".join(result)

    return {
        "commented_code": commented_code
    }


# =========================================================
# ANALYZE SINGLE CODE
# =========================================================

@app.post("/analyze/")
def analyze(request: CodeRequest):

    """
    Analyze a single code snippet.
    """

    try:

        result = analyze_code(request.code)

        return {
            "message": "Code analysis completed successfully",
            "analysis": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# ANALYZE GITHUB REPOSITORY
# =========================================================

@app.post("/analyze-repo/")
def analyze_repo(
    request: RepoRequest,
    db: Session = Depends(get_db)
):

    """
    Main Repository Intelligence Endpoint

    Workflow:

    GitHub Repository
            ↓
    Fetch Python Files
            ↓
    Code Analysis
            ↓
    Risk Engine
            ↓
    Priority Calculation
            ↓
    Repository Summary
            ↓
    Developer Action Plan
    """

    repo_name = request.repo.strip()

    try:

        # =================================================
        # VALIDATE REPOSITORY FORMAT
        # =================================================

        if not repo_name:

            raise HTTPException(
                status_code=400,
                detail="Repository name cannot be empty"
            )

        # Support GitHub URL
        if "github.com/" in repo_name:

            repo_name = (
                repo_name
                .split("github.com/")[-1]
                .replace(".git", "")
                .strip("/")
            )

        # Must be owner/repository
        if "/" not in repo_name:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid repository format. "
                    "Use owner/repository or GitHub URL."
                )
            )

        # =================================================
        # CHECK DATABASE
        # =================================================

        repository = (
            db.query(Repository)
            .filter(
                Repository.url.contains(repo_name)
            )
            .first()
        )

        # =================================================
        # CREATE REPOSITORY ENTRY IF NOT EXISTS
        # =================================================

        if not repository:

            repository = Repository(
                name=repo_name.split("/")[-1],
                url=f"https://github.com/{repo_name}",
                description="Repository analyzed by AI Code Assistant"
            )

            db.add(repository)

            db.commit()

            db.refresh(repository)

        # =================================================
        # FETCH FILES FROM GITHUB
        # =================================================

        files = get_repository_files(repo_name)

        if not files:

            raise HTTPException(
                status_code=404,
                detail=(
                    "No supported source files found "
                    "in this repository."
                )
            )

        # =================================================
        # ANALYZE REPOSITORY WITH RISK ENGINE
        # =================================================

        output = analyze_repository_files(files)

        # =================================================
        # CALCULATE SUMMARY
        # =================================================

        summary = calculate_repository_summary(output)

        # =================================================
        # SAVE ANALYSIS RESULTS
        # =================================================

        for file_name, analysis_data in output.items():

            existing_analysis = (
                db.query(Analysis)
                .filter(
                    Analysis.repository_id == repository.id,
                    Analysis.file_name == file_name
                )
                .first()
            )

            if existing_analysis:

                existing_analysis.bugs = str(
                    analysis_data.get("bugs", "")
                )

                existing_analysis.complexity = str(
                    analysis_data.get("complexity", "")
                )

                existing_analysis.optimization = str(
                    analysis_data.get("optimization", "")
                )

                existing_analysis.quality_score = int(
                    analysis_data.get("quality_score", 0)
                )

            else:

                new_analysis = Analysis(
                    repository_id=repository.id,
                    file_name=file_name,
                    bugs=str(
                        analysis_data.get("bugs", "")
                    ),
                    complexity=str(
                        analysis_data.get("complexity", "")
                    ),
                    optimization=str(
                        analysis_data.get("optimization", "")
                    ),
                    quality_score=int(
                        analysis_data.get("quality_score", 0)
                    )
                )

                db.add(new_analysis)

        db.commit()

        # =================================================
        # RETURN FINAL REPOSITORY INTELLIGENCE
        # =================================================

        return {

            "message": (
                "Repository analysis completed successfully"
            ),

            "repository": repo_name,

            "summary": summary,

            "output": output
        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        print(
            "Repository Analysis Error:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )