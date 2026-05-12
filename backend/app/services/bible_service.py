import requests
from flask import current_app


class BibleService:
    def search_passages(self, query):
        api_key = current_app.config["BIBLE_API_KEY"]
        base_url = current_app.config["BIBLE_API_BASE_URL"]
        if not api_key:
            return []

        response = requests.get(
            f"{base_url}/bibles",
            headers={"api-key": api_key},
            timeout=15,
        )
        response.raise_for_status()
        return response.json().get("data", [])
