from typing import List, Dict, Any
from flask import current_app
from ..crawler.serpapi_client import get_serpapi_client, SearchException

def get_search_query(content: str) -> str:
    snippet = content.strip()
    if len(snippet) > 100:
        snippet = snippet[:100]
    return snippet

def execute_google_search(content: str, max_results: int = 10) -> List[Dict[str, Any]]:
    app = current_app
    client = get_serpapi_client(app)
    query = get_search_query(content)
    try:
        return client.search_google(query, max_results)
    except SearchException:
        return []
    except Exception:
        return []
