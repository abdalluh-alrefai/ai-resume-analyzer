import re

TECHNICAL_SKILLS = [
    "python", "java", "c++", "sql", "machine learning", "deep learning",
    "data analysis", "pandas", "numpy", "tensorflow", "pytorch",
    "streamlit", "flask", "django", "nlp", "excel", "power bi",
    "tableau", "git", "github", "html", "css", "javascript",
    "react", "redux", "angular", "jquery", "mongodb", "hadoop",
    "apache spark", "spark", "keras", "etl", "pl/sql", "xml",
    "json", "ajax", "oracle", "ms sql server"
]

SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "team worker", "critical thinking",
    "problem solving", "creativity", "time management", "adaptability",
    "organization", "collaboration", "presentation", "planning",
    "attention to detail", "innovative", "highly organized"
]

EDUCATION_TEACHING_SKILLS = [
    "teaching", "teacher", "classroom management", "lesson planning",
    "curriculum development", "student assessment", "proofreading",
    "spelling", "grammar", "linguistic expression", "literary analysis",
    "communication methods", "text correction", "rhetoric", "arabic grammar",
    "morphology", "language instruction", "education"
]

LOGISTICS_SKILLS = [
    "warehouse", "warehousing", "inventory", "inventory management",
    "logistics", "packing", "picking", "shipping", "supply chain",
    "cleaning equipment", "sanitation", "deep sanitation practices",
    "distribution", "operations", "storage", "quality control",
    "inspection", "record keeping", "sorting products", "forklift",
    "forklift driver", "conveyor belts", "labeling", "pallet jack operations",
    "hazardous materials", "health & safety"
]

PROJECT_MANAGEMENT_SKILLS = [
    "project management", "requirement gathering", "budget administration",
    "resource allocation", "forecasting", "process improvement",
    "ms project", "agile", "scrum", "risk management", "project governance",
    "stakeholder management", "documentation", "budgeting"
]

GENERAL_KEYWORDS = (
    TECHNICAL_SKILLS
    + SOFT_SKILLS
    + EDUCATION_TEACHING_SKILLS
    + LOGISTICS_SKILLS
    + PROJECT_MANAGEMENT_SKILLS
)

SECTION_KEYWORDS = {
    "education": ["education", "university", "bachelor", "degree", "college", "courses", "master"],
    "experience": ["experience", "employment", "work experience", "teacher", "associate", "assistant", "internship", "manager", "developer", "engineer"],
    "skills": ["skills", "technical skills", "management skills", "qualifications"],
    "projects": ["projects", "project", "achievements", "certifications", "training"],
    "contact": ["email", "phone", "address", "linkedin", "github"]
}


def normalize_text(text):
    return text.lower().strip()


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None


def extract_phone(text):
    match = re.search(r'(\+?\d[\d\s\-\(\)]{7,}\d)', text)
    return match.group(0).strip() if match else None


def extract_skills(text):
    text_lower = normalize_text(text)
    found_skills = []

    for skill in GENERAL_KEYWORDS:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))


def extract_skills_from_job_description(job_description):
    if not job_description:
        return []

    jd_lower = normalize_text(job_description)
    found_skills = []

    for skill in GENERAL_KEYWORDS:
        if skill.lower() in jd_lower:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))


def has_any_section(text, keywords):
    text_lower = normalize_text(text)
    return any(word in text_lower for word in keywords)


def calculate_resume_score(text, skills, job_skills):
    score = 0

    if len(text) > 300:
        score += 15

    if len(text) > 700:
        score += 10

    if len(skills) >= 3:
        score += 15

    if len(skills) >= 6:
        score += 10

    if has_any_section(text, SECTION_KEYWORDS["education"]):
        score += 10

    if has_any_section(text, SECTION_KEYWORDS["experience"]):
        score += 15

    if has_any_section(text, SECTION_KEYWORDS["skills"]):
        score += 10

    if has_any_section(text, SECTION_KEYWORDS["contact"]):
        score += 10

    if has_any_section(text, SECTION_KEYWORDS["projects"]):
        score += 5

    if job_skills:
        matched = len(set(skills) & set(job_skills))
        score += min(matched * 5, 10)

    return min(score, 100)


def calculate_ats_score(text, skills):
    score = 0
    text_lower = text.lower()

    if len(text) > 500:
        score += 15

    if len(skills) >= 5:
        score += 20

    if "education" in text_lower:
        score += 10

    if "experience" in text_lower or "employment" in text_lower:
        score += 20

    if "skills" in text_lower:
        score += 10

    if "projects" in text_lower:
        score += 10

    if "certifications" in text_lower or "courses" in text_lower:
        score += 5

    if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text):
        score += 5

    if re.search(r'(\+?\d[\d\s\-\(\)]{7,}\d)', text):
        score += 5

    return min(score, 100)


def calculate_match_score(resume_skills, job_skills):
    if not job_skills:
        return 0

    matched = set(resume_skills) & set(job_skills)
    score = int((len(matched) / len(job_skills)) * 100)
    return min(score, 100)


def detect_role(text):
    text_lower = normalize_text(text)

    if "front end developer" in text_lower:
        return "Front-End Developer"
    if "data engineer" in text_lower:
        return "Data Engineer"
    if "project manager" in text_lower:
        return "Project Manager"
    if "teacher" in text_lower or "arabic language" in text_lower:
        return "Teacher / Education Professional"
    if "warehouse" in text_lower:
        return "Warehouse / Logistics Professional"

    return "Professional"


def generate_resume_summary(text, skills):
    role = detect_role(text)
    top_skills = ", ".join(skills[:5]) if skills else "various relevant skills"

    return (
        f"This resume appears to belong to a {role} with experience and qualifications "
        f"that include {top_skills}. The resume contains key professional sections such as "
        f"education, work experience, and skills, and it is suitable for further tailoring "
        f"based on the target job description."
    )


def generate_resume_rewrite(text, skills, job_description=""):
    role = detect_role(text)
    top_skills = skills[:6]
    top_skills_text = ", ".join(top_skills) if top_skills else "relevant professional skills"

    if job_description.strip():
        rewrite = (
            f"Results-driven {role} with experience in {top_skills_text}. "
            f"Demonstrates a strong background in delivering high-quality work, "
            f"maintaining professional standards, and adapting experience to match job requirements. "
            f"Brings a combination of technical knowledge, practical execution, and communication skills "
            f"that can add value in fast-paced work environments."
        )
    else:
        rewrite = (
            f"Results-driven {role} with experience in {top_skills_text}. "
            f"Demonstrates a strong background in professional responsibilities, practical execution, "
            f"and continuous improvement. Brings a combination of relevant expertise, organization, "
            f"and communication skills that supports success across day-to-day operations and long-term goals."
        )

    rewrite_tips = [
        "Start your resume with a strong 2 to 4 line professional summary tailored to the target role.",
        "Use action verbs such as developed, managed, led, improved, delivered, and implemented.",
        "Include measurable achievements whenever possible, such as percentages, time saved, or revenue impact.",
        "Keep your skills section focused on the most relevant tools and competencies for the target job.",
        "Tailor your wording to match the job description without adding skills you do not actually have."
    ]

    return rewrite, rewrite_tips


def analyze_resume_basic(text, job_description=""):
    skills = extract_skills(text)
    job_skills = extract_skills_from_job_description(job_description)
    missing_skills = sorted(list(set(job_skills) - set(skills)))
    matched_skills = sorted(list(set(job_skills) & set(skills)))

    email = extract_email(text)
    phone = extract_phone(text)

    score = calculate_resume_score(text, skills, job_skills)
    ats_score = calculate_ats_score(text, skills)
    match_score = calculate_match_score(skills, job_skills)
    summary = generate_resume_summary(text, skills)
    rewritten_summary, rewrite_tips = generate_resume_rewrite(text, skills, job_description)

    strengths = []
    weaknesses = []
    suggestions = []

    if skills:
        strengths.append("The resume includes identifiable skills.")
    else:
        weaknesses.append("No clear skills were detected.")
        suggestions.append("Add a clear skills section with role-related skills.")

    if has_any_section(text, SECTION_KEYWORDS["education"]):
        strengths.append("Education information is present.")
    else:
        weaknesses.append("Education section is missing or unclear.")
        suggestions.append("Add your degree, university, and graduation year clearly.")

    if has_any_section(text, SECTION_KEYWORDS["experience"]):
        strengths.append("Work experience information is present.")
    else:
        weaknesses.append("Experience section is missing or unclear.")
        suggestions.append("Add work experience, internships, or freelance projects.")

    if has_any_section(text, SECTION_KEYWORDS["skills"]):
        strengths.append("There is a dedicated skills or qualifications section.")
    else:
        weaknesses.append("Skills section is missing or unclear.")
        suggestions.append("Create a dedicated skills section for better readability.")

    if email:
        strengths.append("Email address detected.")
    else:
        weaknesses.append("Email address is missing.")
        suggestions.append("Add a professional email address.")

    if phone:
        strengths.append("Phone number detected.")
    else:
        weaknesses.append("Phone number is missing.")
        suggestions.append("Add a phone number so employers can contact you.")

    if len(text) < 400:
        weaknesses.append("The resume content looks too short.")
        suggestions.append("Add more detail about responsibilities, achievements, and qualifications.")

    if not has_any_section(text, SECTION_KEYWORDS["projects"]):
        suggestions.append("Add projects, achievements, certifications, or training courses if relevant.")

    if missing_skills:
        suggestions.append("Include missing job-related skills only if you truly have them.")

    if not suggestions:
        suggestions.append("The resume looks good overall. Improve formatting and tailor it for each job.")

    return {
        "score": score,
        "ats_score": ats_score,
        "skills": skills,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "missing_skills": missing_skills,
        "matched_skills": matched_skills,
        "email": email,
        "phone": phone,
        "summary": summary,
        "match_score": match_score,
        "rewritten_summary": rewritten_summary,
        "rewrite_tips": rewrite_tips
    }