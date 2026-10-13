import html
import re
import textwrap
from pathlib import Path

import streamlit as st

from model import (
    extract_skills,
    match_skills,
    semantic_match,
    weighted_skill_match,
    resume_quality_score,
    skill_gap_analysis,
)

from utils import (
    extract_text_from_pdf,
    is_valid_resume_text,
    get_text_statistics,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LOAD CSS
# ============================================================

def load_css():
    css_path = Path(__file__).parent / "style.css"

    if not css_path.exists():
        st.error(
            "style.css not found. Keep style.css in the same folder as app.py."
        )
        return

    css = css_path.read_text(encoding="utf-8")

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )


load_css()


# ============================================================
# HTML RENDERER
# ============================================================

def render_html(content):
    """
    Render HTML safely without Streamlit interpreting
    indented HTML as Markdown code.
    """

    cleaned_html = textwrap.dedent(content).strip()
    st.html(cleaned_html)


# ============================================================
# SAFE HTML TEXT
# ============================================================

def safe_text(value):
    return html.escape(str(value))


# ============================================================
# ROLE DATA
# ============================================================

ROLE_DATA = {

    "AI/ML Developer": {
        "skills": [
            "deep learning",
            "machine learning",
            "nlp",
            "numpy",
            "pandas",
            "python",
            "scikit-learn",
            "tensorflow",
        ],

        "high_priority": [
            "python",
            "machine learning",
            "deep learning",
            "nlp",
            "scikit-learn",
            "tensorflow",
        ],

        "description": """
        AI/ML Developer responsible for developing and implementing
        artificial intelligence and machine learning solutions.
        The role involves Python programming, machine learning,
        deep learning, data preprocessing, model development,
        NLP, data analysis and ML libraries such as scikit-learn
        and TensorFlow.
        """,
    },


    "AI Engineer": {
        "skills": [
            "python",
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "nlp",
            "pytorch",
            "tensorflow",
            "scikit-learn",
        ],

        "high_priority": [
            "python",
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "nlp",
        ],

        "description": """
        AI Engineer responsible for building intelligent systems
        using artificial intelligence and machine learning.
        The role can involve deep learning, NLP, computer vision,
        Python programming, model development and AI frameworks.
        """,
    },


    "Machine Learning Engineer": {
        "skills": [
            "python",
            "machine learning",
            "deep learning",
            "scikit-learn",
            "tensorflow",
            "numpy",
            "pandas",
        ],

        "high_priority": [
            "python",
            "machine learning",
            "deep learning",
            "scikit-learn",
            "tensorflow",
        ],

        "description": """
        Machine Learning Engineer responsible for designing,
        training, evaluating and deploying machine learning
        models. Strong Python programming, data preprocessing,
        machine learning algorithms, deep learning, model
        evaluation and ML frameworks are important.
        """,
    },


    "Data Scientist": {
        "skills": [
            "python",
            "statistics",
            "machine learning",
            "pandas",
            "numpy",
            "data visualization",
            "scikit-learn",
            "sql",
        ],

        "high_priority": [
            "python",
            "machine learning",
            "statistics",
            "pandas",
            "numpy",
            "scikit-learn",
            "sql",
        ],

        "description": """
        Data Scientist responsible for analyzing data, building
        predictive models, performing statistical analysis,
        exploratory data analysis, feature engineering and
        communicating insights. Python, statistics, machine
        learning, pandas, SQL and data visualization are important.
        """,
    },


    "Data Analyst": {
        "skills": [
            "python",
            "sql",
            "pandas",
            "excel",
            "power bi",
            "data visualization",
            "statistics",
        ],

        "high_priority": [
            "sql",
            "pandas",
            "data visualization",
            "statistics",
        ],

        "description": """
        Data Analyst responsible for collecting, cleaning and
        analyzing data, creating reports and dashboards and
        generating business insights. SQL, Excel, Python,
        pandas, statistics, Power BI and data visualization
        are commonly required.
        """,
    },


    "Python Developer": {
        "skills": [
            "python",
            "flask",
            "django",
            "sql",
            "rest api",
            "git",
        ],

        "high_priority": [
            "python",
            "rest api",
            "sql",
        ],

        "description": """
        Python Developer responsible for developing backend
        applications and APIs using Python. Experience with
        Flask or Django, SQL databases, REST APIs, Git and
        software development practices is valuable.
        """,
    },


    "Backend Developer": {
        "skills": [
            "python",
            "flask",
            "django",
            "sql",
            "rest api",
            "git",
            "docker",
        ],

        "high_priority": [
            "python",
            "sql",
            "rest api",
        ],

        "description": """
        Backend Developer responsible for building server-side
        applications, APIs and database-driven systems.
        Python, Flask or Django, SQL, REST APIs, Git and
        deployment technologies are relevant.
        """,
    },


    "Software Developer": {
        "skills": [
            "python",
            "java",
            "javascript",
            "sql",
            "git",
            "data structures",
            "algorithms",
        ],

        "high_priority": [
            "python",
            "data structures",
            "algorithms",
        ],

        "description": """
        Software Developer responsible for designing,
        developing, testing and maintaining software applications.
        Programming, data structures, algorithms, databases,
        Git and software development practices are important.
        """,
    },
}


ROLE_SKILLS = {
    role: data["skills"]
    for role, data in ROLE_DATA.items()
}


# ============================================================
# DISPLAY NAMES
# ============================================================

DISPLAY_NAMES = {
    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",

    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "artificial intelligence": "Artificial Intelligence",
    "nlp": "NLP",
    "computer vision": "Computer Vision",

    "data analysis": "Data Analysis",
    "statistics": "Statistics",

    "numpy": "NumPy",
    "pandas": "Pandas",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",

    "scikit-learn": "Scikit-learn",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "keras": "Keras",

    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",

    "excel": "Excel",
    "power bi": "Power BI",

    "data visualization": "Data Visualization",

    "flask": "Flask",
    "django": "Django",
    "rest api": "REST API",

    "git": "Git / GitHub",
    "docker": "Docker",
    "aws": "AWS",

    "data structures": "Data Structures",
    "algorithms": "Algorithms",
}


def display_skill(skill):
    skill = str(skill).lower().strip()

    return DISPLAY_NAMES.get(
        skill,
        skill.title(),
    )


# ============================================================
# DOMAIN DETECTION
# ============================================================

def detect_domain(text):
    text = text.lower()

    domains = {

        "AI / Machine Learning": [
            ("artificial intelligence", 4),
            ("machine learning", 5),
            ("deep learning", 5),
            ("nlp", 4),
            ("natural language processing", 4),
            ("tensorflow", 3),
            ("pytorch", 3),
            ("scikit-learn", 3),
            ("computer vision", 4),
            ("generative ai", 4),
            ("llm", 4),
            ("data science", 3),
            ("predictive model", 3),
            ("classification", 2),
            ("regression", 2),
        ],

        "Data Analytics": [
            ("data analysis", 3),
            ("data analytics", 3),
            ("data visualization", 3),
            ("power bi", 3),
            ("tableau", 3),
            ("excel", 2),
            ("business intelligence", 3),
            ("sql", 2),
        ],

        "Software Development": [
            ("software development", 4),
            ("software developer", 4),
            ("web development", 3),
            ("backend", 3),
            ("frontend", 3),
            ("flask", 2),
            ("django", 2),
            ("rest api", 3),
            ("javascript", 2),
            ("java", 2),
        ],

        "Banking & Finance": [
            ("banking", 4),
            ("finance", 3),
            ("financial", 3),
            ("fraud detection", 4),
            ("fintech", 4),
            ("transaction", 2),
            ("portfolio", 3),
        ],

        "Education": [
            ("education", 1),
            ("academic", 1),
            ("teaching", 2),
            ("school", 1),
            ("university", 1),
            ("college", 1),
            ("student", 1),
        ],
    }

    scores = {}

    for domain, keywords in domains.items():

        score = 0

        for keyword, weight in keywords:

            if keyword in text:
                score += weight

        if score:
            scores[domain] = score

    if not scores:
        return "General / Not Detected"

    return max(
        scores,
        key=scores.get,
    )


# ============================================================
# EXPERIENCE DETECTION
# ============================================================

def detect_experience(text):
    text_lower = text.lower()

    # --------------------------------------------------------
    # Professional experience
    # --------------------------------------------------------

    experience_patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+professional\s+experience",
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+work\s+experience",
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience",
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+experience",
    ]

    values = []

    for pattern in experience_patterns:

        matches = re.findall(
            pattern,
            text_lower,
        )

        for match in matches:

            try:
                values.append(float(match))

            except ValueError:
                pass

    if values:
        return max(values)

    # --------------------------------------------------------
    # Months
    # --------------------------------------------------------

    month_patterns = [
        r"(\d+)\+?\s*months?\s+of\s+experience",
        r"(\d+)\+?\s*months?\s+of\s+internship",
        r"internship\s*[:\-]?\s*(\d+)\s*months?",
    ]

    month_values = []

    for pattern in month_patterns:

        matches = re.findall(
            pattern,
            text_lower,
        )

        for match in matches:

            try:
                month_values.append(
                    float(match) / 12
                )

            except ValueError:
                pass

    if month_values:
        return max(month_values)

    # --------------------------------------------------------
    # Fresher / student indicators
    # --------------------------------------------------------

    fresher_terms = [
        "fresher",
        "fresh graduate",
        "recent graduate",
        "recently graduated",
        "entry level",
        "entry-level",
        "no professional experience",
        "no work experience",
        "no prior experience",
        "looking for an entry level",
        "seeking an entry level",
        "seeking entry level",
        "currently pursuing",
        "mca",
        "master of computer applications",
        "bachelor of computer science",
        "recently completed",
    ]

    if any(
        term in text_lower
        for term in fresher_terms
    ):
        return 0.0

    return None


def experience_label(experience):

    if experience is None:
        return "Not Clearly Specified"

    if experience == 0:
        return "Fresher / Entry Level"

    if experience < 1:
        return "Less than 1 Year"

    if experience < 2:
        return "1–2 Years"

    if experience < 3:
        return "2–3 Years"

    if experience < 5:
        return "3–5 Years"

    return "5+ Years"


# ============================================================
# TECHNICAL PROFILE
# ============================================================

def technical_profile(skill_count):

    if skill_count >= 8:
        return "Strong"

    if skill_count >= 4:
        return "Moderate"

    return "Developing"


# ============================================================
# SKILL PRIORITY
# ============================================================

def skill_priority(
    skill,
    high_priority_skills,
    all_required_skills=None,
):

    normalized = skill.lower().strip()

    high = {
        item.lower().strip()
        for item in high_priority_skills
    }

    required = {
        item.lower().strip()
        for item in (all_required_skills or [])
    }

    if normalized in high:
        return "High Priority"

    if normalized in required:
        return "Medium Priority"

    return "Low Priority"


# ============================================================
# RECOMMENDATIONS
# ============================================================

def get_recommendation(skill):

    recommendations = {

        "deep learning":
            "Learn neural networks, CNNs, RNNs, transformers and transfer learning.",

        "tensorflow":
            "Learn TensorFlow/Keras and build a practical deep learning project.",

        "nlp":
            "Learn text preprocessing, embeddings, transformers and NLP applications.",

        "machine learning":
            "Practice supervised and unsupervised learning with real datasets.",

        "python":
            "Strengthen Python, OOP, functions, modules and problem solving.",

        "numpy":
            "Practice numerical computing, arrays and vectorized operations.",

        "pandas":
            "Practice data cleaning, transformation and exploratory data analysis.",

        "scikit-learn":
            "Build ML pipelines using preprocessing, training and model evaluation.",

        "statistics":
            "Learn probability, distributions, hypothesis testing and statistical analysis.",

        "sql":
            "Practice joins, subqueries, aggregation and window functions.",

        "data visualization":
            "Learn Matplotlib, Seaborn and dashboard design.",

        "excel":
            "Learn formulas, pivot tables, charts and data analysis.",

        "power bi":
            "Learn dashboards, data modelling and DAX fundamentals.",

        "pytorch":
            "Learn tensors, neural networks, training loops and model deployment.",

        "rest api":
            "Build REST APIs using Flask or Django REST Framework.",

        "docker":
            "Learn containers, Dockerfiles and deployment workflows.",
    }

    return recommendations.get(
        skill.lower(),
        f"Develop practical skills in {display_skill(skill)} through projects.",
    )


# ============================================================
# CAREER RECOMMENDATION
# ============================================================

def career_recommendation(
    role,
    matched,
    missing,
    final_score,
):

    if final_score >= 80:

        return (
            f"Your profile shows strong alignment with the "
            f"{role} role. Focus on measurable project outcomes, "
            f"internships and real-world implementation."
        )

    if final_score >= 60:

        return (
            f"You have a good foundation for the {role} role. "
            f"Strengthen the missing skills and demonstrate them "
            f"through practical projects."
        )

    return (
        f"Your profile is still developing for the {role} role. "
        f"Prioritize the missing technical skills and build "
        f"2–3 relevant projects."
    )


# ============================================================
# CAREER SCORE FOR ALL ROLES
# ============================================================

def calculate_role_score(
    resume_text,
    resume_skills,
    role_name,
):

    data = ROLE_DATA[role_name]

    job_skills = data["skills"]
    high_priority = data["high_priority"]
    description = data["description"]

    keyword_score, matched, missing = match_skills(
        resume_skills,
        job_skills,
    )

    weighted_score = weighted_skill_match(
        resume_skills,
        job_skills,
        high_priority,
    )

    semantic_score = semantic_match(
        resume_text,
        job_skills,
        description,
    )

    return (
        keyword_score,
        weighted_score,
        semantic_score,
        matched,
        missing,
    )


def career_role_ranking(
    resume_text,
    resume_skills,
):

    results = []

    for role_name in ROLE_DATA:

        (
            keyword_score,
            weighted_score,
            semantic_score,
            matched,
            missing,
        ) = calculate_role_score(
            resume_text,
            resume_skills,
            role_name,
        )

        score = (
            0.40 * keyword_score
            + 0.30 * weighted_score
            + 0.30 * semantic_score
        )

        results.append(
            {
                "role": role_name,
                "score": round(
                    max(
                        0,
                        min(
                            100,
                            score,
                        ),
                    ),
                    2,
                ),
                "matched": matched,
                "missing": missing,
            }
        )

    results.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    return results


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">
                🎯
            </div>

            <div class="sidebar-brand-title">
                Career Target
            </div>
        </div>
        """
    )

    render_html(
        """
        <div class="sidebar-label">
            Select Target Role
        </div>
        """
    )

    role = st.selectbox(
        "Target Role",
        list(ROLE_DATA.keys()),
        index=list(
            ROLE_DATA.keys()
        ).index("AI/ML Developer"),
        label_visibility="collapsed",
    )

    st.markdown(
        "<hr>",
        unsafe_allow_html=True,
    )

    render_html(
        """
        <div class="sidebar-section-title">
            📌 Target Role Skills
        </div>
        """
    )

    for skill in ROLE_DATA[role]["skills"]:

        render_html(
            f"""
            <div class="sidebar-skill">
                • {safe_text(display_skill(skill))}
            </div>
            """
        )

    st.markdown(
        "<hr>",
        unsafe_allow_html=True,
    )

    render_html(
        """
        <div class="sidebar-help">
            <div class="sidebar-help-title">
                How it works
            </div>

            <div class="sidebar-help-text">
                Upload your resume and the AI Career Assistant
                analyzes your skills, semantic alignment,
                experience and career gaps.
            </div>
        </div>
        """
    )


# ============================================================
# HEADER
# ============================================================

render_html(
    """
    <div class="app-header">

        <div class="app-title">
            🚀 AI Career Assistant
        </div>

        <div class="app-subtitle">
            Analyze your resume with AI
        </div>

    </div>
    """
)


# ============================================================
# UPLOAD SECTION
# ============================================================

render_html(
    """
    <div class="section-heading">

        <div class="section-icon">
            📄
        </div>

        <div>
            <div class="section-title">
                Upload Resume
            </div>

            <div class="section-subtitle">
                Upload your PDF resume to receive your
                personalized career analysis.
            </div>
        </div>

    </div>
    """
)


render_html(
    """
    <div class="upload-intro">

        <div class="upload-intro-title">
            Upload your resume
        </div>

        <div class="upload-intro-text">
            Supported format: PDF
        </div>

    </div>
    """
)


uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"],
    label_visibility="collapsed",
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze = st.button(
    "🚀 Analyze Resume",
    use_container_width=True,
    disabled=uploaded_file is None,
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze and uploaded_file:

    with st.spinner(
        "Analyzing your resume... 🤖"
    ):

        # ----------------------------------------------------
        # Extract PDF text
        # ----------------------------------------------------

        text = extract_text_from_pdf(
            uploaded_file
        )

        if not is_valid_resume_text(text):

            st.error(
                "❌ The PDF does not contain enough readable "
                "text for analysis."
            )

            st.stop()

        # ----------------------------------------------------
        # Resume statistics
        # ----------------------------------------------------

        statistics = get_text_statistics(
            text
        )

        analysis_text = text.lower()

        # ----------------------------------------------------
        # Selected role
        # ----------------------------------------------------

        role_data = ROLE_DATA[role]

        job_skills = role_data["skills"]

        high_priority_skills = (
            role_data["high_priority"]
        )

        role_description = (
            role_data["description"]
        )

        # ----------------------------------------------------
        # Skill extraction
        # ----------------------------------------------------

        resume_skills = extract_skills(
            analysis_text
        )

        # FIX: technical variable
        technical = technical_profile(
            len(resume_skills)
        )

        # ----------------------------------------------------
        # Keyword matching
        # ----------------------------------------------------

        (
            keyword_score,
            matched,
            missing,
        ) = match_skills(
            resume_skills,
            job_skills,
        )

        # ----------------------------------------------------
        # Weighted skill score
        # ----------------------------------------------------

        weighted_score = weighted_skill_match(
            resume_skills,
            job_skills,
            high_priority_skills,
        )

        # ----------------------------------------------------
        # Semantic matching
        # ----------------------------------------------------

        semantic_score = semantic_match(
            analysis_text,
            job_skills,
            role_description,
        )

        # ----------------------------------------------------
        # Resume quality
        # ----------------------------------------------------

        quality_score = resume_quality_score(
            analysis_text
        )

        # ----------------------------------------------------
        # Skill gap analysis
        # ----------------------------------------------------

        gap_analysis = skill_gap_analysis(
            resume_skills,
            job_skills,
            high_priority_skills,
        )

        # ----------------------------------------------------
        # Experience
        # ----------------------------------------------------

        experience = detect_experience(
            text
        )

        # ----------------------------------------------------
        # Domain
        # ----------------------------------------------------

        domain = detect_domain(
            analysis_text
        )

        # ----------------------------------------------------
        # Experience score
        # ----------------------------------------------------

        if experience is None:

            experience_score = 50.0

        elif experience == 0:

            experience_score = 60.0

        elif experience < 1:

            experience_score = 70.0

        elif experience < 2:

            experience_score = 80.0

        elif experience < 3:

            experience_score = 90.0

        else:

            experience_score = 100.0

        # ----------------------------------------------------
        # Final score
        # ----------------------------------------------------

        final_score = (
            0.35 * keyword_score
            + 0.25 * weighted_score
            + 0.25 * semantic_score
            + 0.10 * experience_score
            + 0.05 * quality_score
        )

        final_score = max(
            0.0,
            min(
                100.0,
                final_score,
            ),
        )

        final_score = round(
            final_score,
            2,
        )

        # ====================================================
        # ANALYSIS HEADER
        # ====================================================

        render_html(
            f"""
            <div class="section-heading">

                <div class="section-icon">
                    🎯
                </div>

                <div>
                    <div class="section-title">
                        Career Analysis
                    </div>

                    <div class="section-subtitle">
                        Resume alignment with
                        {safe_text(role)}
                    </div>
                </div>

            </div>
            """
        )

        # ====================================================
        # SCORE CARDS
        # ====================================================

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Resume Match",
                f"{final_score:.1f}%",
            )

        with c2:

            st.metric(
                "Keyword Match",
                f"{keyword_score:.1f}%",
            )

        with c3:

            st.metric(
                "Semantic Match",
                f"{semantic_score:.1f}%",
            )

        with c4:

            st.metric(
                "Resume Quality",
                f"{quality_score:.1f}%",
            )

        st.progress(
            int(round(final_score))
        )

        if final_score >= 80:

            st.success(
                "🔥 Strong career alignment"
            )

        elif final_score >= 60:

            st.warning(
                "⚡ Moderate career alignment"
            )

        else:

            st.error(
                "🚨 Low career alignment"
            )

        # ====================================================
        # PROFILE OVERVIEW
        # ====================================================

        render_html(
            """
            <div class="section-heading">

                <div class="section-icon">
                    👤
                </div>

                <div>
                    <div class="section-title">
                        Profile Overview
                    </div>
                </div>

            </div>
            """
        )

        p1, p2, p3, p4 = st.columns(4)

        with p1:

            st.metric(
                "Target Role",
                role,
            )

        with p2:

            st.metric(
                "Technical Profile",
                technical,
            )

        with p3:

            st.metric(
                "Detected Domain",
                domain,
            )

        with p4:

            st.metric(
                "Experience",
                experience_label(
                    experience
                ),
            )

        # ====================================================
        # SKILL ANALYSIS
        # ====================================================

        render_html(
            """
            <div class="section-heading">

                <div class="section-icon">
                    🧠
                </div>

                <div>

                    <div class="section-title">
                        Skill Analysis
                    </div>

                    <div class="section-subtitle">
                        Skills detected and compared against
                        the selected target role.
                    </div>

                </div>

            </div>
            """
        )

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # MATCHED SKILLS
        # ----------------------------------------------------

        with col1:

            render_html(
                """
                <div class="skill-column-title">
                    ✅ Matched Skills
                </div>
                """
            )

            if matched:

                for skill in matched:

                    render_html(
                        f"""
                        <div class="skill-card matched-card">

                            <div class="skill-name">
                                {safe_text(display_skill(skill))}
                            </div>

                            <div class="skill-status">
                                Matched
                            </div>

                        </div>
                        """
                    )

            else:

                st.info(
                    "No required skills were matched."
                )

        # ----------------------------------------------------
        # MISSING SKILLS
        # ----------------------------------------------------

        with col2:

            render_html(
                """
                <div class="skill-column-title">
                    ❌ Missing Skills
                </div>
                """
            )

            if missing:

                for skill in missing:

                    priority = skill_priority(
                        skill,
                        high_priority_skills,
                        job_skills,
                    )

                    render_html(
                        f"""
                        <div class="skill-card missing-card">

                            <div class="skill-name">
                                {safe_text(display_skill(skill))}
                            </div>

                            <div class="skill-status">
                                {safe_text(priority)}
                            </div>

                        </div>
                        """
                    )

            else:

                st.success(
                    "🎉 No major missing skills."
                )

        # ====================================================
        # SKILL GAP RECOMMENDATIONS
        # ====================================================

        render_html(
            """
            <div class="section-heading">

                <div class="section-icon">
                    📚
                </div>

                <div>

                    <div class="section-title">
                        Skill Gap Recommendations
                    </div>

                    <div class="section-subtitle">
                        Recommended learning areas based on
                        your selected role.
                    </div>

                </div>

            </div>
            """
        )

        if missing:

            for skill in missing:

                priority = skill_priority(
                    skill,
                    high_priority_skills,
                    job_skills,
                )

                recommendation = get_recommendation(
                    skill
                )

                render_html(
                    f"""
                    <div class="content-card">

                        <div class="profile-label">
                            {safe_text(display_skill(skill))}
                        </div>

                        <div class="profile-value">
                            {safe_text(priority)}
                        </div>

                        <div class="upload-intro-text">
                            {safe_text(recommendation)}
                        </div>

                    </div>
                    """
                )

        else:

            st.success(
                "🎉 Your resume covers all required skills."
            )

        # ====================================================
        # EXPERIENCE
        # ====================================================

        render_html(
            """
            <div class="section-heading">

                <div class="section-icon">
                    💼
                </div>

                <div>

                    <div class="section-title">
                        Experience Analysis
                    </div>

                </div>

            </div>
            """
        )

        if experience is None:

            st.info(
                "Experience was not clearly specified in the resume."
            )

        elif experience == 0:

            st.info(
                "Fresher / Entry Level — focus on projects, "
                "internships and practical implementation."
            )

        else:

            st.success(
                f"Detected professional experience: "
                f"{experience_label(experience)}"
            )

        # ====================================================
        # RESUME QUALITY
        # ====================================================

        render_html(
            """
            <div class="section-heading">

                <div class="section-icon">
                    📊
                </div>

                <div>

                    <div class="section-title">
                        Resume Quality
                    </div>

                    <div class="section-subtitle">
                        Basic completeness indicators for reliable analysis.
                    </div>

                </div>

            </div>
            """
        )

        q1, q2, q3 = st.columns(3)

        with q1:

            st.metric(
                "Words",
                statistics["words"],
            )

        with q2:

            st.metric(
                "Characters",
                statistics["characters"],
            )

        with q3:

            st.metric(
                "Detected Skills",
                len(resume_skills),
            )

        # ====================================================
        # CAREER RECOMMENDATION ACROSS ALL ROLES
        # ====================================================

        render_html(
            """
            <div class="section-heading">

                <div class="section-icon">
                    🚀
                </div>

                <div>

                    <div class="section-title">
                        Career Recommendation
                    </div>

                    <div class="section-subtitle">
                        AI-based ranking of your resume across
                        available career roles.
                    </div>

                </div>

            </div>
            """
        )

        role_rankings = career_role_ranking(
            analysis_text,
            resume_skills,
        )

        if role_rankings:

            best_role = role_rankings[0]

            st.success(
                f"🏆 Best Match: {best_role['role']} "
                f"— {best_role['score']:.1f}%"
            )

            st.markdown(
                "### Career Match Ranking"
            )

            for index, item in enumerate(
                role_rankings,
                start=1,
            ):

                role_name = item["role"]
                role_score = item["score"]

                if index == 1:

                    badge = "🏆 Best Match"

                elif index == 2:

                    badge = "🥈 Strong Alternative"

                elif index == 3:

                    badge = "🥉 Alternative"

                else:

                    badge = "Career Option"

                col_a, col_b, col_c = st.columns(
                    [0.6, 3, 1.2]
                )

                with col_a:

                    st.write(
                        f"**#{index}**"
                    )

                with col_b:

                    st.write(
                        f"**{role_name}**"
                    )

                    st.caption(
                        badge
                    )

                with col_c:

                    st.metric(
                        "Match",
                        f"{role_score:.1f}%",
                    )

                st.progress(
                    int(round(role_score))
                )

            # ------------------------------------------------
            # Best role explanation
            # ------------------------------------------------

            best_matched = best_role["matched"]
            best_missing = best_role["missing"]

            st.markdown(
                f"### Why **{best_role['role']}**?"
            )

            if best_matched:

                st.success(
                    "Matched skills: "
                    + ", ".join(
                        display_skill(skill)
                        for skill in best_matched
                    )
                )

            if best_missing:

                st.warning(
                    "Skills to strengthen: "
                    + ", ".join(
                        display_skill(skill)
                        for skill in best_missing[:5]
                    )
                )

        # ====================================================
        # SELECTED ROLE RECOMMENDATION
        # ====================================================

        st.markdown(
            "### Selected Role Assessment"
        )

        recommendation = career_recommendation(
            role,
            matched,
            missing,
            final_score,
        )

        st.info(
            recommendation
        )

        # ====================================================
        # DETECTED RESUME SKILLS
        # ====================================================

        render_html(
            """
            <div class="section-heading">

                <div class="section-icon">
                    📋
                </div>

                <div>

                    <div class="section-title">
                        Detected Resume Skills
                    </div>

                </div>

            </div>
            """
        )

        if resume_skills:

            skill_display = [
                display_skill(skill)
                for skill in resume_skills
            ]

            st.info(
                " • ".join(
                    skill_display
                )
            )

        else:

            st.warning(
                "No known technical skills were detected."
            )

        # ====================================================
        # STRENGTHS
        # ====================================================

        render_html(
            """
            <div class="section-heading">

                <div class="section-icon">
                    💪
                </div>

                <div>

                    <div class="section-title">
                        Strengths
                    </div>

                </div>

            </div>
            """
        )

        if matched:

            st.success(
                "Strong in: "
                + ", ".join(
                    display_skill(skill)
                    for skill in matched
                )
            )

        else:

            st.info(
                "Build more projects containing skills "
                "required for the selected role."
            )

        # ====================================================
        # DEBUG INFORMATION
        # ====================================================

        with st.expander(
            "🔍 Developer Debug Information"
        ):

            st.write(
                "Target Role:",
                role,
            )

            st.write(
                "Detected Domain:",
                domain,
            )

            st.write(
                "Technical Profile:",
                technical,
            )

            st.write(
                "Experience:",
                experience,
            )

            st.write(
                "Resume Skills:",
                [
                    display_skill(skill)
                    for skill in resume_skills
                ],
            )

            st.write(
                "Required Skills:",
                [
                    display_skill(skill)
                    for skill in job_skills
                ],
            )

            st.write(
                "Matched:",
                [
                    display_skill(skill)
                    for skill in matched
                ],
            )

            st.write(
                "Missing:",
                [
                    display_skill(skill)
                    for skill in missing
                ],
            )

            st.write(
                "Keyword Score:",
                round(
                    keyword_score,
                    2,
                ),
            )

            st.write(
                "Weighted Skill Score:",
                round(
                    weighted_score,
                    2,
                ),
            )

            st.write(
                "Semantic Score:",
                round(
                    semantic_score,
                    2,
                ),
            )

            st.write(
                "Resume Quality:",
                round(
                    quality_score,
                    2,
                ),
            )

            st.write(
                "Final Score:",
                round(
                    final_score,
                    2,
                ),
            )


# ============================================================
# EMPTY STATE
# ============================================================

elif not uploaded_file:

    render_html(
        """
        <div class="empty-state">

            <div class="empty-icon">
                📄
            </div>

            <div class="empty-title">
                Upload your resume to begin
            </div>

            <div class="empty-text">
                Select your target role, upload your PDF resume,
                and click Analyze Resume.
            </div>

        </div>
        """
    )