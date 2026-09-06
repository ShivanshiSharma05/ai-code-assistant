from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(255),
        nullable=False
    )

    url = Column(
        String(500),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    user = relationship(
        "User",
        back_populates="repositories"
    )

    analyses = relationship(
        "Analysis",
        back_populates="repository",
        cascade="all, delete-orphan"
    )