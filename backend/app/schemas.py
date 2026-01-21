from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    # Enable ORM mode for Pydantic v2
    model_config = ConfigDict(from_attributes=True)

# Job Schemas
class JobBase(BaseModel):
    title: str
    department: str
    skills_required: str
    experience_required: str
    description: str

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    created_at: datetime
    recruiter_id: int

    # Enable ORM mode for Pydantic v2
    model_config = ConfigDict(from_attributes=True)

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Score Schema
class ScoreBase(BaseModel):
    similarity_score: float
    rank: int
    status: str
    feedback: Optional[str] = None

class Score(ScoreBase):
    id: int
    candidate_id: int

    # Enable ORM mode for Pydantic v2
    model_config = ConfigDict(from_attributes=True)

# Candidate Schema
class CandidateBase(BaseModel):
    name: str # extracted or provided
    email: str 
    phone: str 
    resume_text: str

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    id: int
    file_path: str
    upload_date: datetime
    job_id: int
    scores: List[Score] = []

    # Enable ORM mode for Pydantic v2
    model_config = ConfigDict(from_attributes=True)
