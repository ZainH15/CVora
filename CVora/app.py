import os
import json

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pypdf import PdfReader
from openai import OpenAI


app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "uploads")

client = OpenAI()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    cv = request.files.get("cv")

    if not cv:
        return "Please select a CV before uploading.", 400

    if cv.filename == "":
        return "Please select a CV before uploading.", 400

    if not cv.filename.lower().endswith(".pdf"):
        return "CVora currently accepts PDF files only.", 400

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    filename = secure_filename(cv.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    cv.save(filepath)

    try:
        reader = PdfReader(filepath)

        cv_text = ""

        for page in reader.pages:
            text = page.extract_text(extraction_mode="layout")

            if text:
                cv_text += text + "\n"

        if not cv_text.strip():
            return ("CVora couldn't find any readable text in this PDF. Please upload a text-based CV.", 400)

        text = cv_text.lower()
        score = 0

        if "@" in text:
            score += 10

        if "education" in text:
            score += 15

        if "skills" in text:
            score += 15

        if "experience" in text:
            score += 15

        if "projects" in text:
            score += 15

        if len(cv_text) >= 1000:
            score += 10

        if len(cv_text) >= 2000:
            score += 5

        if any(char.isdigit() for char in cv_text):
            score += 5

        score = min(score, 100)

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=f"""
You are a professional CV reviewer.

Analyse the CV below and provide useful, specific feedback.

Focus only on the CV itself. Do not compare it against a job description.

Return:

1. Strengths — the strongest aspects of the CV.
2. Weaknesses — the most important problems or missing elements.
3. Improvements — specific and actionable changes the candidate should make.
4. Assessment — a concise overall assessment of the CV.

Base your feedback only on information actually present in the CV.
Do not invent experience, qualifications, skills, or achievements.

CV:
{cv_text}
""",

            text={
                "format": {
                    "type": "json_schema",
                    "name": "cv_analysis",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "strengths": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "weaknesses": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "improvements": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "assessment": {
                                "type": "string",
                            },
                        },
                        "required": [
                            "strengths",
                            "weaknesses",
                            "improvements",
                            "assessment",
                        ],
                        "additionalProperties": False,
                    },
                }
            },
        )

        analysis = json.loads(response.output_text)

        return render_template(
            "results.html",
            score=score,
            analysis=analysis
        )

    except Exception as error:
        print("CVora processing error:", error)
        return "CVora couldn't complete the analysis. Please try again in a moment.", 500

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)


if __name__ == "__main__":
    app.run(debug=True)


@app.route("/test-ai")
def test_ai():
    response = client.responses.create(
        model="gpt-5.6-luna",
        input="Say exactly: AI connection successful."
    )

    return response.output_text
