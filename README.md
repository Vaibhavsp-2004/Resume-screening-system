# AI Powered Resume Screening System

An automated resume screening system that uses NLP and Machine Learning to rank candidates based on job descriptions.

## Features
- **Recruiter Dashboard**: Manage job postings and view candidates.
- **Resume Parsing**: Supports PDF and DOCX formats.
- **AI Matching**: Uses TF-IDF and Cosine Similarity to score resumes against job requirements.
- **Fair & Unbiased**: Ranks based on content similarity, ignoring gender/race.
- **Dark Mode UI**: Modern, glassmorphism-inspired design.

## Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python, FastAPI
- **Database**: SQLite (SQLAlchemy)
- **ML/NLP**: Scikit-Learn, PyPDF2, python-docx

## Installation & Setup

### Prerequisites
- Python 3.9+
- Pip

### 1. Setup Backend
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

pip install -r requirements.txt
```

### 2. Run the Application
```bash
# From the project root (aise folder)
uvicorn backend.app.main:app --reload
```

The API will run at `http://127.0.0.1:8000`.

### 3. Open Frontend
Simply open `frontend/index.html` in your browser.
Ideally, use a live server (VS Code Live Server) or serve it using python:
```bash
cd frontend
python -m http.server 5500
```

### 4. Create Sample Data (Optional)
To generate sample resumes to test the system:
```bash
python create_samples.py
```
This will create a `sample_resumes` folder with dummy PDF/DOCX files.

## Docker Deployment

To run the entire system using Docker:
```bash
docker-compose up --build
```
This will start the backend service on port 8000. You still need to serve the frontend or open `frontend/index.html` configured to point to localhost:8000.

## Usage Guide
1. **Register**: Create a new recruiter account.
2. **Login**: Access the dashboard.
3. **Create Job**: Post a new job description (e.g., "Python Developer").
4. **Upload Resumes**: Go to the job details and upload multiple resumes.
5. **View Results**: See the ranked list of candidates immediately.

## UML Diagrams
See [UML_DIAGRAMS.md](UML_DIAGRAMS.md) for architecture and design diagrams.
