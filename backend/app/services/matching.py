from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache
import re
import numpy as np

def clean_text(text: str) -> str:
    # Keep letters, numbers, spaces, and specific symbols like + and # (for C++, C#)
    text = re.sub(r'[^a-zA-Z0-9\s\+\#]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@lru_cache(maxsize=1)
def get_vectorizer():
    # token_pattern that allows 1+ alphanumerics plus + and #
    return CountVectorizer(stop_words='english', token_pattern=r'(?u)\b\w[\w\+\#]*\b')

def calculate_similarity(resume_text: str, job_desc_text: str) -> float:
    if not resume_text or not job_desc_text:
        return 0.0
    
    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(job_desc_text)
    
    print(f"DEBUG: Clean Resume: {clean_resume[:50]}...")
    print(f"DEBUG: Clean JD: {clean_jd[:50]}...")
    
    corpus = [clean_resume, clean_jd]
    
    score = 0.0
    try:
        vectorizer = get_vectorizer()
        count_matrix = vectorizer.fit_transform(corpus)
        similarity = cosine_similarity(count_matrix[0:1], count_matrix[1:2])
        score = similarity[0][0]
    except Exception as e:
        print(f"Error calculating cosine similarity: {e}")
        score = 0.0

    # Fallback: Simple set intersection if score is very low
    # This ensures that if key terms match, we show SOME score.
    if score < 0.1:
        resume_tokens = set(clean_resume.split())
        jd_tokens = set(clean_jd.split())
        
        # Filter stop words from fallback too
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
        resume_tokens = {w for w in resume_tokens if w not in ENGLISH_STOP_WORDS}
        jd_tokens = {w for w in jd_tokens if w not in ENGLISH_STOP_WORDS}
        
        if jd_tokens:
            common = resume_tokens.intersection(jd_tokens)
            fallback_score = len(common) / len(jd_tokens)
            print(f"DEBUG: Fallback Score used. Common: {common}")
            # we take the max, but cap fallback at 0.5 to prefer vector matches
            score = max(score, min(fallback_score, 0.5))

    return round(score, 2)

def rank_candidates(candidates_data: list) -> list:
    # candidate_data = [{'id': 1, 'score': 0.8}, ...]
    return sorted(candidates_data, key=lambda x: x['score'], reverse=True)
