from typing import List, Dict, Any

def extract_and_clean_results(raw_results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    cleaned_results = []
    for result in raw_results:
        if "link" in result and "snippet" in result:
            cleaned_results.append({
                "link": result.get("link", ""),
                "title": result.get("title", "No Title"),
                "content_snippet": result.get("snippet", "").strip()
            })
    return cleaned_results

def preprocess_text_for_comparison(text: str) -> str:
    text = text.lower()
    text = "".join(c for c in text if c.isalnum() or c.isspace())
    text = " ".join(text.split())
    return text
