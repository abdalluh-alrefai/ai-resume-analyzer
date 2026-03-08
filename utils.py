import PyPDF2
from docx import Document


def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"

        return text

    if uploaded_file.name.endswith(".docx"):
        doc = Document(uploaded_file)
        text = ""

        for p in doc.paragraphs:
            text += p.text + "\n"

        return text

    return ""


def generate_analysis_report(result):
    email = result["email"] if result["email"] else "Not detected"
    phone = result["phone"] if result["phone"] else "Not detected"

    report = f"""
Resume Score: {result["score"]}
ATS Score: {result["ats_score"]}
Match Score: {result["match_score"]}

Email: {email}
Phone: {phone}

Summary:
{result["summary"]}

AI Resume Rewrite:
{result["rewritten_summary"]}

Skills:
{", ".join(result["skills"])}

Matched Skills:
{", ".join(result["matched_skills"])}

Missing Skills:
{", ".join(result["missing_skills"])}

ATS Suggestions:
{chr(10).join("- " + s for s in result["ats_improvement_suggestions"])}
"""

    return report