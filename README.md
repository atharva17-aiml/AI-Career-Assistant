# AI Career Assistant

AI-powered resume analysis and career alignment system built with Python and Streamlit.

The application analyzes a user's resume against selected career roles, identifies relevant and missing skills, evaluates semantic alignment, measures resume quality, detects experience level, and recommends suitable career paths.

---

## Features

- Resume upload with PDF support
- Resume text extraction using PyMuPDF and PyPDF2
- Multiple career role selection
- AI/ML skill extraction using predefined skill mappings
- Keyword-based skill matching
- Weighted skill matching
- Semantic similarity using Sentence Transformers
- Cosine similarity-based semantic analysis
- Resume match score calculation
- Matched skills identification
- Missing skills identification
- High-priority skill detection
- Resume quality scoring
- Experience-level detection
- Technical profile detection
- Domain detection
- Career alignment analysis
- Career role ranking and recommendations
- Skill-gap analysis
- Improvement suggestions
- Streamlit-based interactive UI

---

## Supported Career Roles

The application currently supports:

- AI/ML Developer
- AI Engineer
- Machine Learning Engineer
- Data Scientist
- Data Analyst
- Python Developer
- Backend Developer
- Software Developer

---

## Tech Stack

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn
- Pandas
- NumPy
- PyMuPDF
- PyPDF2
- Matplotlib
- Git & GitHub

---

## Project Structure

```text
AI-Career-Assistant/
│
├── app.py
├── model.py
├── utils.py
├── style.css
├── requirements.txt
└── README.md