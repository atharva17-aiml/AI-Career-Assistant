import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# SEMANTIC MODEL
# ============================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    # --------------------------------------------------------
    # Programming
    # --------------------------------------------------------

    "python": [
        "python",
        "python programming",
        "python development",
        "python developer",
    ],

    "java": [
        "java",
        "java programming",
    ],

    "javascript": [
        "javascript",
        "java script",
        "js",
    ],

    # --------------------------------------------------------
    # AI / ML
    # --------------------------------------------------------

    "artificial intelligence": [
        "artificial intelligence",
        "artificial-intelligence",
        "artificial intelligence ai",
        "ai",
    ],

    "machine learning": [
        "machine learning",
        "machine-learning",
        "machine learning algorithms",
        "ml",
    ],

    "deep learning": [
        "deep learning",
        "deep-learning",
        "deep neural networks",
        "neural networks",
        "neural network",
        "dl",
    ],

    "nlp": [
        "nlp",
        "natural language processing",
        "natural-language-processing",
        "text processing",
        "language processing",
    ],

    "computer vision": [
        "computer vision",
        "computer-vision",
        "image processing",
        "opencv",
    ],

    "generative ai": [
        "generative ai",
        "generative-ai",
        "gen ai",
        "genai",
        "generative artificial intelligence",
    ],

    "llm": [
        "llm",
        "large language model",
        "large language models",
        "large language modelling",
        "large language modeling",
    ],

    # --------------------------------------------------------
    # ML Frameworks
    # --------------------------------------------------------

    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn",
        "scikit",
    ],

    "tensorflow": [
        "tensorflow",
        "tensor flow",
        "tensorflow keras",
    ],

    "pytorch": [
        "pytorch",
        "py torch",
    ],

    "keras": [
        "keras",
        "tensorflow keras",
    ],

    # --------------------------------------------------------
    # Data
    # --------------------------------------------------------

    "pandas": [
        "pandas",
    ],

    "numpy": [
        "numpy",
        "num py",
    ],

    "matplotlib": [
        "matplotlib",
    ],

    "seaborn": [
        "seaborn",
    ],

    "data analysis": [
        "data analysis",
        "data analytics",
        "data-analysis",
        "analytics",
    ],

    "data visualization": [
        "data visualization",
        "data visualisation",
        "visualization",
        "visualisation",
        "charts",
        "graphs",
    ],

    "statistics": [
        "statistics",
        "statistical analysis",
        "statistical modeling",
        "statistical modelling",
    ],

    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------

    "sql": [
        "sql",
        "structured query language",
        "sql queries",
    ],

    "mysql": [
        "mysql",
        "my sql",
    ],

    "postgresql": [
        "postgresql",
        "postgres",
        "postgre sql",
    ],

    # --------------------------------------------------------
    # Web / Backend
    # --------------------------------------------------------

    "flask": [
        "flask",
        "flask framework",
    ],

    "django": [
        "django",
        "django framework",
    ],

    "rest api": [
        "rest api",
        "restful api",
        "rest apis",
        "restful apis",
        "rest api development",
        "api development",
    ],

    # --------------------------------------------------------
    # Tools
    # --------------------------------------------------------

    "git": [
        "git",
        "github",
        "gitlab",
        "version control",
    ],

    "docker": [
        "docker",
        "docker containers",
        "containerization",
        "containerisation",
    ],

    "aws": [
        "aws",
        "amazon web services",
    ],

    # --------------------------------------------------------
    # CS Fundamentals
    # --------------------------------------------------------

    "data structures": [
        "data structures",
        "data structure",
        "dsa",
    ],

    "algorithms": [
        "algorithms",
        "algorithm",
        "algorithmic problem solving",
    ],

    # --------------------------------------------------------
    # Business Tools
    # --------------------------------------------------------

    "excel": [
        "excel",
        "microsoft excel",
        "ms excel",
    ],

    "power bi": [
        "power bi",
        "powerbi",
        "power-bi",
    ],
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize text for reliable matching.
    """

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[/|,_\\-]+",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def normalize_skill(skill):
    """
    Convert a skill or alias into its canonical skill name.
    """

    skill = normalize_text(skill)

    if not skill:
        return ""

    for canonical, variations in SKILL_ALIASES.items():

        if skill == canonical:
            return canonical

        normalized_variations = [
            normalize_text(item)
            for item in variations
        ]

        if skill in normalized_variations:
            return canonical

    return skill


def normalize_skills(skills):
    """
    Normalize a list of skills and remove duplicates.
    """

    normalized = set()

    if not skills:
        return []

    for skill in skills:

        canonical = normalize_skill(skill)

        if canonical:
            normalized.add(canonical)

    return sorted(normalized)


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(text):
    """
    Extract known skills from resume text.
    """

    text = normalize_text(text)

    if not text:
        return []

    found = set()

    for canonical, variations in SKILL_ALIASES.items():

        for variation in variations:

            variation = normalize_text(variation)

            if not variation:
                continue

            pattern = (
                r"(?<![a-z0-9+#.-])"
                + re.escape(variation)
                + r"(?![a-z0-9+#.-])"
            )

            if re.search(pattern, text):

                found.add(canonical)

                break

    return sorted(found)


# ============================================================
# BASIC SKILL MATCH
# ============================================================

def match_skills(
    resume_skills,
    job_skills,
):
    """
    Compare resume skills against required job skills.
    """

    resume = set(
        normalize_skills(
            resume_skills
        )
    )

    required = set(
        normalize_skills(
            job_skills
        )
    )

    if not required:
        return 0.0, [], []

    matched = resume.intersection(
        required
    )

    missing = required.difference(
        resume
    )

    score = (
        len(matched)
        / len(required)
    ) * 100

    return (
        round(score, 2),
        sorted(matched),
        sorted(missing),
    )


# ============================================================
# WEIGHTED SKILL MATCH
# ============================================================

def weighted_skill_match(
    resume_skills,
    job_skills,
    high_priority_skills=None,
):
    """
    Give higher importance to critical skills.
    """

    resume = set(
        normalize_skills(
            resume_skills
        )
    )

    required = normalize_skills(
        job_skills
    )

    high_priority = set(
        normalize_skills(
            high_priority_skills or []
        )
    )

    if not required:
        return 0.0

    total = 0
    matched = 0

    for skill in required:

        weight = (
            2
            if skill in high_priority
            else 1
        )

        total += weight

        if skill in resume:
            matched += weight

    return round(
        (matched / total) * 100,
        2,
    )


# ============================================================
# SEMANTIC MATCH
# ============================================================

def semantic_match(
    resume_text,
    job_skills,
    role_description="",
):
    """
    Calculate semantic similarity between the resume
    and the target role.

    Combines:
    - Role description similarity: 65%
    - Required skills similarity: 35%
    """

    resume_text = normalize_text(
        resume_text
    )

    if not resume_text:
        return 0.0

    # --------------------------------------------------------
    # Role description
    # --------------------------------------------------------

    description_target = normalize_text(
        role_description
    )

    # --------------------------------------------------------
    # Required skills
    # --------------------------------------------------------

    skill_target = " ".join(
        normalize_skills(
            job_skills
        )
    )

    if not description_target and not skill_target:
        return 0.0

    try:

        texts = [resume_text]

        if description_target:
            texts.append(description_target)

        if skill_target:
            texts.append(skill_target)

        embeddings = embedding_model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        # ----------------------------------------------------
        # Resume vs role description
        # ----------------------------------------------------

        if description_target:

            description_similarity = cosine_similarity(
                embeddings[0:1],
                embeddings[1:2],
            )[0][0]

            description_similarity = max(
                0.0,
                min(
                    1.0,
                    float(description_similarity),
                ),
            )

        else:

            description_similarity = 0.0

        # ----------------------------------------------------
        # Resume vs required skills
        # ----------------------------------------------------

        if skill_target:

            skill_index = 2 if description_target else 1

            skill_similarity = cosine_similarity(
                embeddings[0:1],
                embeddings[
                    skill_index:skill_index + 1
                ],
            )[0][0]

            skill_similarity = max(
                0.0,
                min(
                    1.0,
                    float(skill_similarity),
                ),
            )

        else:

            skill_similarity = 0.0

        # ----------------------------------------------------
        # Combined semantic score
        # ----------------------------------------------------

        if description_target and skill_target:

            similarity = (
                description_similarity * 0.65
                + skill_similarity * 0.35
            )

        elif description_target:

            similarity = description_similarity

        else:

            similarity = skill_similarity

        return round(
            similarity * 100,
            2,
        )

    except Exception:
        return 0.0


# ============================================================
# RESUME QUALITY
# ============================================================

def resume_quality_score(text):
    """
    Estimate resume quality based on structure and content.
    """

    text = normalize_text(
        text
    )

    if not text:
        return 0.0

    score = 0

    words = len(
        text.split()
    )

    # --------------------------------------------------------
    # Resume length
    # --------------------------------------------------------

    if words >= 300:
        score += 25

    elif words >= 150:
        score += 18

    elif words >= 75:
        score += 10

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    if any(
        item in text
        for item in [
            "education",
            "bachelor",
            "master",
            "degree",
            "university",
            "college",
        ]
    ):
        score += 15

    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    if "project" in text:
        score += 15

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    if any(
        item in text
        for item in [
            "skills",
            "technical skills",
            "technologies",
        ]
    ):
        score += 15

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    if any(
        item in text
        for item in [
            "experience",
            "internship",
            "intern",
            "employment",
        ]
    ):
        score += 15

    # --------------------------------------------------------
    # Email
    # --------------------------------------------------------

    if re.search(
        r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
        text,
    ):
        score += 5

    # --------------------------------------------------------
    # LinkedIn
    # --------------------------------------------------------

    if "linkedin" in text:
        score += 2

    # --------------------------------------------------------
    # GitHub
    # --------------------------------------------------------

    if "github" in text:
        score += 3

    return round(
        min(score, 100),
        2,
    )


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

def skill_gap_analysis(
    resume_skills,
    job_skills,
    high_priority_skills=None,
):
    """
    Identify matched and missing skills and assign priorities.
    """

    score, matched, missing = match_skills(
        resume_skills,
        job_skills,
    )

    high_priority = set(
        normalize_skills(
            high_priority_skills or []
        )
    )

    required = set(
        normalize_skills(
            job_skills
        )
    )

    gaps = []

    for skill in missing:

        if skill in high_priority:

            priority = "High"

        elif skill in required:

            priority = "Medium"

        else:

            priority = "Low"

        gaps.append(
            {
                "skill": skill,
                "priority": priority,
            }
        )

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2,
    }

    gaps.sort(
        key=lambda item:
        priority_order[
            item["priority"]
        ]
    )

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "gaps": gaps,
    }