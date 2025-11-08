from flask import Flask, render_template, request
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

# Sample job listings
jobs = [
    {"id": 1, "title": "Software Engineer", "skills": ["Python", "Django", "JavaScript"]},
    {"id": 2, "title": "Data Scientist", "skills": ["Python", "Machine Learning", "Statistics"]},
    {"id": 3, "title": "Web Developer", "skills": ["HTML", "CSS", "JavaScript"]},
    {"id": 4, "title": "Data Analyst", "skills": ["SQL", "Data Visualization", "Excel"]},
]

@app.route('/')
def index():
    return render_template('index.html', jobs=None)  # Initially, no matches

@app.route('/match', methods=['POST'])
def match():
    # Get resume text from form
    resume_text = request.form.get('resume_text', '').lower()
    if not resume_text:
        return render_template('index.html', jobs=None)

    # Convert resume text into a set of words
    resume_words = set(resume_text.split())

    # Create job vectors based on keywords
    job_vectors = []
    all_skills = list({skill for job in jobs for skill in job['skills']})

    for job in jobs:
        job_vector = [1 if skill.lower() in [s.lower() for s in job['skills']] else 0 for skill in all_skills]
        job_vectors.append(job_vector)

    # Create resume vector
    resume_vector = [1 if skill.lower() in resume_words else 0 for skill in all_skills]

    # Calculate cosine similarity
    similarities = cosine_similarity([resume_vector], job_vectors)[0]

    # Pair jobs with similarity scores and sort
    matched_jobs = sorted(zip(jobs, similarities), key=lambda x: x[1], reverse=True)

    return render_template('index.html', jobs=matched_jobs)

if __name__ == '__main__':
    app.run(debug=True)
