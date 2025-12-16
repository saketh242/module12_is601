import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.database import Base, get_db


# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_engine():
    """Create an in-memory database for testing."""
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a new database session for a test."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with a test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Don't close the session

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session):
    """Create a test user."""
    from app.models.user import User
    
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPass123!"
    }
    user = User.register(db_session, user_data)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_user_token(client, test_user):
    """Get authentication token for test user."""
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "TestPass123!"}
    )
    if response.status_code != 200:
        pytest.fail(f"Failed to login: {response.text}")
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def auth_headers(test_user_token):
    """Return authorization headers for authenticated requests."""
    return {"Authorization": f"Bearer {test_user_token}"}
