from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app
from app.routes import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

login_token = None


# Default registration test
def test_register_user():
    # Define test data
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
    }

    # Make POST request to register a user
    response = client.post("/api/v2/users/register", json=user_data)

    # Verify that the response status code is 200 OK
    assert response.status_code == 200

    # Verify that the response body contains the expected message
    assert response.json()["message"] == "User registered successfully."


# Faulty email registration test
def test_poor_email_register_user():
    # Define test data
    user_data = {
        "username": "pooremailuser",
        "email": "pooremail",
        "password": "testpassword",
    }

    # Make a POST request to register a user
    response = client.post("/api/v2/users/register", json=user_data)

    # Verify that the response status code is 422 UNPROCESSABLE ENTITY
    assert response.status_code == 422


# Duplicate name registration test
def test_duplicate_name_register_user():
    # Define the duplicate test data
    user_data = {
        "username": "testuser",
        "email": "duplicatename@example.com",
        "password": "testpassword",
    }

    # Make a POST request to register a user
    response = client.post("/api/v2/users/register", json=user_data)

    # Verify that the response status code is 422 UNPROCESSABLE ENTITY
    assert response.status_code == 422

    # Verify that the response body contains the expected message
    assert response.json()["detail"] == "Username already registered."


# Duplicate email registration test
def test_duplicate_email_register_user():
    # Define the duplicate test data
    user_data = {
        "username": "duplicateemail",
        "email": "test@example.com",
        "password": "testpassword",
    }

    # Make a POST request to register a user
    response = client.post("/api/v2/users/register", json=user_data)

    # Verify that the response status code is 422 UNPROCESSABLE ENTITY
    assert response.status_code == 422

    # Verify that the response body contains the expected message
    assert response.json()["detail"] == "Email already registered."


# Default login test
def test_login_user():
    # Define the user data
    user_data = {
        "username": "testuser",
        "password": "testpassword",
    }

    # Make a POST request to login a user
    response = client.post("/api/v2/users/token", data=user_data)

    global login_token
    login_token = response.json()["access_token"]

    # Verify that the response status code is 200 OK
    assert response.status_code == 200

    # Verify that the response body contains the expected message
    assert response.json()["message"] == "User successfully logged in."

    # Verify that the response body contains the expected token type
    assert response.json()["token_type"] == "bearer"


# Unauthenticated login test
def test_bad_login_user():
    # Define the unauthorised data
    bad_user_data = {
        "username": "notauser",
        "password": "testpassword",
    }

    # Make a POST request to attempt a login
    response = client.post("/api/v2/users/token", data=bad_user_data)

    # Verify that the response status code is 401 UNAUTHORIZED
    assert response.status_code == 401

    # Verify that the response body contains the expected message
    assert response.json()["detail"] == "Could not validate user."


# Default get user profile test
def test_get_user_profile():
    # Make a GET request to get the user profile
    response = client.get(
        "/api/v2/users/profile", headers={"Authorization": f"Bearer {login_token}"}
    )

    print(login_token)

    # Verify that the response status code is 200 OK
    assert response.status_code == 200

    # Verify that the response body contains the expected keys
    assert response.json()["User"] == "testuser"

    # Verify that the response body contains the expected credit balance
    assert response.json()["Credits"] == 2000


# Unauthorised get user profile test
def test_bad_get_user_profile():
    # Make a GET request to get the user profile
    response = client.get(
        "/api/v2/users/profile", headers={"Authorization": "Bearer thisisnotreal"}
    )

    print(login_token)

    # Verify that the response status code is 401 UNAUTHORIZED
    assert response.status_code == 401

    # Verify that the response body contains the expected message
    assert response.json()["detail"] == "Could not validate user."
