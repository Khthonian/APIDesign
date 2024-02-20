from typing import Optional

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import User, UserCreate, UserSearch

app = FastAPI()


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


# Define a toy database
USERS = [
    {
        "id": 1,
        "name": "John Smith",
        "credits": 1000,
        "username": "JSmith10",
    },
    {
        "id": 2,
        "name": "Jack Smith",
        "credits": 2000,
        "username": "JSmith20",
    },
    {
        "id": 3,
        "name": "Jill Smith",
        "credits": 3000,
        "username": "JSmith30",
    },
    {
        "id": 4,
        "name": "Jane Smith",
        "credits": 4000,
        "username": "JSmith40",
    },
]


# Define the root route
@apiRouter.get("/", status_code=200)
async def root():
    return {"message": "Hello, Charlie!"}


# Define the user route
@apiRouter.get("/user/{ID}", status_code=200, response_model=User)
async def getUser(*, ID: int):
    response = [user for user in USERS if user["id"] == ID]
    if response:
        return response[0]


# Define the search route
@apiRouter.get("/search/", status_code=200, response_model=UserSearch)
async def searchUser(
    *, searchword: Optional[str] = None, maxResults: Optional[int] = 4
):
    if not searchword:
        return {"results": USERS[:maxResults]}

    response = filter(
        lambda user: searchword.lower() in user["username"].lower(), USERS
    )
    return {"results": list(response)[:maxResults]}


# Define the user create route
@apiRouter.post("/user/", status_code=201, response_model=User)
async def createUser(*, user: UserCreate):
    newID = len(USERS) + 1
    newEntry = User(
        id=newID,
        name=user.name,
        credits=user.credits,
        username=user.username,
    )
    USERS.append(newEntry.dict())

    return newEntry


app.include_router(apiRouter)
