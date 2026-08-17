from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class Analysis(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)

    repository_id = Column(
        Integer,
        ForeignKey("repositories.id"),
        nullable=False
    )

    status = Column(String(50), nullable=False, default="completed")

    summary = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    repository = relationship(
        "Repository",
        back_populates="analyses"
    )

    issues = relationship(
        "Issue",
        back_populates="analysis",
        cascade="all, delete-orphan"
    )