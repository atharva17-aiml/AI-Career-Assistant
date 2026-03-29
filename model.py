import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

# 🔥 Smart Skill Mapping
SKILL_ALIASES = {
    "python": ["python", "python programming"],
    "machine learning": ["machine learning", "ml"],
    "data analysis": ["data analysis", "data analytics"],
    "nlp": ["nlp", "natural language processing"],
    "deep learning": ["deep learning"],
    "sql": ["sql"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "tensorflow": ["tensorflow"],
    "keras": ["keras"],
    "power bi": ["power bi"],
    "excel": ["excel"],
    "statistics": ["statistics", "statistical analysis"],
    "data visualization": ["data visualization", "visualization", "charts"]
}
def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill, variations in SKILL_ALIASES.items():
        for v in variations:
            if v in text:
                found_skills.append(skill)
                break

    return list(set(found_skills))


def match_skills(resume_skills, job_skills):
    matched = set(resume_skills) & set(job_skills)

    if len(job_skills) == 0:
        score = 0
    else:
        score = (len(matched) / len(job_skills)) * 100

    # 🔥 Make scoring realistic
    if score == 100:
        score = 90 + len(matched)

    missing = list(set(job_skills) - set(resume_skills))

    return score, list(matched), missing

def semantic_match(resume_text, job_skills):
    job_text = " ".join(job_skills)

    texts = [resume_text.lower(), job_text.lower()]

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(vectors[0], vectors[1])[0][0] * 100

    # 🔥 smoothing (avoid harsh 0)
    if similarity == 0:
        similarity = 5.0

    return similarity