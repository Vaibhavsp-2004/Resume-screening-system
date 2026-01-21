from sklearn.feature_extraction.text import CountVectorizer
from functools import lru_cache
import re

def clean_text(text: str) -> str:
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@lru_cache(maxsize=1)
def get_vectorizer():
    return CountVectorizer(stop_words='english')

def calculate_similarity(resume_text: str, job_desc_text: str) -> float:
    if not resume_text or not job_desc_text:
        return 0.0
    
    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(job_desc_text)
    
    print(f"DEBUG: Resume length: {len(clean_resume)} chars")
    print(f"DEBUG: JD length: {len(clean_jd)} chars")
    print(f"DEBUG: Resume sample: {clean_resume[:50]}...")
    
    # Use CountVectorizer to avoid IDF issues with small corpus (2 docs)
    # TF-IDF penalizes words appearing in all docs (which here is 50-100% of docs), leading to 0 scores.
    corpus = [clean_resume, clean_jd]
    
    vectorizer = get_vectorizer()
    try:
        count_matrix = vectorizer.fit_transform(corpus)
        similarity = cosine_similarity(count_matrix[0:1], count_matrix[1:2])
        return round(similarity[0][0], 2)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0

def rank_candidates(candidates_data: list) -> list:
    # candidate_data = [{'id': 1, 'score': 0.8}, ...]
    return sorted(candidates_data, key=lambda x: x['score'], reverse=True)
