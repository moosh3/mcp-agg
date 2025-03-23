import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Temporarily set DATABASE_URL to use in-memory SQLite for tests
# Use SQLite-compatible parameters
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['TESTING'] = 'True'

# Now import app and database components after setting the environment variable
from api.database import Base, get_db
from api.main import app
from api.models import User, SlackCredentials
from api.apps.github.models import GitHubCredential


# Create a test database in memory
# We already set DATABASE_URL, so we can use it directly from the api.database module
from api.database import engine

# Create a test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Fixture for creating a fresh database session for a test"""
    # Create the test database and tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session for the test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Clean up after the test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session, test_user):
    """Fixture for creating a FastAPI TestClient with a test database and authenticated user"""
    # Import here to avoid circular imports
    from api.dependencies import get_current_active_user
    
    # Override the get_db dependency to use our test session
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    # Override the authentication dependency to use our test user
    async def override_get_current_active_user():
        return test_user
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Remove the overrides after the test
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session):
    """Fixture for creating a test user in the database"""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",  # Not a real hash for testing
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def github_credentials(db_session, test_user):
    """Fixture for creating GitHub credentials for the test user"""
    creds = GitHubCredential(
        user_id=test_user.id,
        access_token="github_test_token",
        token_type="bearer",
        scope="repo,user"
    )
    db_session.add(creds)
    db_session.commit()
    db_session.refresh(creds)
    return creds


@pytest.fixture(scope="function")
def slack_credentials(db_session, test_user):
    """Fixture for creating Slack credentials for the test user"""
    creds = SlackCredentials(
        user_id=test_user.id,
        access_token="xoxp-slack-test-token",
        token_type="bearer",
        scope="channels:read,chat:write",
        team_id="T12345",
        team_name="Test Team"
    )
    db_session.add(creds)
    db_session.commit()
    db_session.refresh(creds)
    return creds
