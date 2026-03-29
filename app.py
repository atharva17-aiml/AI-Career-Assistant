import streamlit as st
from utils import extract_text_from_pdf
from model import extract_skills, match_skills, semantic_match
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🚀"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: 700;
}
.subtitle {
    color: gray;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">🚀 AI Career Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analyze your resume with AI</div>', unsafe_allow_html=True)

# ---------------- ROLE SKILLS ----------------
ROLE_SKILLS = {
    "Data Scientist": ["python", "statistics", "machine learning", "pandas", "data visualization"],
    "ML Engineer": ["python", "machine learning", "deep learning", "tensorflow"],
    "Data Analyst": ["python", "sql", "pandas", "excel", "power bi"]
}

# ---------------- DOMAIN ----------------
def detect_domain(text):
    text = text.lower()
    if "insurance" in text:
        return "Non-Tech"
    elif "python" in text or "machine learning" in text:
        return "Tech"
    return "Unknown"

# ---------------- INPUT ----------------
uploaded_file = st.file_uploader("📂 Upload Resume", type=["pdf"])
role = st.selectbox("🎯 Select Role", list(ROLE_SKILLS.keys()))
analyze = st.button("🚀 Analyze")

# ---------------- ANALYSIS ----------------
if analyze and uploaded_file:

    with st.spinner("Analyzing Resume... 🤖"):
        text = extract_text_from_pdf(uploaded_file)

        if not text or len(text.strip()) < 20:
            st.error("⚠️ Could not extract text.")
            st.stop()

        text = re.sub(r'\s+', ' ', text.lower())

        domain = detect_domain(text)

        resume_skills = extract_skills(text)
        job_skills = ROLE_SKILLS[role]

        keyword_score, matched, missing = match_skills(resume_skills, job_skills)
        semantic_score = semantic_match(text, job_skills)

        final_score = (0.6 * keyword_score) + (0.4 * semantic_score)

    # 🔹 Role Match Validation Block
    if semantic_score < 30:
        st.warning("⚠️ Your resume may not strongly match this role.")

    # ---------------- RESULT ----------------
    st.subheader("🎯 Final Score")
    st.progress(int(final_score))
    st.metric("Match Score", f"{final_score:.1f}%")

    # Status
    if final_score < 40:
        st.error("🚨 Low match")
    elif final_score < 70:
        st.warning("⚡ Moderate match")
    else:
        st.success("🔥 Strong match")

    if domain == "Non-Tech":
        st.warning("⚠️ Non-technical resume")

    # ---------------- DETAILS ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Scores")
        st.info(f"Keyword Match: {keyword_score:.1f}%")
        st.info(f"Semantic Match: {semantic_score:.1f}%")

    with col2:
        st.markdown("### 💡 Suggestions")

        for skill in missing:
            if skill == "data visualization":
                st.info("📊 Learn Data Visualization (Matplotlib, Seaborn)")
            elif skill == "statistics":
                st.info("📈 Learn Statistics (probability, distributions)")
            elif skill == "excel":
                st.info("📊 Learn Excel for data analysis")
            elif skill == "power bi":
                st.info("📊 Learn Power BI for dashboards")
            else:
                st.info(f"📌 Learn {skill}")

    # ---------------- SKILLS ----------------
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### ✅ Matched Skills")
        for skill in matched:
            st.success(skill)

    with col4:
        st.markdown("### ❌ Missing Skills")
        for skill in missing:
            st.error(skill)

    # ---------------- STRENGTH ----------------
    st.subheader("💪 Strengths")
    if matched:
        st.success(f"Strong in: {', '.join(matched)}")

    # ---------------- DEBUG ----------------
    with st.expander("🔍 Debug Info"):
        st.write("Text:", text[:300])
        st.write("Matched:", matched)
        st.write("Missing:", missing)

else:
    st.info("👆 Upload resume and click Analyze")