from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(original, text_list):
    vectorizer = TfidfVectorizer().fit_transform([original] + text_list)
    vectors = vectorizer.toarray()
    original_vec = vectors[0]
    similarities = []
    for i in range(1, len(vectors)):
        similarities.append(cosine_similarity([original_vec], [vectors[i]])[0][0])
    return similarities

def get_combined_match_score(original, text_list):
    sims = compute_similarity(original, text_list)
    if not sims:
        return 0.0
    return sum(sims) / len(sims)
