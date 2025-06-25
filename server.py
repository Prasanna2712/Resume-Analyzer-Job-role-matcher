from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords

app = Flask(__name__)
CORS(app)

# Utility: clean text
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    return ' '.join([word for word in text.split() if word not in stop_words])

@app.route('/api/match', methods=['POST'])
def match_resume():
    data = request.get_json()
    resume = clean_text(data.get("resume", ""))
    jd = clean_text(data.get("jd", ""))

    if not resume or not jd:
        return jsonify({"error": "Missing resume or job description"}), 400

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, jd])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    score = round(similarity * 100, 2)

    resume_words = set(resume.split())
    jd_words = set(jd.split())
    missing = list(jd_words - resume_words)

    return jsonify({
        "match_score": score,
        "missing_keywords": missing
    })

@app.route('/api/message')
def message():
    return jsonify({"message": "Hello Team 1 Welcome"})

if __name__ == '__main__':
    app.run(debug=True)
