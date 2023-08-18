import requests
from typing import List, Optional, Any

class VectifyClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'api_key': self.api_key
        }

    def _request(self, method: str, endpoint: str, data: Optional[dict] = None):
        url = f"{self.base_url}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, headers=self.headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=self.headers)
        
        response.raise_for_status()  # This will raise an exception for HTTP error codes.
        return response.json()

    def get_usage(self) -> dict:
        return self._request("GET", "/usage")

    def get_sources(self) -> List[str]:
        return self._request("GET", "/sources")

    def get_agents(self) -> List[str]:
        return self._request("GET", "/agents")

    def get_models(self) -> List[str]:
        return self._request("GET", "/models")

    def retrieve(self, query: str, top_k: int, sources: List[str]) -> dict:
        data = {
            'query': query,
            'top_k': top_k,
            'sources': sources
        }
        return self._request("POST", "/retrieve", data)

    def chat(self, query: Optional[str], agent: str, model: Optional[str], chat_history: Optional[List[Any]]) -> dict:
        data = {
            'query': query,
            'agent': agent,
            'model': model,
            'chat_history': chat_history
        }
        return self._request("POST", "/chat", data)

