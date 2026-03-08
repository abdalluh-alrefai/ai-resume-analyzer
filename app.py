import streamlit as st
from utils import extract_text_from_file, generate_analysis_report
from analyzer import analyze_resume_basic, generate_resume_builder_output

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.markdown("""
<style>
.main-title{
font-size:42px;
font-weight:700;
}

.subtitle{
font-size:18px;
color:#aaa;
}

.card{
background:#111827;
padding:20px;
border-radius:12px;
margin-top:10px;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title">AI Resume Analyzer</div>', unsafe_allow_html=True)

st.markdown(
'<div class="subtitle">Analyze resumes, improve ATS score, compare with job descriptions and generate AI resume drafts.</div>',
unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["Resume Analyzer", "AI Resume Builder"])

# ---------------------------------
# Resume Analyzer
# ---------------------------------

with tab1:

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

    job_description = st.text_area(
        "Optional: Paste Job Description",
        height=150
    )

    if uploaded_file:

        text = extract_text_from_file(uploaded_file)

        result = analyze_resume_basic(text, job_description)

        col1, col2, col3 = st.columns(3)

        col1.metric("Resume Score", result["score"])
        col2.metric("ATS Score", result["ats_score"])
        col3.metric("Job Match", result["match_score"])

        st.markdown("### Contact Information")
        st.write("Email:", result["email"])
        st.write("Phone:", result["phone"])

        st.markdown("### Resume Summary")
        st.write(result["summary"])

        st.markdown("### AI Resume Rewrite")
        st.write(result["rewritten_summary"])

        st.markdown("### Rewrite Tips")

        for tip in result["rewrite_tips"]:
            st.write("-", tip)

        st.markdown("### Extracted Skills")

        st.write(result["skills"])

        if job_description:

            st.markdown("### Matched Skills")
            st.write(result["matched_skills"])

            st.markdown("### Missing Skills")
            st.write(result["missing_skills"])

        st.markdown("### ATS Improvement Suggestions")

        for s in result["ats_improvement_suggestions"]:
            st.write("-", s)

        report = generate_analysis_report(result)

        st.download_button(
            "Download Report",
            data=report,
            file_name="resume_analysis.txt"
        )


# ---------------------------------
# Resume Builder
# ---------------------------------

with tab2:

    st.header("AI Resume Builder")

    name = st.text_input("Full Name")
    title = st.text_input("Professional Title")

    email = st.text_input("Email")
    phone = st.text_input("Phone")

    location = st.text_input("Location")

    skills = st.text_area(
        "Skills",
        placeholder="Python, SQL, Excel, Communication"
    )

    experience = st.text_area(
        "Work Experience",
        height=150
    )

    education = st.text_area(
        "Education",
        height=120
    )

    projects = st.text_area(
        "Projects / Certifications",
        height=120
    )

    if st.button("Generate Resume Draft"):

        summary, resume = generate_resume_builder_output(
            name,
            title,
            email,
            phone,
            location,
            skills,
            experience,
            education,
            projects
        )

        st.markdown("### Generated Summary")

        st.write(summary)

        st.markdown("### Generated Resume")

        st.text(resume)

        st.download_button(
            "Download Resume Draft",
            data=resume,
            file_name="resume.txt"
        )