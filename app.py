import streamlit as st
from utils import extract_text_from_file, generate_analysis_report
from analyzer import analyze_resume_basic, generate_resume_builder_output

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 10px;
}
.subtitle {
    font-size: 18px;
    color: #aaaaaa;
    margin-bottom: 25px;
}
.card {
    background-color: #111827;
    padding: 20px;
    border-radius: 14px;
    margin-top: 10px;
    margin-bottom: 15px;
    border: 1px solid #1f2937;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Analyze resumes, improve ATS score, compare with job descriptions, and generate AI resume drafts.</div>',
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["Resume Analyzer", "AI Resume Builder"])

with tab1:
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

    job_description = st.text_area(
        "Optional: Paste Job Description",
        height=150
    )

    if uploaded_file:
        text = extract_text_from_file(uploaded_file)

        if text.strip():
            result = analyze_resume_basic(text, job_description)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Resume Score", result["score"])
            with col2:
                st.metric("ATS Score", result["ats_score"])
            with col3:
                st.metric("Job Match", result["match_score"])

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Contact Information")
            email = result["email"] if result["email"] else "Not detected"
            phone = result["phone"] if result["phone"] else "Not detected"
            st.write(f"**Email:** {email}")
            st.write(f"**Phone:** {phone}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Resume Summary")
            st.write(result["summary"])
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("AI Resume Rewrite")
            st.write(result["rewritten_summary"])
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Rewrite Tips")
            for tip in result["rewrite_tips"]:
                st.markdown(f"- {tip}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Extracted Skills")
            skills = result["skills"]
            if skills:
                for skill in skills:
                    st.markdown(f"- {skill.title()}")
            else:
                st.write("No skills detected.")
            st.markdown('</div>', unsafe_allow_html=True)

            if job_description.strip():
                col4, col5 = st.columns(2)

                with col4:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.subheader("Matched Skills")
                    if result["matched_skills"]:
                        for skill in result["matched_skills"]:
                            st.markdown(f"- {skill.title()}")
                    else:
                        st.write("No matched skills found.")
                    st.markdown('</div>', unsafe_allow_html=True)

                with col5:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.subheader("Missing Skills")
                    if result["missing_skills"]:
                        for skill in result["missing_skills"]:
                            st.markdown(f"- {skill.title()}")
                    else:
                        st.write("No major missing skills detected.")
                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("ATS Improvement Suggestions")
            for suggestion in result["ats_improvement_suggestions"]:
                st.markdown(f"- {suggestion}")
            st.markdown('</div>', unsafe_allow_html=True)

            report = generate_analysis_report(result)

            st.download_button(
                "Download Report",
                data=report,
                file_name="resume_analysis.txt"
            )
        else:
            st.error("Could not extract text from the uploaded file.")

with tab2:
    st.header("AI Resume Builder")
    st.write("Fill in your details and generate a simple resume draft that you can copy, edit, and improve.")

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

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Generated Summary")
        st.write(summary)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Generated Resume")
        st.text(resume)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            "Download Resume Draft",
            data=resume,
            file_name="resume.txt"
        )