from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# SKILL DATABASE
# -----------------------------
SKILLS_DB = [
    "python", "java", "c", "c++", "sql",
    "html", "css", "javascript",
    "machine learning", "deep learning",
    "data analysis", "pandas", "numpy",
    "flask", "django", "react",
    "node", "node.js",
    "mongodb", "mysql",
    "git", "github"
]

# -----------------------------
# 1. MATCH SCORE
# -----------------------------
def calculate_similarity(resume_text, job_desc):
    texts = [resume_text, job_desc]

    cv = CountVectorizer()
    matrix = cv.fit_transform(texts)

    similarity = cosine_similarity(matrix)[0][1]

    return round(similarity * 100, 2)


# -----------------------------
# 2. SKILL EXTRACTION
# -----------------------------
def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


# -----------------------------
# 3. MISSING SKILLS
# -----------------------------
def missing_skills(resume_text, job_desc):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_desc)

    missing = list(set(job_skills) - set(resume_skills))
    return missing


# -----------------------------
# 4. AI SUGGESTIONS
# -----------------------------
def generate_ai_suggestions(resume_text, job_desc, missing_skills_list):
    suggestions = []

    resume_text = resume_text.lower()

    # Missing skills suggestion
    if missing_skills_list:
        suggestions.append(
            "Learn and add these skills: " + ", ".join(missing_skills_list)
        )

    # Resume length check
    if len(resume_text.split()) < 120:
        suggestions.append(
            "Your resume is too short. Add more projects, internships, and achievements."
        )

    # Project section check
    if "project" not in resume_text:
        suggestions.append(
            "Add at least 1–2 strong projects to improve your profile."
        )

    # Experience check
    if "experience" not in resume_text:
        suggestions.append(
            "Include internship or practical experience."
        )

    # ATS optimization tip
    suggestions.append(
        "Use keywords from the job description to improve ATS score."
    )

    return suggestions


# -----------------------------
# 5. ATS SCORE BREAKDOWN
# -----------------------------
def ats_score(resume_text, job_desc):
    resume_text = resume_text.lower()
    job_desc = job_desc.lower()

    # Skill match
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_desc)

    if len(job_skills) == 0:
        skill_score = 0
    else:
        skill_score = (len(set(resume_skills) & set(job_skills)) / len(job_skills)) * 100

    # Keyword match
    resume_words = set(resume_text.split())
    job_words = set(job_desc.split())

    if len(job_words) == 0:
        keyword_score = 0
    else:
        keyword_score = (len(resume_words & job_words) / len(job_words)) * 100

    # Resume quality score
    quality_score = 0

    if len(resume_text.split()) > 100:
        quality_score += 40
    if "project" in resume_text:
        quality_score += 30
    if "experience" in resume_text:
        quality_score += 30

    # Final ATS score
    final_score = (skill_score * 0.5) + (keyword_score * 0.3) + (quality_score * 0.2)

    return {
        "final": round(final_score, 2),
        "skill": round(skill_score, 2),
        "keyword": round(keyword_score, 2),
        "quality": round(quality_score, 2)
    }