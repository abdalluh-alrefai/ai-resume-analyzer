import re
import PyPDF2
from docx import Document


def clean_extracted_text(text):
    if not text:
        return ""

    text = text.replace("\t", " ")
    text = re.sub(r"\r", "\n", text)
    text = re.sub(r"\n{2,}", "\n", text)

    text = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", text)
    text = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", text)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

    text = re.sub(r"[ ]{2,}", " ", text)

    return text.strip()


def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return clean_extracted_text(text)
    except Exception as e:
        return f"Error reading PDF: {e}"


def extract_text_from_docx(uploaded_file):
    try:
        document = Document(uploaded_file)
        text = "\n".join([para.text for para in document.paragraphs if para.text.strip()])
        return clean_extracted_text(text)
    except Exception as e:
        return f"Error reading DOCX: {e}"


def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    if file_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)

    return "Unsupported file type. Please upload a PDF or DOCX file."


def generate_analysis_report(result):
    lines = [
        "AI Resume Analyzer Report",
        "=" * 30,
        "",
        f"Resume Score: {result['score']}/100",
        f"ATS Compatibility Score: {result['ats_score']}%",
        f"Resume Match Score: {result['match_score']}%",
        "",
        "Contact Information",
        "-" * 20,
        f"Email: {result['email'] if result['email'] else 'Not detected'}",
        f"Phone: {result['phone'] if result['phone'] else 'Not detected'}",
        "",
        "Resume Summary",
        "-" * 20,
        result["summary"],
        "",
        "AI Resume Rewrite",
        "-" * 20,
        result["rewritten_summary"],
        "",
        "Rewrite Tips",
        "-" * 20,
    ]

    for item in result["rewrite_tips"]:
        lines.append(f"- {item}")

    lines.extend([
        "",
        "ATS Improvement Suggestions",
        "-" * 20,
    ])

    for item in result["ats_improvement_suggestions"]:
        lines.append(f"- {item}")

    lines.extend([
        "",
        "Extracted Skills",
        "-" * 20,
        ", ".join(result["skills"]) if result["skills"] else "No skills detected",
        "",
        "Matched Skills",
        "-" * 20,
        ", ".join(result["matched_skills"]) if result["matched_skills"] else "No matched skills",
        "",
        "Missing Skills / Keywords",
        "-" * 20,
        ", ".join(result["missing_skills"]) if result["missing_skills"] else "No major missing skills detected",
        "",
        "Strengths",
        "-" * 20,
    ])

    for item in result["strengths"]:
        lines.append(f"- {item}")

    lines.extend(["", "Weaknesses", "-" * 20])

    if result["weaknesses"]:
        for item in result["weaknesses"]:
            lines.append(f"- {item}")
    else:
        lines.append("- No major weaknesses detected")

    lines.extend(["", "Suggestions", "-" * 20])

    for item in result["suggestions"]:
        lines.append(f"- {item}")

    return "\n".join(lines)