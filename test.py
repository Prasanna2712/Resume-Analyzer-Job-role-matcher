from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import mysql.connector
import nltk

# NLTK Setup
nltk.download('stopwords')
from nltk.corpus import stopwords

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",             # change
    password="",             # add your password 
    database="resume_matcher"
)
cursor = db.cursor()

# clean text
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    return ' '.join([word for word in text.split() if word not in stop_words])

#  SIGNUP 
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        return jsonify({"message": "Email already registered"}), 400

    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    db.commit()
    return jsonify({"message": "Signup successful"})

# 2. LOGIN 
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    if user:
        return jsonify({"message": "Login successful", "user": {"id": user[0], "name": user[1]}})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# 3. RESUME MATCHING 
@app.route('/api/match', methods=['POST'])
def match_resume():
    data = request.get_json()
    resume = clean_text(data.get("resume", ""))
    jd = clean_text(data.get("jd", ""))

    if not resume or not jd:
        return jsonify({"error": "Missing resume or job description"}), 400

    #  Vectorize and calculate similarity
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, jd])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    score = round(similarity * 100, 2)

    #  Find missing words
    resume_words = set(resume.split())
    jd_words = set(jd.split())
    missing = list(jd_words - resume_words)

    #  Generate suggestions based on missing keywords
    suggestions = []
    for keyword in missing:
        suggestions.append(f"Consider adding '{keyword}' in your resume (skills, projects, or summary)")

    #   response
    return jsonify({
        "match_score": score,
        "missing_keywords": missing,
        "suggestions": suggestions
    })

# Optional test route
@app.route('/api/message')
def message():
    return jsonify({"message": "Hello Team 1 Welcome"})

if __name__ == '__main__':
    app.run(debug=True)
