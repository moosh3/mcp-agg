from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use SQLite in-memory database for testing
SQLITE_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create test session factory
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for test models
TestBase = declarative_base()
