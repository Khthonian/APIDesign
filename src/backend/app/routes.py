import os
from datetime import datetime, timedelta
from typing import Annotated

import ipdata
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from openai import OpenAI
from passlib.context import CryptContext
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app import database, models, schemas

# Load env files
load_dotenv()

# Initialise router
router = APIRouter(prefix="/api/v2")

# Initialise OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define access token configs
SECRET_KEY = "testkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30

# Define rate limiter
limiter = Limiter(key_func=get_remote_address)

# Define authentication configs
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v2/users/login")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Define a function to get the database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define database dependency
db_dependency = Annotated[Session, Depends(get_db)]


# Define a function to create an access token
def create_access_token(username: str, id: int, expires: timedelta):
    encode = {"sub": username, "id": id}
    expire = datetime.utcnow() + expires
    encode.update({"exp": expire})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Define a function to create a refresh token
def create_refresh_token(username: str, id: int, expires: timedelta):
    encode = {"sub": username, "id": id, "refresh": True}
    expire = datetime.utcnow() + expires
    encode.update({"exp": expire})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Define a function to get the current user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id: int = payload.get("id")
        if username is None or id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "id": id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )


# Define a function to authenticate the user
def authenticate_user(username: str, password: str, db):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


user_dependency = Annotated[dict, Depends(get_current_user)]

# Routes


# Define a route to register a user
@router.post("/users/register", response_model=schemas.SuccessMessage)
@limiter.limit("20/minute")
async def register_user(request: Request, db: db_dependency, user: schemas.UserCreate):
    # Check if the new username is unique
    existing_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username already registered.",
        )

    # Check if the new email is unique
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email already registered.",
        )

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=bcrypt_context.hash(user.password),
    )

    db.add(db_user)
    db.commit()
    return {"message": "User registered successfully."}


# Define a route to login the user
@router.post("/users/login", response_model=schemas.Token)
@limiter.limit("20/minute")
async def login(
    request: Request,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user = authenticate_user(form.username, form.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )
    token = create_access_token(user.username, user.id, timedelta(minutes=30))
    return {
        "message": "User successfully logged in.",
        "access_token": token,
        "token_type": "bearer",
    }


# Define a route to get the current user's profile
@router.get("/users/profile", response_model=schemas.UserAccount)
@limiter.limit("20/minute")
def get_user_profile(request: Request, user: user_dependency, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user["id"]).first()

    return {"username": db_user.username, "credits": db_user.credits}


# Define a route to update the current user's profile
@router.put("/users/profile", response_model=schemas.UserRefresh)
@limiter.limit("20/minute")
def update_user_profile(
    request: Request,
    user: schemas.UserUpdate,
    current_user: user_dependency,
    db: db_dependency,
):
    db_user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    if user.username == db_user.username:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cannot use current details.",
        )

    # Check if the new username is unique
    if user.username is not None:
        existing_user = (
            db.query(models.User).filter(models.User.username == user.username).first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username already exists.",
            )
        db_user.username = user.username

    db.commit()

    # Create new access and refresh tokens
    db_user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    access_token = create_access_token(
        db_user.username, current_user["id"], timedelta(minutes=30)
    )
    refresh_token = create_refresh_token(
        db_user.username, current_user["id"], timedelta(days=7)
    )

    # Return updated user profile along with new tokens
    return {"user": user, "access_token": access_token, "refresh_token": refresh_token}


# Define a route to delete the current user's profile
@router.delete("/users/profile", response_model=schemas.SuccessMessage)
@limiter.limit("20/minute")
def delete_user_profile(
    request: Request, current_user: user_dependency, db: db_dependency
):
    db_user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    db.query(models.Location).filter(models.Location.user_id == db_user.id).delete()
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully."}


# Define a route to get the current user's credit balance
@router.get("/credits", response_model=schemas.UserBalance)
@limiter.limit("20/minute")
def get_user_credits(
    request: Request, current_user: user_dependency, db: db_dependency
):
    db_user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return {"credits": db_user.credits}


# Define a route for the user to purchase credits
@router.post("/credits/purchase", response_model=schemas.SuccessMessage)
@limiter.limit("20/minute")
def purchase_credits(
    request: Request,
    amount: int,
    current_user: user_dependency,
    db: db_dependency,
):
    db_user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    db_user.credits += amount
    db.commit()
    return {"message": f"{amount} credits purchased successfully."}


# Define a route to get the current user's locations
@router.get("/users/locations")
@limiter.limit("10/minute")
def get_user_locations(
    request: Request, current_user: user_dependency, db: db_dependency
):
    db_user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return {"locations": db_user.locations}


# Define the route to add the current user's current location
@router.post("/users/locations", response_model=schemas.SuccessMessage)
@limiter.limit("10/minute")
def add_user_location(
    request: Request,
    current_user: user_dependency,
    db: db_dependency,
):
    # Step 1: Get user's coordinates from geolocation API (Example: IP Geolocation API)
    geolocation_api_key = os.getenv("GEOLOCATION_API_KEY")
    ipdata.api_key = geolocation_api_key
    try:
        data = ipdata.lookup()
        latitude = data.latitude
        longitude = data.longitude
        city = data.city
        country = data.country_name
    except Exception as e:
        return {"message": "Failed to retrieve user's location"}

    # Step 2: Fetch weather data from OpenWeather API using obtained coordinates
    openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
    openweather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={openweather_api_key}"

    try:
        weather_response = requests.get(openweather_url)
        weather_data = weather_response.json()
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
    except Exception as e:
        return {"message": "Failed to retrieve weather data"}

    # Step 3: Deduct credits from the user
    credit_cost = 1  # Define the cost for adding a location
    db_user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    if db_user.credits < credit_cost:
        return {"message": "Insufficient credits to add location"}

    db_user.credits -= credit_cost
    db.commit()

    # Step 4: Format the response
    location_info = f"{city}, {country}"
    weather_info = f"The weather in {location_info} is currently {temperature - 273.15} degrees Celsius with {description}."

    # Step 5: AI complete the message
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"You are a weather assistant, and I want you to extend the following sentence with a little message about what to wear: {weather_info}",
            },
        ],
        max_tokens=100,
    )
    weather_info = completion.choices[0].message.content

    # Assuming you have a database to store the location
    db_location = models.Location(
        city=city,
        country=country,
        temperature=temperature,
        description=weather_info,
        latitude=latitude,
        longitude=longitude,
        user_id=current_user["id"],
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)

    return {
        "message": "Location added successfully",
    }


# Define a route to delete one of the current user's locations
@router.delete("/users/locations/{location_id}", response_model=schemas.SuccessMessage)
@limiter.limit("20/minute")
def delete_user_location(
    request: Request,
    location_id: int,
    current_user: user_dependency,
    db: db_dependency,
):
    db_location = (
        db.query(models.Location)
        .filter(
            models.Location.id == location_id,
            models.Location.user_id == current_user["id"],
        )
        .first()
    )
    if not db_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Location not found."
        )
    db.delete(db_location)
    db.commit()
    return {"message": "Location deleted successfully."}
