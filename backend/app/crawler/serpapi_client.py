import requests
from typing import List, Dict, Any

class SearchException(Exception):
    pass

class SerpAPIClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def search_google(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": num_results
        }
        response = requests.get(self.base_url, params=params, timeout=15)
        if response.status_code != 200:
            raise SearchException("Search request failed")
        data = response.json()
        return data.get("organic_results", [])

def get_serpapi_client(app) -> SerpAPIClient:
    if not hasattr(app, "serpapi_client"):
        app.serpapi_client = SerpAPIClient(
            api_key=app.config.get("SERPAPI_KEY", "serpapi_key"),
            base_url=app.config.get("SERPAPI_BASE_URL", "https://serpapi.com/search")
        )
    return app.serpapi_client
