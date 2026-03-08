# AI Resume Analyzer

AI Resume Analyzer is a Streamlit web application that analyzes resumes in PDF or DOCX format and provides smart insights such as resume scoring, ATS compatibility, skill extraction, job matching, and improvement suggestions.

## Features

- Upload resumes in PDF or DOCX format
- Extract and clean resume text
- Detect contact information
- Extract technical and non-technical skills
- Generate a resume score
- Calculate ATS compatibility score
- Compare resume with a job description
- Show matched and missing skills
- Generate a professional resume summary
- Download the full analysis report

## Tech Stack

- Python
- Streamlit
- PyPDF2
- python-docx
- Regular Expressions (re)
- NLP-style keyword extraction
- Git & GitHub

## Project Structure

```bash
ai_resume_analyzer/
│
├── app.py
├── analyzer.py
├── utils.py
├── requirements.txt
├── README.md
└── .gitignore