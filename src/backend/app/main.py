from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from locationData import LOCATION
from schemas.location import Location, LocationCreate, LocationSearch

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

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


# Define the root route
@apiRouter.get("/", status_code=200)
async def root(request: Request):
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "locations": LOCATION},
    )


# Define the user route
@apiRouter.get("/location/{ID}", status_code=200, response_model=Location)
async def getLocation(*, ID: int):
    response = [location for location in LOCATION if location["id"] == ID]
    if not response:
        raise HTTPException(status_code=404, detail=f"Location with ID {ID} not found!")
    return response[0]


# Define the search route
@apiRouter.get("/search/", status_code=200, response_model=LocationSearch)
async def searchLocation(
    *, searchword: Optional[str] = None, maxResults: Optional[int] = 4
):
    if not searchword:
        return {"results": LOCATION[:maxResults]}

    response = filter(lambda user: searchword.lower() in user["name"].lower(), LOCATION)
    return {"results": list(response)[:maxResults]}


# Define the user create route
@apiRouter.post("/location/", status_code=201, response_model=Location)
async def createLocation(*, location: LocationCreate):
    newID = len(LOCATION) + 1
    newEntry = Location(
        id=newID,
        name=location.name,
        weather=location.weather,
        url=location.url,
    )
    LOCATION.append(newEntry.dict())

    return newEntry


app.include_router(apiRouter)
