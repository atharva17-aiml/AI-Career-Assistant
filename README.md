# AI Career Assistant

## Features

* Resume upload (PDF support)
* Role-based analysis (Data Scientist, ML Engineer, Data Analyst)
* Skill extraction using NLP (SpaCy)
* Keyword-based skill matching
* Semantic similarity using TF-IDF & cosine similarity
* Match score calculation (0–100%)
* Missing skills identification
* Smart suggestions for improvement
* Domain detection (Tech / Non-Tech)
* Streamlit-based UI

---

## Setup

Install dependencies:

```
pip install -r requirements.txt
```

Download SpaCy model:

```
python -m spacy download en_core_web_sm
```

Run application:

```
streamlit run app.py
```

---

## Usage

1. Upload your resume (PDF format)
2. Select target role:

   * Data Scientist
   * ML Engineer
   * Data Analyst
3. Click **Analyze**

---

## Output

* Match Score (percentage)
* Keyword Match Score
* Semantic Match Score
* Matched Skills
* Missing Skills
* Suggestions for improvement

---

## How It Works

* Extracts resume text using PyMuPDF & PyPDF2
* Identifies skills using predefined skill mappings
* Computes:

  * Keyword Match Score
  * Semantic Match (TF-IDF + cosine similarity)
* Final Score:

```
Final Score = (0.6 × Keyword Score) + (0.4 × Semantic Score)
```

---

## Assumptions

* Resume is in PDF format
* Text extraction works correctly
* Skills are present in predefined mapping
* Selected role defines expected skills

---

## Limitations

* Limited to predefined roles
* Rule-based skill extraction
* Basic semantic matching (TF-IDF)
* Not using deep learning models

---

## Notes

* Very short resumes may give inaccurate results
* Non-technical resumes may show low scores
* Semantic score is approximate, not exact AI understanding

---

## Example Run

* Role: Data Scientist
* Match Score: 72%
* Missing Skills: TensorFlow, Statistics

---

## Tech Stack

* Python
* Streamlit
* SpaCy
* Scikit-learn
* PyMuPDF
* PyPDF2

---

## Verification

Results verified using:

* UI output (Streamlit dashboard)
* Debug logs (matched & missing skills)

---

## Future Improvements

* Add LLM (GPT) integration
* Dynamic job role detection
* Advanced embeddings (BERT/OpenAI)
* Web deployment
* Resume scoring dashboard

---
