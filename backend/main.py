from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from  . import database, models
from .routers.weather import router as weather_router
from .routers.document import router as document_router
from .routers.textsummarize import router as textsummarize_router
from .routers.imageanalytics import router as imageanalytics_router
from .routers.agenticai import router as agenticai_router

app = FastAPI()

app.include_router(weather_router)
app.include_router(document_router)
app.include_router(textsummarize_router)
app.include_router(imageanalytics_router)
app.include_router(agenticai_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProfileSchema(BaseModel):
    id: int
    name: str
    age: int
    email: str
    marital_status: str
    country: str
    state: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

@app.get("/profiles/", response_model=List[ProfileSchema])
def get_profiles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    profiles = db.query(models.Profile).offset(skip).limit(limit).all()
    return profiles