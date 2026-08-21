from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from models.repository import Repository
from schemas.repository import RepositoryCreate, RepositoryResponse


router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"]
)


@router.post(
    "/",
    response_model=RepositoryResponse
)
def create_repository(
    data: RepositoryCreate,
    db: Session = Depends(get_db)
):
    repository = Repository(
        name=data.name,
        url=data.url,
        description=data.description,
        user_id=1
    )

    db.add(repository)
    db.commit()
    db.refresh(repository)

    return repository


@router.get(
    "/",
    response_model=list[RepositoryResponse]
)
def get_repositories(
    db: Session = Depends(get_db)
):
    repositories = db.query(Repository).all()

    return repositories


@router.get(
    "/{repository_id}",
    response_model=RepositoryResponse
)
def get_repository(
    repository_id: int,
    db: Session = Depends(get_db)
):
    repository = db.query(Repository).filter(
        Repository.id == repository_id
    ).first()

    if not repository:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    return repository


@router.delete("/{repository_id}")
def delete_repository(
    repository_id: int,
    db: Session = Depends(get_db)
):
    repository = db.query(Repository).filter(
        Repository.id == repository_id
    ).first()

    if not repository:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    db.delete(repository)
    db.commit()

    return {
        "message": "Repository deleted successfully"
    }