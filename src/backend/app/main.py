import uvicorn
from fastapi import FastAPI

app = FastAPI()


# Define the root route
@app.get("/")
async def root():
    return {"message": "Hello, World!"}


# Define the test route
@app.get("/test/{name}")
async def test(name):
    return {f"Hello, {name}!"}


def main():
    uvicorn.run("main:app", port=5000)


if __name__ == "__main__":
    main()
