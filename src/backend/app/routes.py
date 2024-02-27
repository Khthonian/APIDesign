from datetime import datetime, timedelta
from typing import Annotated

import requests
from app import database, models, schemas
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

router = APIRouter()

SECRET_KEY = "testkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def create_access_token(username: str, id: int, expires: timedelta):
    encode = {"sub": username, "id": id}
    expire = datetime.utcnow() + expires
    encode.update({"exp": expire})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(username: str, id: int, expires: timedelta):
    encode = {"sub": username, "id": id, "refresh": True}
    expire = datetime.utcnow() + expires
    encode.update({"exp": expire})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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


def authenticate_user(username: str, password: str, db):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


user_dependency = Annotated[dict, Depends(get_current_user)]

# User Routes


@router.post("/api/users/register")
async def register_user(db: db_dependency, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=bcrypt_context.hash(user.password),
    )
    db.add(db_user)
    db.commit()


@router.post("/api/users/token", response_model=schemas.Token)
async def login_for_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form.username, form.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )
    token = create_access_token(user.username, user.id, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/api/users/profile")
def get_user_profile(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Authentication failed."
        )
    db_user = db.query(models.User).filter(models.User.id == user["id"]).first()

    return {"User": db_user.username, "Credits": db_user.credits}


@router.put("/api/users/profile")
def update_user_profile(
    user: schemas.UserBase,
    current_user: user_dependency,
    db: db_dependency,
):
    db_user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    # Update user profile in the database
    db_user.username = user.username
    db_user.email = user.email
    db.commit()

    # Create new access and refresh tokens
    access_token = create_access_token(
        user.username, current_user["id"], timedelta(minutes=30)
    )
    refresh_token = create_refresh_token(
        user.username, current_user["id"], timedelta(days=7)
    )

    # Return updated user profile along with new tokens
    return {"User": user, "access_token": access_token, "refresh_token": refresh_token}


# Logic to delete user profile based on token
@router.delete("/api/users/profile")
def delete_user_profile(current_user: user_dependency, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully."}


# Logic to retrieve weather information based on location
@router.get("/api/weather")
def get_weather(request: schemas.WeatherRequest, db: db_dependency):
    # Here you would typically integrate with a weather API service
    # and retrieve weather information based on the provided location
    # For demonstration purposes, let's assume we return mock weather data
    return {
        "location": f"{request.location.city}, {request.location.country}",
        "weather": "Sunny",
        "temperature": "25°C",
    }


# Logic to retrieve user's credit balance
@router.get("/api/credits")
def get_user_credits(current_user: user_dependency, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return {"credits": db_user.credits}


# Logic to purchase credits for the user
@router.post("/api/credits/purchase")
def purchase_credits(
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


# Logic to deduct credits for weather requests
@router.post("/api/credits/usage")
def use_credits(
    request: schemas.WeatherRequest, current_user: user_dependency, db: db_dependency
):
    db_user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    if db_user.credits < 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient credits."
        )
    db_user.credits -= 1
    db.commit()
    return {"message": "Credit used successfully."}


# Logic to retrieve user's saved locations
@router.get("/api/users/locations")
def get_user_locations(current_user: user_dependency, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return db_user.locations


# Logic to add a new location to user's saved locations
@router.post("/api/users/locations")
def add_user_location(
    request: Request,
    location: schemas.LocationCreate,
    current_user: user_dependency,
    db: db_dependency,
):
    # Step 1: Get user's coordinates from geolocation API (Example: IP Geolocation API)
    ip_address = request.client.host
    geolocation_api_key = ""
    geolocation_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={geolocation_api_key}&ip={ip_address}"

    try:
        response = requests.get(geolocation_url)
        data = response.json()
        latitude = data["latitude"]
        longitude = data["longitude"]
    except Exception as e:
        return {"error": "Failed to retrieve user's location"}

    # Step 2: Fetch weather data from OpenWeather API using obtained coordinates
    openweather_api_key = ""
    openweather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={openweather_api_key}"

    try:
        weather_response = requests.get(openweather_url)
        weather_data = weather_response.json()
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
    except Exception as e:
        return {"error": "Failed to retrieve weather data"}

    # Step 3: Deduct credits from the user
    credit_cost = 1  # Define the cost for adding a location
    db_user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    if db_user.credits < credit_cost:
        return {"error": "Insufficient credits to add location"}

    db_user.credits -= credit_cost
    db.commit()

    # Step 4: Format the response
    location_info = f"{location.city}, {location.country}"
    weather_info = f"The weather in {location_info} is currently {temperature} degrees Celsius with {description}."

    # Assuming you have a database to store the location
    db_location = models.Location(
        city=location.city,
        country=location.country,
        latitude=latitude,
        longitude=longitude,
        user_id=current_user["id"],
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)

    return {"message": "Location added successfully", "weather_info": weather_info}


# Logic to delete a location from user's saved locations
@router.delete("/api/users/locations/{location_id}")
def delete_user_location(
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
