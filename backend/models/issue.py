from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from core.database import Base


class Issue(Base):
    __tablename__ = "code_issues"

    id = Column(Integer, primary_key=True, index=True)

    analysis_id = Column(
        Integer,
        ForeignKey("analysis_results.id"),
        nullable=False
    )

    file_path = Column(String(500), nullable=False)

    line_number = Column(Integer, nullable=True)

    severity = Column(String(50), nullable=False)

    message = Column(Text, nullable=False)

    suggestion = Column(Text, nullable=True)

    analysis = relationship(
        "Analysis",
        back_populates="issues"
    )