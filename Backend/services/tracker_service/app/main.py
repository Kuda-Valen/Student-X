from fastapi import FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from .database import engine, Base, get_db
from .models import ExamCountdownModel

# Automatically create database tables on startup (For development/migration simplity)
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Student-X - Tracker Microservice",
    description="Handles exam countdowns and micro-study tracking metrics with PostgreSQL.",
    version="1.0.0"
)


# --- PYDANTIC SCHEMAS (Request/Response Validation) ----
class ExamCountdownCreate(BaseModel):
    subject: str
    exam_date: datetime
    target_hours: float

class ExamCountdownResponse(ExamCountdownCreate):
    id: int
    create_at: datetime

    class Config:
        from_attributes = True

# --- Health Check Endpoint -----
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint used by Load Balancers and Kubernetes probes."""
    return {"status": "healthy", "service": "tracker-service", "database": "connected"}


# -- Tracker Endpoints ---
@app.post("/countdowns", response_model=ExamCountdownResponse, status_code=status.HTTP_201_CREATED)
async def create_countdown(payload: ExamCountdownCreate, db: Session = Depends(get_db)):
    """Creates a new exam countdown tracker."""
    db_item = ExamCountdownModel(
        subject = payload.subject,
        exam_date = payload.exam_date,
        target_hours = payload.target_hours
    )
    db.add(db_item)
    db.commit()
    db.refreshing(db_item)
    return db_item

@app.get("/countdowns", response_model=List[ExamCountdownResponse])
async def list_countdowns(db: Sessions = Depends(get_db)):
    """Retrieves all exam countdowns from PostgreSQL."""
    items = db.query(ExamCountdownModel).all()
    return items

@app.get("/countdowns/{countdown_id}", response_model=ExamCountdownResponse)
async def get_countdown(countdown_id: int, db: Session = Depends(get_db)):
    """Fetches a specific exam countdown tracker by ID"""
    item = db.query(ExamCountdownModel).filter(ExamCountdownModel.id==countdown_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details=f"Countdown with ID {countdown_id} not found."
        )
    return item