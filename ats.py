from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string 
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords

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

    # 1. Vectorize and calculate similarity
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, jd])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    score = round(similarity * 100, 2)
