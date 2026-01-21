import shutil
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database, dependencies
from ..services import resume_parser, matching

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
    responses={404: {"description": "Not found"}},
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/", response_model=schemas.Candidate)
def upload_resume(
    job_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    # Verify job exists and belongs to user
    job = db.query(models.JobDescription).filter(models.JobDescription.id == job_id, models.JobDescription.recruiter_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Parse resume
    text = resume_parser.parse_resume(file_location)
    
    # Calculate Score
    # Combine relevant JD fields for matching
    jd_text = f"{job.title} {job.skills_required} {job.experience_required} {job.description}"
    score_val = matching.calculate_similarity(text, jd_text)
    
    # Create Candidate entry
    new_candidate = models.Candidate(
        name=file.filename, # Placeholder naming
        email="", # Placeholder
        phone="", # Placeholder
        resume_text=text,
        file_path=file_location,
        job_id=job_id
    )
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    # Create Score entry
    status = "Pending"
    if score_val >= 0.7:
        status = "Shortlisted"
    elif score_val >= 0.4:
        status = "Borderline"
    else:
        status = "Rejected"

    new_score = models.Score(
        candidate_id=new_candidate.id,
        similarity_score=score_val,
        rank=0, # Can be updated later or dynamically calculated
        status=status,
        feedback="Auto-generated based on similarity."
    )
    db.add(new_score)
    db.commit()
    
    # Return candidate with updated relationship (need to refresh or better re-query if eager loading not set)
    db.refresh(new_candidate)
    return new_candidate

@router.get("/{job_id}", response_model=List[schemas.Candidate])
def get_candidates(job_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    job = db.query(models.JobDescription).filter(models.JobDescription.id == job_id, models.JobDescription.recruiter_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job.candidates
