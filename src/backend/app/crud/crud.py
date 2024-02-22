from sqlalchemy.orm import Session

from app.models import models
from app.schemas import schemas


def getUser(db: Session, userId: int):
    return db.query(models.User).filter(models.User.id == userId).first()


def getUserByEmail(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def getUsers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def createUser(db: Session, user: schemas.UserCreate):
    passwordHash = user.password + "THISHASHISFAKE"
    dbUser = models.User(
        name=user.name,
        credits=user.credits,
        email=user.email,
        username=user.username,
        passwordHash=passwordHash,
    )
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser


def getLocations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Location).offset(skip).limit(limit).all()


def createUserLocation(db: Session, location: schemas.LocationCreate, userId: int):
    dbItem = models.Location(**location.dict(), owner=userId)
    db.add(dbItem)
    db.commit()
    db.refresh(dbItem)
    return dbItem
