from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Integer, default=True) # 1 for active, 0 for inactive

    jobs = relationship("JobDescription", back_populates="recruiter", cascade="all, delete-orphan")


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    department = Column(String)
    skills_required = Column(Text) # JSON or comma-separated string
    experience_required = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    recruiter_id = Column(Integer, ForeignKey("users.id"))

    recruiter = relationship("User", back_populates="jobs")
    candidates = relationship("Candidate", back_populates="job", cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String)
    phone = Column(String)
    resume_text = Column(Text) # Extracted text
    file_path = Column(String) # Path to the stored file
    upload_date = Column(DateTime, default=datetime.utcnow)
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))

    job = relationship("JobDescription", back_populates="candidates")
    scores = relationship("Score", back_populates="candidate", cascade="all, delete-orphan")


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    similarity_score = Column(Float)
    rank = Column(Integer)
    status = Column(String, default="Pending") # Shortlisted, Borderline, Rejected
    feedback = Column(Text) # Logging feedback

    candidate = relationship("Candidate", back_populates="scores")
