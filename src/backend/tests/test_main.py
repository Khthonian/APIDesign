from fastapi import responses
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
    global default_user_data
    default_user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
    }

    # Make POST request to register a user
    response = client.post("/api/v2/users/register", json=default_user_data)

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
        "username": default_user_data["username"],
        "password": default_user_data["password"],
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

    # Verify that the response status code is 200 OK
    assert response.status_code == 200

    # Verify that the response body contains the expected keys
    assert response.json()["user"] == "testuser"

    # Verify that the response body contains the expected credit balance
    assert response.json()["credits"] == 2000


# Unauthorised get user profile test
def test_bad_get_user_profile():
    # Make a GET request to get the user profile
    response = client.get(
        "/api/v2/users/profile", headers={"Authorization": "Bearer thisisnotreal"}
    )

    # Verify that the response status code is 401 UNAUTHORIZED
    assert response.status_code == 401

    # Verify that the response body contains the expected message
    assert response.json()["detail"] == "Could not validate user."


# Default update user profile test
def test_update_user_profile():
    # Define the new user settings
    user_data = {
        "username": "testuserNEW",
        "email": "testNEW@example.com",
    }

    global login_token

    # Make a PUT request to update the user profile
    response = client.put(
        "/api/v2/users/profile",
        headers={"Authorization": f"Bearer {login_token}"},
        json=user_data,
    )

    login_token = response.json()["access_token"]

    # Verify that the response status code is 200 OK
    assert response.status_code == 200

    # Verify that the response body contains the expected content
    assert response.json()["user"] == {
        "username": "testuserNEW",
        "email": "testNEW@example.com",
    }

    # Reset user profile settings
    reset = client.put(
        "/api/v2/users/profile",
        headers={"Authorization": f"Bearer {login_token}"},
        json=default_user_data,
    )

    login_token = reset.json()["access_token"]


# Unique username update test
def test_unique_name_update_user_profile():
    # Define the new user settings
    user_data = {
        "username": default_user_data["username"],
        "email": "testNEW@example.com",
    }

    # Make a PUT request to update the user profile
    response = client.put(
        "/api/v2/users/profile",
        headers={"Authorization": f"Bearer {login_token}"},
        json=user_data,
    )

    # Verify that the response status code is 422 UNPROCESSABLE ENTITY
    assert response.status_code == 422


# Unique username update test
def test_unique_email_update_user_profile():
    # Define the new user settings
    user_data = {
        "username": "testuserNEW",
        "email": default_user_data["email"],
    }

    # Make a PUT request to update the user profile
    response = client.put(
        "/api/v2/users/profile",
        headers={"Authorization": f"Bearer {login_token}"},
        json=user_data,
    )

    # Verify that the response status code is 422 UNPROCESSABLE ENTITIY
    assert response.status_code == 422


# Default get user credit test
def test_user_credit():
    # Make a GET request to get the user profile
    response = client.get(
        "/api/v2/credits", headers={"Authorization": f"Bearer {login_token}"}
    )

    print(response)

    # Verify that the response status code is 200 OK
    assert response.status_code == 200

    # Verify that the response body contains the expected credit balance
    assert response.json()["credits"] == 2000


# Default purchase user credit test
def test_purchase_credit():
    # Make a GET request to get the user profile
    response = client.post(
        "/api/v2/credits/purchase?amount=250",
        headers={"Authorization": f"Bearer {login_token}"},
    )

    # Verify that the response status code is 200 OK
    assert response.status_code == 200

    # Verify that the response body contains the expected credit balance
    assert response.json()["message"] == "250 credits purchased successfully."


# Default get user locations test
def test_get_user_locations():
    # Make a GET request to get the user's locations
    response = client.get(
        "/api/v2/users/locations", headers={"Authorization": f"Bearer {login_token}"}
    )

    # Verify that the response status code is 200 OK
    assert response.status_code == 200

    # Verify that the response body contains the expected keys
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 0


# Default add user location test
def test_new_user_location():
    # Make a POST request to add a new user location
    response = client.post(
        "/api/v2/users/locations", headers={"Authorization": f"Bearer {login_token}"}
    )

    # Verify that the response status code is 200 OK
    assert response.status_code == 200

    # Verify that the response body contains the expected keys
    assert "message" in response.json()
    assert "weather_info" in response.json()
    assert "temperature" in response.json()
    assert "latitude" in response.json()
    assert "longitude" in response.json()
    assert "ip" in response.json()
