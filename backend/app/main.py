from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from . import models, database
from .routers import auth, jobs, resumes

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI Powered Resume Screening System")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500", # Live Server default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(resumes.router)

# Serve Frontend
# Logic to find frontend directory whether in Docker or Local
# Local: internal architecture is backend/app/main.py, frontend is at ../../frontend from main.py
# Docker: /app/app/main.py, frontend is at /app/frontend

# Try determining path dynamically
current_file_dir = os.path.dirname(os.path.abspath(__file__)) # .../app
backend_dir = os.path.dirname(current_file_dir) # .../backend (local) or /app (docker potentially if copy structure differs)

# In Dockerfile: COPY ./backend/app /app/app -> so main.py is /app/app/main.py. dirname is /app/app. dirname is /app.
# And COPY ./frontend /app/frontend -> so /app/frontend.
# So if we go up 2 levels from main.py, we are at /app.
# Join with 'frontend' -> /app/frontend. Correct.

# Local: .../aise/backend/app/main.py -> up 2 levels -> .../aise/backend.
# Frontend is .../aise/frontend.
# So locally we need to go up 3 levels?
# .../aise/backend/app/main.py
# 1. .../aise/backend/app
# 2. .../aise/backend
# 3. .../aise
# Join 'frontend' -> .../aise/frontend.

# So there is a mismatch. Docker: 2 levels deep from root? No.
# Docker: /app/app/main.py.
# 1. /app/app
# 2. /app
# 3. / (root) -> join frontend -> /frontend. WRONG.

# Let's check explicitly for Docker environment or specific paths.
frontend_path = "/app/frontend" # Default Docker path
if not os.path.exists(frontend_path):
    # Fallback to local relative path: ../../../frontend
    # .../aise/backend/app/main.py -> .../aise/frontend
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend")

# Ensure uploads directory exists
uploads_path = "uploads"
if not os.path.exists(uploads_path):
    os.makedirs(uploads_path)

app.mount("/uploads", StaticFiles(directory=uploads_path), name="uploads")

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print(f"WARNING: Frontend directory not found. Expected at {frontend_path}")

@app.get("/api-status")
def read_root():
    return {"message": "Welcome to AI Resume Screening System API"}
