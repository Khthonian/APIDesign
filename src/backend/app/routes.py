from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import database, models, schemas

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


@router.post("/api/users/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    if user.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return {"token": user.username}


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


def authenticate_user(username: str, password: str, db):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


@router.get("/api/users/profile")
def get_user_profile(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Authentication failed."
        )
    return {"User": user}


@router.put("/api/users/profile")
def update_user_profile(
    user: schemas.User,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    db_user = db.query(models.User).filter(models.User.username == token).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db_user.username = user.username
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/api/users/profile")
def delete_user_profile(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.username == token).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


# Weather Routes


@router.get("/api/weather")
def get_weather(request: schemas.WeatherRequest, db: Session = Depends(get_db)):
    # Logic to retrieve weather information based on location
    # This logic depends on how you interact with a weather API
    pass


# Credit Routes


@router.get("/api/credits")
def get_user_credits(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"credits": user.credits}


@router.post("/api/credits/purchase")
def purchase_credits(
    amount: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user.credits += amount
    db.commit()
    return {"message": f"{amount} credits purchased successfully"}


@router.post("/api/credits/usage")
def use_credits(
    request: schemas.WeatherRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user.credits < 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient credits"
        )
    user.credits -= 1
    db.commit()
    return {"message": "Credit used successfully"}


# User Location Routes


@router.get("/api/users/locations")
def get_user_locations(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user.locations


@router.post("/api/users/locations")
def add_user_location(
    location: schemas.LocationCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    new_location = models.Location(
        city=location.city, country=location.country, user_id=user.id
    )
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location


@router.delete("/api/users/locations/{location_id}")
def delete_user_location(
    location_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    location = (
        db.query(models.Location)
        .filter(models.Location.id == location_id, models.Location.user_id == user.id)
        .first()
    )
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Location not found"
        )
    db.delete(location)
    db.commit()
    return {"message": "Location deleted successfully"}
