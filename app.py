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
        color: #b0b0b0;
        margin-bottom: 25px;
    }
    .card {
        background-color: #111827;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #2a2f3a;
        margin-bottom: 15px;
    }
    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📄 AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Analyze resumes, improve ATS score, compare with job descriptions, rewrite summaries, and build a resume draft from scratch.</div>',
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["Resume Analyzer", "AI Resume Builder"])

with tab1:
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"], key="resume_uploader")

    job_description = st.text_area(
        "Optional: Paste Job Description",
        placeholder="Paste the job description here to compare it with the resume...",
        height=180,
        key="job_description"
    )

    if uploaded_file is not None:
        text = extract_text_from_file(uploaded_file)

        if text and not text.startswith("Error") and not text.startswith("Unsupported"):
            result = analyze_resume_basic(text, job_description)
            report_text = generate_analysis_report(result)

            st.markdown('<div class="section-title">Extracted Resume Text</div>', unsafe_allow_html=True)
            st.text_area("Resume Content", text, height=240)

            st.markdown('<div class="section-title">Analysis Dashboard</div>', unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Resume Score", f"{result['score']}/100")

            with col2:
                st.metric("ATS Compatibility", f"{result['ats_score']}%")

            with col3:
                if job_description.strip():
                    st.metric("Job Match", f"{result['match_score']}%")
                else:
                    st.metric("Job Match", "N/A")

            with col4:
                st.metric("Skills Found", len(result["skills"]))

            col5, col6 = st.columns(2)

            with col5:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Contact Information")
                st.write(f"**Email:** {result['email'] if result['email'] else 'Not detected'}")
                st.write(f"**Phone:** {result['phone'] if result['phone'] else 'Not detected'}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col6:
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
            for item in result["rewrite_tips"]:
                st.write(f"- {item}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Extracted Skills")
            if result["skills"]:
                st.write(", ".join(result["skills"]))
            else:
                st.write("No skills detected")
            st.markdown('</div>', unsafe_allow_html=True)

            if job_description.strip():
                col7, col8 = st.columns(2)

                with col7:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.subheader("Matched Skills")
                    if result["matched_skills"]:
                        st.write(", ".join(result["matched_skills"]))
                    else:
                        st.write("No matched skills found")
                    st.markdown('</div>', unsafe_allow_html=True)

                with col8:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.subheader("Missing Skills / Keywords")
                    if result["missing_skills"]:
                        st.write(", ".join(result["missing_skills"]))
                    else:
                        st.write("No major missing skills detected")
                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("ATS Improvement Suggestions")
            for item in result["ats_improvement_suggestions"]:
                st.write(f"- {item}")
            st.markdown('</div>', unsafe_allow_html=True)

            col9, col10 = st.columns(2)

            with col9:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Strengths")
                if result["strengths"]:
                    for item in result["strengths"]:
                        st.write(f"- {item}")
                else:
                    st.write("No strengths detected")
                st.markdown('</div>', unsafe_allow_html=True)

            with col10:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Weaknesses")
                if result["weaknesses"]:
                    for item in result["weaknesses"]:
                        st.write(f"- {item}")
                else:
                    st.write("No major weaknesses detected")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Suggestions")
            if result["suggestions"]:
                for item in result["suggestions"]:
                    st.write(f"- {item}")
            else:
                st.write("No suggestions available")
            st.markdown('</div>', unsafe_allow_html=True)

            st.download_button(
                label="📥 Download Analysis Report",
                data=report_text,
                file_name="resume_analysis.txt",
                mime="text/plain"
            )

        else:
            st.error(text if text else "Could not extract text from the uploaded file.")

with tab2:
    st.markdown('<div class="section-title">AI Resume Builder</div>', unsafe_allow_html=True)
    st.write("Fill in your details and generate a simple resume draft that you can copy, edit, and improve.")

    col1, col2 = st.columns(2)

    with col1:
        builder_name = st.text_input("Full Name")
        builder_title = st.text_input("Professional Title")
        builder_email = st.text_input("Email")
        builder_phone = st.text_input("Phone")

    with col2:
        builder_location = st.text_input("Location")
        builder_skills = st.text_area(
            "Skills",
            placeholder="Python, SQL, Excel, Communication, Power BI"
        )

    builder_experience = st.text_area(
        "Work Experience",
        placeholder="Data Analyst at ABC Company - Built dashboards and automated reports\nIntern at XYZ - Cleaned and analyzed sales data",
        height=140
    )

    builder_education = st.text_area(
        "Education",
        placeholder="BSc in Computer Science - University of Jordan\nGoogle Data Analytics Certificate",
        height=120
    )

    builder_projects = st.text_area(
        "Projects / Certifications",
        placeholder="Built an AI Resume Analyzer using Python and Streamlit\nCreated a sales dashboard in Power BI",
        height=120
    )

    if st.button("Generate Resume Draft"):
        summary_text, generated_resume = generate_resume_builder_output(
            name=builder_name.strip() or "Your Name",
            title=builder_title.strip() or "Your Professional Title",
            email=builder_email.strip(),
            phone=builder_phone.strip(),
            location=builder_location.strip(),
            skills=builder_skills,
            experience=builder_experience,
            education=builder_education,
            projects=builder_projects
        )

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Generated Professional Summary")
        st.write(summary_text)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Generated Resume Draft")
        st.markdown(generated_resume)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            label="📄 Download Resume Draft",
            data=generated_resume,
            file_name="generated_resume.md",
            mime="text/markdown"
        )