from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


# Define the test route
@apiRouter.get("/test/{name}", status_code=200)
async def test(name: str):
    return {f"Hello, {name}!"}


app.include_router(apiRouter)
