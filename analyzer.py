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
    "attention to detail", "innovative", "highly organized", "detail oriented",
    "quick learner", "team player", "self motivated", "proactive"
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

MARKETING_BUSINESS_SKILLS = [
    "marketing", "digital marketing", "sales", "business development",
    "market research", "customer service", "report writing", "microsoft office",
    "word", "powerpoint", "presentation skills", "negotiation"
]

GENERAL_KEYWORDS = (
    TECHNICAL_SKILLS
    + SOFT_SKILLS
    + EDUCATION_TEACHING_SKILLS
    + LOGISTICS_SKILLS
    + PROJECT_MANAGEMENT_SKILLS
    + MARKETING_BUSINESS_SKILLS
)

SECTION_KEYWORDS = {
    "education": ["education", "university", "bachelor", "degree", "college", "courses", "master", "diploma"],
    "experience": ["experience", "employment", "work experience", "teacher", "associate", "assistant", "internship", "manager", "developer", "engineer", "supervisor", "team leader"],
    "skills": ["skills", "technical skills", "management skills", "qualifications", "competencies", "core competencies"],
    "projects": ["projects", "project", "achievements", "certifications", "training"],
    "contact": ["email", "phone", "address", "linkedin", "github", "mobile"]
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

    return min(score, 95)


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

    if "skills" in text_lower or "competencies" in text_lower:
        score += 10

    if "projects" in text_lower:
        score += 10

    if "certifications" in text_lower or "courses" in text_lower or "training" in text_lower:
        score += 5

    if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text):
        score += 5

    if re.search(r'(\+?\d[\d\s\-\(\)]{7,}\d)', text):
        score += 5

    return min(score, 95)


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
    if "marketing" in text_lower:
        return "Marketing Professional"
    if "h.s.e" in text_lower or "safety" in text_lower:
        return "HSE / Safety Professional"

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


def generate_ats_improvement_suggestions(text, email, phone, missing_skills, job_description=""):
    suggestions = []

    if not email:
        suggestions.append("Add a professional email address to improve ATS compatibility.")

    if not phone:
        suggestions.append("Add a phone number so recruiters and ATS systems can identify complete contact information.")

    if not has_any_section(text, SECTION_KEYWORDS["skills"]):
        suggestions.append("Add a dedicated skills section with clear keywords related to your target role.")

    if not has_any_section(text, SECTION_KEYWORDS["experience"]):
        suggestions.append("Add a clear work experience section with job titles, company names, and dates.")

    if not has_any_section(text, SECTION_KEYWORDS["education"]):
        suggestions.append("Add an education section with degree, institution, and graduation details.")

    if not has_any_section(text, SECTION_KEYWORDS["projects"]):
        suggestions.append("Add projects, certifications, or training to increase keyword coverage and ATS strength.")

    if len(text) < 450:
        suggestions.append("Add more role-specific detail and measurable achievements to make the resume stronger for ATS screening.")

    if job_description.strip() and missing_skills:
        top_missing = ", ".join(missing_skills[:5])
        suggestions.append(f"Consider adding relevant job keywords if you truly have them, such as: {top_missing}.")

    if not suggestions:
        suggestions.append("The resume already has a strong ATS-friendly structure. Focus on tailoring it for each target job.")

    return suggestions


def generate_resume_builder_output(name, title, email, phone, location, skills, experience, education, projects):
    skills_list = [item.strip() for item in skills.split(",") if item.strip()]
    experience_lines = [item.strip() for item in experience.split("\n") if item.strip()]
    education_lines = [item.strip() for item in education.split("\n") if item.strip()]
    project_lines = [item.strip() for item in projects.split("\n") if item.strip()]

    top_skills = ", ".join(skills_list[:6]) if skills_list else "relevant professional skills"

    summary = (
        f"{name} is a {title} with experience in {top_skills}. "
        f"Known for delivering high-quality work, strong communication, and professional execution."
    )

    resume_text = f"""{name}
{title}
Email: {email or "your.email@example.com"}
Phone: {phone or "Your phone number"}
Location: {location or "Your location"}

PROFESSIONAL SUMMARY
{summary}

SKILLS
"""
    if skills_list:
        for item in skills_list:
            resume_text += f"- {item}\n"
    else:
        resume_text += "- Add your key skills here\n"

    resume_text += "\nWORK EXPERIENCE\n"
    if experience_lines:
        for item in experience_lines:
            resume_text += f"- {item}\n"
    else:
        resume_text += "- Add your work experience here\n"

    resume_text += "\nEDUCATION\n"
    if education_lines:
        for item in education_lines:
            resume_text += f"- {item}\n"
    else:
        resume_text += "- Add your education here\n"

    resume_text += "\nPROJECTS / CERTIFICATIONS\n"
    if project_lines:
        for item in project_lines:
            resume_text += f"- {item}\n"
    else:
        resume_text += "- Add your projects, certifications, or training here\n"

    return summary, resume_text


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
    ats_improvement_suggestions = generate_ats_improvement_suggestions(
        text=text,
        email=email,
        phone=phone,
        missing_skills=missing_skills,
        job_description=job_description
    )

    strengths = []
    weaknesses = []
    suggestions = []

    if skills:
        strengths.append("Relevant skills were detected in the resume.")
    else:
        weaknesses.append("No clear skills were detected.")
        suggestions.append("Add a clear skills section with role-related technologies and competencies.")

    if has_any_section(text, SECTION_KEYWORDS["education"]):
        strengths.append("Education section is present.")
    else:
        weaknesses.append("Education section is missing or unclear.")
        suggestions.append("Add your degree, institution, and graduation details.")

    if has_any_section(text, SECTION_KEYWORDS["experience"]):
        strengths.append("Work experience section is present.")
    else:
        weaknesses.append("Work experience section is missing or unclear.")
        suggestions.append("Add job titles, company names, dates, and responsibilities.")

    if has_any_section(text, SECTION_KEYWORDS["skills"]):
        strengths.append("Skills or competencies section is present.")
    else:
        weaknesses.append("Skills section is missing or unclear.")
        suggestions.append("Create a dedicated skills section to improve readability and ATS matching.")

    if email:
        strengths.append("Email address was detected.")
    else:
        weaknesses.append("Email address is missing.")
        suggestions.append("Add a professional email address.")

    if phone:
        strengths.append("Phone number was detected.")
    else:
        weaknesses.append("Phone number is missing.")
        suggestions.append("Add a phone number for easier recruiter contact.")

    if len(text) < 400:
        weaknesses.append("Resume content appears too short.")
        suggestions.append("Add more measurable achievements, responsibilities, and role-specific details.")

    if not has_any_section(text, SECTION_KEYWORDS["projects"]):
        weaknesses.append("Projects or certifications section is missing or limited.")
        suggestions.append("Add projects, certifications, or training courses to strengthen the resume.")

    if job_description.strip() and not matched_skills:
        weaknesses.append("No strong overlap with the provided job description was found.")
        suggestions.append("Tailor your resume to the target job description using relevant keywords.")

    if not suggestions:
        suggestions.append("The resume looks solid overall. Tailor it for each role to improve results.")

    return {
        "score": score,
        "ats_score": ats_score,
        "skills": skills,
        "missing_skills": missing_skills,
        "matched_skills": matched_skills,
        "email": email,
        "phone": phone,
        "summary": summary,
        "match_score": match_score,
        "rewritten_summary": rewritten_summary,
        "rewrite_tips": rewrite_tips,
        "ats_improvement_suggestions": ats_improvement_suggestions,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }