import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text: str) -> str:
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_similarity(resume_text: str, job_desc_text: str) -> float:
    if not resume_text or not job_desc_text:
        return 0.0
    
    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(job_desc_text)
    
    corpus = [clean_resume, clean_jd]
    
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return similarity[0][0]
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0

def rank_candidates(candidates_data: list) -> list:
    # candidate_data = [{'id': 1, 'score': 0.8}, ...]
    return sorted(candidates_data, key=lambda x: x['score'], reverse=True)
