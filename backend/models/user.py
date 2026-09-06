from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    hashed_password = Column(
        String(255),
        nullable=False
    )

    repositories = relationship(
        "Repository",
        back_populates="user",
        cascade="all, delete-orphan"
    )