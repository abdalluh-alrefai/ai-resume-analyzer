import streamlit as st
from datetime import datetime
from analyzer import (
    analyze_resume_basic,
    generate_resume_builder_output,
    generate_cover_letter,
    generate_resume_template_output,
)
from utils import extract_text_from_file, generate_analysis_report

st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "builder_loaded" not in st.session_state:
    st.session_state.builder_loaded = False

if "template_loaded" not in st.session_state:
    st.session_state.template_loaded = False

if "cover_loaded" not in st.session_state:
    st.session_state.cover_loaded = False

st.markdown("""
<style>
:root {
    --bg: #09111f;
    --card: #111a2e;
    --soft: #16213a;
    --border: #2a3a5c;
    --text: #eef2ff;
    --muted: #a9b5d3;
    --primary: #77a8ff;
    --accent: #8b5cf6;
}

html, body, [class*="css"] {
    font-family: Inter, system-ui, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(79,70,229,0.10), transparent 22%),
        radial-gradient(circle at top right, rgba(59,130,246,0.10), transparent 24%),
        linear-gradient(180deg, #09111f 0%, #08101d 100%);
    color: var(--text);
}

.block-container {
    max-width: 1220px;
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}

.hero {
    padding: 2.4rem;
    border-radius: 28px;
    background:
        radial-gradient(circle at top right, rgba(139,92,246,0.22), transparent 24%),
        radial-gradient(circle at top left, rgba(59,130,246,0.18), transparent 28%),
        linear-gradient(135deg, #11192d 0%, #0e1629 100%);
    border: 1px solid #2a3a5c;
    box-shadow: 0 24px 80px rgba(0,0,0,0.22);
    margin-bottom: 1.2rem;
}

.hero-title {
    font-size: 54px;
    font-weight: 800;
    line-height: 1.04;
    margin-bottom: 14px;
}

.hero-subtitle {
    font-size: 18px;
    color: #bcc7e0;
    max-width: 900px;
    line-height: 1.75;
    margin-bottom: 12px;
}

.section-title {
    font-size: 30px;
    font-weight: 800;
    margin-bottom: 6px;
}

.section-subtitle {
    color: #a9b5d3;
    margin-bottom: 14px;
}

.glass-card {
    background: rgba(17, 26, 46, 0.92);
    border: 1px solid #2a3a5c;
    border-radius: 22px;
    padding: 18px 18px 14px 18px;
    margin-bottom: 16px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.14);
}

.feature-card {
    background: linear-gradient(180deg, #111a2e 0%, #0f172a 100%);
    border: 1px solid #2a3a5c;
    border-radius: 20px;
    padding: 18px;
    height: 100%;
}

.mini-badge {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(119,168,255,0.10);
    border: 1px solid rgba(119,168,255,0.28);
    color: #d7e5ff;
    font-size: 13px;
    margin-right: 8px;
    margin-bottom: 8px;
}

.cta-box {
    background: linear-gradient(180deg, #111a2e 0%, #0d1528 100%);
    border: 1px solid #2a3a5c;
    border-radius: 20px;
    padding: 18px;
    margin-top: 12px;
    margin-bottom: 16px;
}

.stButton > button {
    border-radius: 14px;
    border: 1px solid #365080;
    background: linear-gradient(180deg, #162445 0%, #12203e 100%);
    color: white;
    font-weight: 600;
    padding: 0.6rem 1rem;
}

.stDownloadButton > button {
    border-radius: 14px;
    border: 1px solid #365080;
    background: linear-gradient(180deg, #162445 0%, #12203e 100%);
    color: white;
    font-weight: 600;
    padding: 0.6rem 1rem;
}

code {
    white-space: pre-wrap !important;
}

hr {
    border: none;
    border-top: 1px solid #2a3a5c;
    margin: 16px 0;
}
</style>
""", unsafe_allow_html=True)


def add_history_item(result, file_name: str):
    st.session_state.analysis_history.insert(0, {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "file_name": file_name,
        "resume_score": result["score"],
        "ats_score": result["ats_score"],
        "job_match": result["match_score"],
        "skills_count": len(result["skills"]),
    })


def go_to(page_name: str):
    st.session_state.page = page_name


def render_home():
    st.markdown("""
    <div class="hero">
        <div class="hero-title">AI Resume Analyzer Pro</div>
        <div class="hero-subtitle">
            A modern all-in-one resume intelligence platform for scoring, ATS optimization,
            job matching, summary rewriting, resume building, template generation,
            and tailored cover letter creation.
        </div>
        <div>
            <span class="mini-badge">ATS Optimization</span>
            <span class="mini-badge">Resume Builder</span>
            <span class="mini-badge">Cover Letter Generator</span>
            <span class="mini-badge">Template Generator</span>
            <span class="mini-badge">Dashboard</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Start Resume Analysis", use_container_width=True):
            go_to("Resume Analyzer")
            st.rerun()
    with c2:
        if st.button("Build a Resume", use_container_width=True):
            go_to("Resume Builder")
            st.rerun()
    with c3:
        if st.button("Generate Cover Letter", use_container_width=True):
            go_to("Cover Letter Generator")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""
        <div class="feature-card">
            <div class="section-title" style="font-size:24px;">Resume Analyzer</div>
            <div class="section-subtitle">
                Score resumes, detect skill gaps, analyze ATS readiness, and highlight strengths and weaknesses.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div class="feature-card">
            <div class="section-title" style="font-size:24px;">Resume Builder</div>
            <div class="section-subtitle">
                Generate structured resume drafts from scratch with clearer summaries and better formatting.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown("""
        <div class="feature-card">
            <div class="section-title" style="font-size:24px;">Cover Letters + Templates</div>
            <div class="section-subtitle">
                Create role-focused cover letters and ATS-friendly resume template outputs in multiple styles.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("""
        <div class="glass-card">
            <div class="section-title" style="font-size:24px;">Free</div>
            <div class="section-subtitle">Perfect for demos and early portfolio users.</div>
            <ul>
                <li>Resume analysis</li>
                <li>ATS scoring</li>
                <li>Resume builder</li>
                <li>Cover letter generator</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="glass-card">
            <div class="section-title" style="font-size:24px;">Pro</div>
            <div class="section-subtitle">For job seekers who want deeper optimization.</div>
            <ul>
                <li>Unlimited analysis</li>
                <li>Advanced keyword insights</li>
                <li>Template generation</li>
                <li>Saved history</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div class="glass-card">
            <div class="section-title" style="font-size:24px;">Team</div>
            <div class="section-subtitle">For coaches, recruiters, and service providers.</div>
            <ul>
                <li>Multiple resume reviews</li>
                <li>Dashboard overview</li>
                <li>Shared templates</li>
                <li>Export workflows</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cta-box">
        <div class="section-title" style="font-size:24px;">Live Demo Workflow</div>
        <div class="section-subtitle">
            Upload a resume → review ATS score and keyword gaps → rewrite the summary →
            generate a cover letter → build a polished template-ready resume draft.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_dashboard():
    st.markdown('<div class="section-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Overview of current session activity and generated analysis results.</div>', unsafe_allow_html=True)

    history = st.session_state.analysis_history
    total = len(history)
    avg_resume = int(sum(h["resume_score"] for h in history) / total) if history else 0
    avg_ats = int(sum(h["ats_score"] for h in history) / total) if history else 0
    avg_match = int(sum(h["job_match"] for h in history) / total) if history else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Analyses", total)
    with m2:
        st.metric("Avg Resume Score", avg_resume)
    with m3:
        st.metric("Avg ATS Score", avg_ats)
    with m4:
        st.metric("Avg Job Match", avg_match)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Recent Analysis History")
    if history:
        for item in history[:10]:
            st.markdown(
                f"**{item['file_name']}**  \n"
                f"- Time: {item['time']}  \n"
                f"- Resume Score: {item['resume_score']} | ATS Score: {item['ats_score']} | Job Match: {item['job_match']} | Skills: {item['skills_count']}"
            )
            st.markdown("---")
    else:
        st.write("No analyses yet. Upload a resume in the Resume Analyzer section.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_resume_analyzer():
    st.markdown('<div class="section-title">Resume Analyzer Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Upload a PDF or DOCX file and receive a complete professional analysis.</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"], key="resume_upload")
    job_description = st.text_area(
        "Optional: Paste Job Description",
        height=180,
        placeholder="Paste the target job description here to compare your resume against it."
    )

    if uploaded_file:
        text = extract_text_from_file(uploaded_file)

        if text.strip():
            result = analyze_resume_basic(text, job_description)
            add_history_item(result, uploaded_file.name)

            a, b, c, d = st.columns(4)
            with a:
                st.metric("Resume Score", result["score"])
            with b:
                st.metric("ATS Score", result["ats_score"])
            with c:
                st.metric("Job Match", result["match_score"])
            with d:
                st.metric("Skills Found", len(result["skills"]))

            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("Contact Information")
                st.write(f"**Email:** {result['email'] if result['email'] else 'Not detected'}")
                st.write(f"**Phone:** {result['phone'] if result['phone'] else 'Not detected'}")
                st.markdown('</div>', unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("Resume Summary")
                st.write(result["summary"])
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("AI Resume Rewrite")
            st.write(result["rewritten_summary"])
            st.markdown('</div>', unsafe_allow_html=True)

            c3, c4 = st.columns(2)
            with c3:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("Rewrite Tips")
                for item in result["rewrite_tips"]:
                    st.markdown(f"- {item}")
                st.markdown('</div>', unsafe_allow_html=True)

            with c4:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("ATS Improvement Suggestions")
                for item in result["ats_improvement_suggestions"]:
                    st.markdown(f"- {item}")
                st.markdown('</div>', unsafe_allow_html=True)

            c5, c6 = st.columns(2)
            with c5:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("Strengths")
                if result["strengths"]:
                    for item in result["strengths"]:
                        st.markdown(f"- {item}")
                else:
                    st.write("No major strengths detected.")
                st.markdown('</div>', unsafe_allow_html=True)

            with c6:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("Weaknesses")
                if result["weaknesses"]:
                    for item in result["weaknesses"]:
                        st.markdown(f"- {item}")
                else:
                    st.write("No major weaknesses detected.")
                st.markdown('</div>', unsafe_allow_html=True)

            c7, c8 = st.columns(2)
            with c7:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("Extracted Skills")
                if result["skills"]:
                    for skill in result["skills"]:
                        st.markdown(f"- {skill.title()}")
                else:
                    st.write("No skills detected.")
                st.markdown('</div>', unsafe_allow_html=True)

            with c8:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("Additional Suggestions")
                for item in result["suggestions"]:
                    st.markdown(f"- {item}")
                st.markdown('</div>', unsafe_allow_html=True)

            if job_description.strip():
                c9, c10 = st.columns(2)
                with c9:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.subheader("Matched Skills")
                    if result["matched_skills"]:
                        for skill in result["matched_skills"]:
                            st.markdown(f"- {skill.title()}")
                    else:
                        st.write("No matched skills found.")
                    st.markdown('</div>', unsafe_allow_html=True)

                with c10:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.subheader("Missing Skills")
                    if result["missing_skills"]:
                        for skill in result["missing_skills"]:
                            st.markdown(f"- {skill.title()}")
                    else:
                        st.write("No major missing skills detected.")
                    st.markdown('</div>', unsafe_allow_html=True)

            report = generate_analysis_report(result)

            st.download_button(
                "📥 Download Full Analysis Report",
                data=report,
                file_name="resume_analysis.txt",
                mime="text/plain"
            )
        else:
            st.error("Could not extract text from the uploaded file.")


def load_builder_example():
    st.session_state["rb_name"] = "Abdullah Alrefai"
    st.session_state["rb_title"] = "AI & Python Developer"
    st.session_state["rb_email"] = "alrefaeabdallah3@gmail.com"
    st.session_state["rb_phone"] = "+962790000000"
    st.session_state["rb_location"] = "Madaba, Jordan"
    st.session_state["rb_skills"] = "Python, Machine Learning, NLP, Streamlit, SQL, Git, GitHub, Data Analysis"
    st.session_state["rb_exp"] = (
        "Built AI-powered web apps using Python and Streamlit for document analysis and resume evaluation.\n"
        "Developed NLP-based tools for text extraction, keyword detection, ATS scoring, and AI rewrite suggestions.\n"
        "Worked on portfolio-ready freelance projects focused on automation, analytics, and user-friendly interfaces."
    )
    st.session_state["rb_edu"] = (
        "Bachelor's Degree in Artificial Intelligence, Jordan\n"
        "Completed practical projects in Python, machine learning, and data analysis."
    )
    st.session_state["rb_proj"] = (
        "AI Document Analyzer - Built a Streamlit app to analyze PDF documents, summarize content, and extract keywords.\n"
        "AI Resume Analyzer - Developed a resume scoring and ATS analysis tool with AI rewrite features.\n"
        "Completed online training in Python, machine learning, and Git/GitHub."
    )


def render_resume_builder():
    st.markdown('<div class="section-title">Resume Builder</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Generate a polished resume draft from your details.</div>', unsafe_allow_html=True)

    c0, c00 = st.columns([1, 4])
    with c0:
        if st.button("Load Example", key="load_builder_example"):
            load_builder_example()
            st.rerun()
    with c00:
        st.caption("Use the example to test the builder quickly.")

    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Full Name", key="rb_name")
        title = st.text_input("Professional Title", key="rb_title", placeholder="AI & Python Developer")
        email = st.text_input("Email", key="rb_email")
        phone = st.text_input("Phone", key="rb_phone")
    with c2:
        location = st.text_input("Location", key="rb_location")
        skills = st.text_area(
            "Skills",
            placeholder="Python, SQL, Power BI, Streamlit, Communication",
            key="rb_skills",
            height=142
        )

    experience = st.text_area("Work Experience", height=160, key="rb_exp")
    education = st.text_area("Education", height=130, key="rb_edu")
    projects = st.text_area("Projects / Certifications", height=130, key="rb_proj")

    if st.button("Generate Resume Draft", key="rb_btn"):
        summary, resume = generate_resume_builder_output(
            name, title, email, phone, location, skills, experience, education, projects
        )

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Generated Professional Summary")
        st.write(summary)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Generated Resume Draft")
        st.code(resume)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            "📄 Download Resume Draft",
            data=resume,
            file_name="resume_draft.txt",
            mime="text/plain"
        )


def load_template_example():
    st.session_state["tpl_name"] = "Abdullah Alrefai"
    st.session_state["tpl_title"] = "AI & Python Developer"
    st.session_state["tpl_email"] = "alrefaeabdallah3@gmail.com"
    st.session_state["tpl_phone"] = "+962790000000"
    st.session_state["tpl_location"] = "Madaba, Jordan"
    st.session_state["tpl_skills"] = "Python, Machine Learning, NLP, Streamlit, SQL, Git, GitHub, Data Analysis"
    st.session_state["tpl_exp"] = (
        "Built AI-powered web apps using Python and Streamlit for document analysis and resume evaluation.\n"
        "Developed NLP-based tools for text extraction, keyword detection, ATS scoring, and AI rewrite suggestions."
    )
    st.session_state["tpl_edu"] = (
        "Bachelor's Degree in Artificial Intelligence, Jordan\n"
        "Completed practical projects in Python and machine learning."
    )
    st.session_state["tpl_proj"] = (
        "AI Resume Analyzer - ATS scoring and rewrite tool.\n"
        "AI Document Analyzer - PDF analysis and summary tool."
    )


def render_templates():
    st.markdown('<div class="section-title">Resume Templates</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Generate ATS-friendly resume output in different styles.</div>', unsafe_allow_html=True)

    c0, c00 = st.columns([1, 4])
    with c0:
        if st.button("Load Example", key="load_template_example"):
            load_template_example()
            st.rerun()
    with c00:
        st.caption("Quickly populate this section with a polished sample.")

    template_style = st.selectbox(
        "Choose Template Style",
        ["Classic Professional", "Modern Minimal", "ATS Optimized"]
    )

    name = st.text_input("Template Full Name", key="tpl_name")
    title = st.text_input("Template Professional Title", key="tpl_title")
    email = st.text_input("Template Email", key="tpl_email")
    phone = st.text_input("Template Phone", key="tpl_phone")
    location = st.text_input("Template Location", key="tpl_location")
    skills = st.text_area("Template Skills", key="tpl_skills")
    experience = st.text_area("Template Work Experience", height=140, key="tpl_exp")
    education = st.text_area("Template Education", height=120, key="tpl_edu")
    projects = st.text_area("Template Projects / Certifications", height=120, key="tpl_proj")

    if st.button("Generate Template Resume", key="tpl_btn"):
        template_output = generate_resume_template_output(
            template_style=template_style,
            name=name,
            title=title,
            email=email,
            phone=phone,
            location=location,
            skills=skills,
            experience=experience,
            education=education,
            projects=projects
        )

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader(f"{template_style} Output")
        st.code(template_output)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            "📄 Download Template Resume",
            data=template_output,
            file_name="template_resume.txt",
            mime="text/plain"
        )


def load_cover_example():
    st.session_state["cl_name"] = "Abdullah Alrefai"
    st.session_state["cl_role"] = "Junior AI Engineer"
    st.session_state["cl_company"] = "TechNova"
    st.session_state["cl_skills"] = "Python, NLP, Machine Learning, SQL, Streamlit"
    st.session_state["cl_exp"] = (
        "Built AI-powered applications for document analysis and resume evaluation, "
        "with hands-on experience in machine learning, NLP, and data-driven interfaces."
    )
    st.session_state["cl_jd"] = (
        "We are looking for a Junior AI Engineer with strong Python skills, practical NLP experience, "
        "and the ability to build intelligent tools for real users."
    )


def render_cover_letter():
    st.markdown('<div class="section-title">Cover Letter Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Generate a cleaner, stronger cover letter tailored to your target role.</div>', unsafe_allow_html=True)

    c0, c00 = st.columns([1, 4])
    with c0:
        if st.button("Load Example", key="load_cover_example"):
            load_cover_example()
            st.rerun()
    with c00:
        st.caption("Use the example to preview the cover letter generator instantly.")

    name = st.text_input("Your Name", key="cl_name")
    role = st.text_input("Target Role", key="cl_role")
    company = st.text_input("Company Name", key="cl_company")
    skills = st.text_area("Key Skills", key="cl_skills", placeholder="Python, NLP, Machine Learning, SQL, Streamlit")
    experience = st.text_area("Relevant Experience", key="cl_exp", height=160)
    job_description = st.text_area("Job Description / Notes", key="cl_jd", height=160)

    if st.button("Generate Cover Letter", key="cl_btn"):
        letter = generate_cover_letter(
            name=name,
            role=role,
            company=company,
            skills=skills,
            experience=experience,
            job_description=job_description
        )

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Generated Cover Letter")
        st.code(letter)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            "📄 Download Cover Letter",
            data=letter,
            file_name="cover_letter.txt",
            mime="text/plain"
        )


with st.sidebar:
    st.markdown("## Navigation")
    page = st.radio(
        "Go to",
        ["Home", "Dashboard", "Resume Analyzer", "Resume Builder", "Resume Templates", "Cover Letter Generator"],
        index=["Home", "Dashboard", "Resume Analyzer", "Resume Builder", "Resume Templates", "Cover Letter Generator"].index(st.session_state.page)
    )
    st.session_state.page = page
    st.markdown("---")
    st.caption("AI Resume Analyzer Pro")
    st.caption("Final polished portfolio version")

if st.session_state.page == "Home":
    render_home()
elif st.session_state.page == "Dashboard":
    render_dashboard()
elif st.session_state.page == "Resume Analyzer":
    render_resume_analyzer()
elif st.session_state.page == "Resume Builder":
    render_resume_builder()
elif st.session_state.page == "Resume Templates":
    render_templates()
elif st.session_state.page == "Cover Letter Generator":
    render_cover_letter()