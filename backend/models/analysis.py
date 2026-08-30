from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from core.database import Base


class Analysis(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)

    repository_id = Column(
        Integer,
        ForeignKey("repositories.id"),
        nullable=False
    )

    file_name = Column(String(500), nullable=False)

    bugs = Column(Text, nullable=True)

    complexity = Column(String(100), nullable=True)

    optimization = Column(Text, nullable=True)

    quality_score = Column(Integer, nullable=True)

    repository = relationship(
        "Repository",
        back_populates="analyses"
    )

    issues = relationship(
        "Issue",
        back_populates="analysis",
        cascade="all, delete-orphan"
    )