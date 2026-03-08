import streamlit as st
from utils import extract_text_from_file, generate_analysis_report
from analyzer import analyze_resume_basic

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
    .small-label {
        color: #9ca3af;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📄 AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Upload a resume in PDF or DOCX format and get smart analysis, matching, and improvement suggestions.</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

job_description = st.text_area(
    "Optional: Paste Job Description",
    placeholder="Paste the job description here to compare it with the resume...",
    height=180
)

if uploaded_file is not None:
    text = extract_text_from_file(uploaded_file)

    if text and not text.startswith("Error") and not text.startswith("Unsupported"):
        result = analyze_resume_basic(text, job_description)

        report_text = generate_analysis_report(
            result=result,
            summary_text=result["summary"],
            matched_skills=result["matched_skills"],
            missing_skills=result["missing_skills"],
            match_score=result["match_score"]
        )

        st.markdown('<div class="section-title">Extracted Resume Text</div>', unsafe_allow_html=True)
        st.text_area("Resume Content", text, height=260)

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
                st.subheader("Missing Skills")
                if result["missing_skills"]:
                    st.write(", ".join(result["missing_skills"]))
                else:
                    st.write("No major missing skills detected")
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