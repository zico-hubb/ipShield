from fuzzywuzzy import fuzz
from typing import List, Dict
from ..crawler.parse_results import preprocess_text_for_comparison

def score_fuzzy_match(original_text: str, candidate_text: str) -> int:
    clean_original = preprocess_text_for_comparison(original_text)
    clean_candidate = preprocess_text_for_comparison(candidate_text)
    return fuzz.token_sort_ratio(clean_original, clean_candidate)
