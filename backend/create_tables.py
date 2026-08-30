from core.database import Base, engine

# Import ALL models so SQLAlchemy registers them
from models.user import User
from models.repository import Repository
from models.analysis import Analysis
from models.issue import Issue


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")