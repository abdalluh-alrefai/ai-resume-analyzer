import streamlit as st
from utils import extract_text_from_file
from analyzer import analyze_resume_basic, generate_resume_builder_output

from database import init_db, update_usage, get_usage
from auth import login_page, signup_page

init_db()

st.set_page_config(page_title="AI Resume Analyzer SaaS", layout="wide")

# SESSION
if "user" not in st.session_state:
    st.session_state["user"] = None


# LANDING PAGE
def landing_page():

    st.title("AI Resume Analyzer")

    st.write("""
Analyze resumes, improve ATS score, compare with job descriptions,
rewrite summaries, and build resumes with AI.
""")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            st.session_state["page"] = "login"
            st.rerun()

    with col2:
        if st.button("Sign Up"):
            st.session_state["page"] = "signup"
            st.rerun()

    st.markdown("---")

    st.header("Pricing")

    st.write("""
Free Plan
- 1 resume per day

Pro Plan
- Unlimited resumes
- AI Resume Builder
- $5 / month
""")


# ANALYZER
def analyzer_page():

    user = st.session_state["user"]

    user_id = user[0]
    plan = user[3]

    st.title("AI Resume Analyzer")

    usage = get_usage(user_id)

    if plan == "free" and usage >= 1:
        st.error("Free plan limit reached (1 resume per day). Upgrade to Pro.")
        return

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

    job_description = st.text_area("Job Description")

    if uploaded_file:

        text = extract_text_from_file(uploaded_file)

        result = analyze_resume_basic(text, job_description)

        st.metric("Resume Score", result["score"])
        st.metric("ATS Score", result["ats_score"])

        st.write("Skills:", result["skills"])

        update_usage(user_id)


# BUILDER
def builder_page():

    st.title("AI Resume Builder")

    name = st.text_input("Name")
    title = st.text_input("Title")

    email = st.text_input("Email")
    phone = st.text_input("Phone")

    location = st.text_input("Location")

    skills = st.text_area("Skills")
    experience = st.text_area("Experience")
    education = st.text_area("Education")
    projects = st.text_area("Projects")

    if st.button("Generate Resume"):

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

        st.subheader("Summary")
        st.write(summary)

        st.subheader("Resume")
        st.text(resume)


# ROUTER
page = st.session_state.get("page", "landing")

if st.session_state["user"] is None:

    if page == "login":
        login_page()

    elif page == "signup":
        signup_page()

    else:
        landing_page()

else:

    menu = st.sidebar.selectbox(
        "Menu",
        ["Resume Analyzer", "Resume Builder"]
    )

    if menu == "Resume Analyzer":
        analyzer_page()

    if menu == "Resume Builder":
        builder_page()

    if st.sidebar.button("Logout"):
        st.session_state["user"] = None
        st.rerun()