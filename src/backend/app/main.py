from pathlib import Path

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .locationData import LOCATION

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather API", openapi_url="/openapi.json")

apiRouter = APIRouter()

origins = ["http://localhost:3000", "localhost:3000"]

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define a function to get the database
def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define the root route
@apiRouter.get("/", status_code=200)
def root(request: Request):
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "locations": LOCATION},
    )


# Define the user creation route
@apiRouter.post("/users/", status_code=200, response_model=schemas.User)
def createUser(user: schemas.UserCreate, db: Session = Depends(getDB)):
    dbUser = crud.getUserByEmail(db, email=user.email)
    if dbUser:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.createUser(db=db, user=user)


# Define the users read route
@apiRouter.get("/users/", response_model=list[schemas.User])
def readUsers(skip: int = 0, limit: int = 100, db: Session = Depends(getDB)):
    users = crud.getUsers(db, skip=skip, limit=limit)
    return users


# Define the user read route
@apiRouter.get("/users/{userId}", response_model=schemas.User)
def readUser(userId: int, db: Session = Depends(getDB)):
    dbUser = crud.getUser(db, userId=userId)
    if dbUser is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dbUser


# Define the user update route
@apiRouter.post("/users/{userId}/locations/", response_model=schemas.Location)
def createLocationForUser(
    userId: int, location: schemas.LocationCreate, db: Session = Depends(getDB)
):
    return crud.createUserLocation(db=db, location=location, userId=userId)


# Define the location read route
@apiRouter.get("/locations/", response_model=list[schemas.Location])
def readLocations(skip: int = 0, limit: int = 100, db: Session = Depends(getDB)):
    items = crud.getLocations(db, skip=skip, limit=limit)
    return items


app.include_router(apiRouter)
