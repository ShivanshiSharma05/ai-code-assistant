from pydantic import BaseModel


class RepositoryCreate(BaseModel):
    name: str
    url: str
    description: str | None = None


class RepositoryResponse(BaseModel):
    id: int
    name: str
    url: str
    description: str | None = None

    class Config:
        from_attributes = True