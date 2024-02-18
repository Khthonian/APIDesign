from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ["http://localhost:3000", "localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the root route
@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello, Charlie!"}


# Define the test route
@app.get("/test/{name}")
async def test(name):
    return {f"Hello, {name}!"}
