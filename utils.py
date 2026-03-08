import PyPDF2
from docx import Document


def extract_text_from_file(uploaded_file):

    if uploaded_file.name.endswith(".pdf"):

        reader = PyPDF2.PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            t = page.extract_text()

            if t:
                text += t

        return text

    if uploaded_file.name.endswith(".docx"):

        doc = Document(uploaded_file)

        text = ""

        for p in doc.paragraphs:
            text += p.text + "\n"

        return text

    return ""


def generate_analysis_report(result):

    report = f"""
Resume Score: {result["score"]}
ATS Score: {result["ats_score"]}
Match Score: {result["match_score"]}

Email: {result["email"]}
Phone: {result["phone"]}

Skills:
{result["skills"]}

Matched Skills:
{result["matched_skills"]}

Missing Skills:
{result["missing_skills"]}

Suggestions:
{result["ats_improvement_suggestions"]}
"""

    return report