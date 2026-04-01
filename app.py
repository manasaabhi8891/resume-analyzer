from flask import Flask, render_template, request
from utils.parser import extract_text_from_pdf
from utils.analyzer import (
    calculate_similarity,
    missing_skills,
    generate_ai_suggestions,
    ats_score
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    missing = []
    suggestions = []
    ats = None   # important to avoid error

    if request.method == "POST":
        file = request.files.get("resume")
        job_desc = request.form.get("job_desc")

        if file and job_desc:
            try:
                resume_text = extract_text_from_pdf(file)

                # Match score
                score = calculate_similarity(resume_text, job_desc)

                # Missing skills
                missing = missing_skills(resume_text, job_desc)

                # AI Suggestions
                suggestions = generate_ai_suggestions(
                    resume_text, job_desc, missing
                )

                # ATS Score
                ats = ats_score(resume_text, job_desc)

            except Exception as e:
                print("Error:", e)

    return render_template(
        "index.html",
        score=score,
        missing=missing,
        suggestions=suggestions,
        ats=ats
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)