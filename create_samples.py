import os
from fpdf import FPDF
from docx import Document

os.makedirs("sample_resumes", exist_ok=True)

resumes = [
    {
        "filename": "python_dev_fullstack.pdf",
        "content": "John Doe\nPython Full Stack Developer\nSkills: Python, Django, FastAPI, React, SQL.\nExperience: 5 years building web apps. Expert in REST APIs."
    },
    {
        "filename": "data_scientist.docx",
        "content": "Jane Smith\nData Scientist\nSkills: Python, Pandas, Scikit-learn, TensorFlow, SQL.\nExperience: 3 years in ML and AI. Strong math background."
    },
    {
        "filename": "java_developer.pdf",
        "content": "Bob Wilson\nJava Developer\nSkills: Java, Spring Boot, Hibernate, MySQL.\nExperience: 4 years in enterprise software."
    },
    {
        "filename": "fresher_python.docx",
        "content": "Alice Brown\nFresher\nSkills: Python, HTML, CSS.\nEducation: B.Tech Computer Science.\nLooking for entry level python developer roles."
    }
]

def create_pdf(filename, text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(os.path.join("sample_resumes", filename))

def create_docx(filename, text):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(os.path.join("sample_resumes", filename))

for r in resumes:
    if r["filename"].endswith(".pdf"):
        create_pdf(r["filename"], r["content"])
    else:
        create_docx(r["filename"], r["content"])

print("Sample resumes created in 'sample_resumes' folder.")
