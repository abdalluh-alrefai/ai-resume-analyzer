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

st.markdown("""
<style>
:root {
    --bg: #0b1020;
    --card: #121a2b;
    --soft: #1a2440;
    --border: #263252;
    --text: #eef2ff;
    --muted: #aab6d3;
    --primary: #6ea8fe;
    --accent: #8b5cf6;
    --success: #22c55e;
}

html, body, [class*="css"]  {
    font-family: Inter, system-ui, sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #0b1020 0%, #0a0f1d 100%);
    color: var(--text);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.hero {
    padding: 2.2rem;
    border-radius: 24px;
    background:
        radial-gradient(circle at top right, rgba(139,92,246,0.25), transparent 25%),
        radial-gradient(circle at top left, rgba(110,168,254,0.20), transparent 30%),
        linear-gradient(135deg, #11192d 0%, #0f172a 100%);
    border: 1px solid #263252;
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
    margin-bottom: 1.2rem;
}

.hero-title {
    font-size: 52px;
    font-weight: 800;
    line-height: 1.05;
    margin-bottom: 14px;
}

.hero-subtitle {
    font-size: 18px;
    color: #b9c3df;
    max-width: 850px;
    line-height: 1.7;
    margin-bottom: 8px;
}

.section-title {
    font-size: 30px;
    font-weight: 800;
    margin-top: 6px;
    margin-bottom: 8px;
}

.section-subtitle {
    color: #aab6d3;
    margin-bottom: 14px;
}

.glass-card {
    background: rgba(18, 26, 43, 0.9);
    border: 1px solid #263252;
    border-radius: 20px;
    padding: 18px 18px 14px 18px;
    margin-bottom: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
}

.feature-card {
    background: linear-gradient(180deg, #121a2b 0%, #10172a 100%);
    border: 1px solid #263252;
    border-radius: 18px;
    padding: 18px;
    height: 100%;
}

.metric-box {
    background: linear-gradient(180deg, #121a2b 0%, #0f172a 100%);
    border: 1px solid #263252;
    border-radius: 18px;
    padding: 10px;
}

.badge {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(110,168,254,0.12);
    border: 1px solid rgba(110,168,254,0.35);
    color: #d8e6ff;
    font-size: 13px;
    margin-right: 8px;
    margin-bottom: 8px;
}

hr {
    border: none;
    border-top: 1px solid #263252;
    margin: 18px 0;
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


def render_home():
    st.markdown("""
    <div class="hero">
        <div class="hero-title">AI Resume Analyzer Pro</div>
        <div class="hero-subtitle">
            Analyze resumes, improve ATS compatibility, compare with job descriptions,
            rewrite summaries, generate cover letters, and build polished resume drafts
            with a modern all-in-one workflow.
        </div>
        <div>
            <span class="badge">ATS Optimization</span>
            <span class="badge">Resume Builder</span>
            <span class="badge">Cover Letter Generator</span>
            <span class="badge">Template Generator</span>
            <span class="badge">Job Match Analysis</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="section-title" style="font-size:22px;">Resume Analyzer</div>
            <div class="section-subtitle">Score resumes, detect skills, identify strengths and weaknesses, and improve ATS compatibility.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="section-title" style="font-size:22px;">Resume Builder</div>
            <div class="section-subtitle">Generate structured resume drafts from your details and export them instantly.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="section-title" style="font-size:22px;">Cover Letter + Templates</div>
            <div class="section-subtitle">Create cover letters and ATS-friendly template outputs tailored to your role.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("""
        <div class="glass-card">
            <div class="section-title" style="font-size:24px;">Free</div>
            <div class="section-subtitle">For portfolio demos and initial users.</div>
            <ul>
                <li>Resume analysis</li>
                <li>ATS score</li>
                <li>Resume builder</li>
                <li>Cover letter generator</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="glass-card">
            <div class="section-title" style="font-size:24px;">Pro</div>
            <div class="section-subtitle">For serious job seekers and power users.</div>
            <ul>
                <li>Unlimited analyses</li>
                <li>Saved history</li>
                <li>Advanced keyword suggestions</li>
                <li>Premium templates</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div class="glass-card">
            <div class="section-title" style="font-size:24px;">Team</div>
            <div class="section-subtitle">For recruiters, coaches, and agencies.</div>
            <ul>
                <li>Multiple resumes</li>
                <li>Central dashboard</li>
                <li>Shared templates</li>
                <li>Export workflows</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <div class="section-title" style="font-size:24px;">Live Demo Workflow</div>
        <div class="section-subtitle">
            1. Upload a resume → 2. Review ATS & skill gaps → 3. Rewrite summary →
            4. Generate a cover letter → 5. Build a template-ready resume draft.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_dashboard():
    st.markdown('<div class="section-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Overview of your current session analyses and generated assets.</div>', unsafe_allow_html=True)

    history = st.session_state.analysis_history
    total_analyses = len(history)
    avg_resume = int(sum(h["resume_score"] for h in history) / total_analyses) if history else 0
    avg_ats = int(sum(h["ats_score"] for h in history) / total_analyses) if history else 0
    avg_match = int(sum(h["job_match"] for h in history) / total_analyses) if history else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Analyses", total_analyses)
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
    st.markdown('<div class="section-subtitle">Upload a PDF or DOCX resume and receive a complete professional analysis.</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"], key="resume_upload")
    job_description = st.text_area("Optional: Paste Job Description", height=180, key="job_desc")

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


def render_resume_builder():
    st.markdown('<div class="section-title">Resume Builder</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Generate a polished resume draft from your information.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Full Name", key="rb_name")
        title = st.text_input("Professional Title", key="rb_title")
        email = st.text_input("Email", key="rb_email")
        phone = st.text_input("Phone", key="rb_phone")
    with c2:
        location = st.text_input("Location", key="rb_location")
        skills = st.text_area("Skills", placeholder="Python, SQL, Power BI, Streamlit, Communication", key="rb_skills", height=142)

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


def render_templates():
    st.markdown('<div class="section-title">Resume Templates</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Generate ATS-friendly resume output in different styles.</div>', unsafe_allow_html=True)

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


def render_cover_letter():
    st.markdown('<div class="section-title">Cover Letter Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Generate a tailored cover letter from your resume information and job target.</div>', unsafe_allow_html=True)

    name = st.text_input("Your Name", key="cl_name")
    role = st.text_input("Target Role", key="cl_role")
    company = st.text_input("Company Name", key="cl_company")
    skills = st.text_area("Key Skills", key="cl_skills", placeholder="Python, SQL, Dashboarding, Communication")
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
    st.caption("Modern portfolio-grade version")

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