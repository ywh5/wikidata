import requests
import json
from typing import Dict, List, Any
import time
from pathlib import Path

class WikidataFetcher:
    def __init__(self):
        self.base_url = "https://www.wikidata.org/w/api.php"
        self.headers = {
            "User-Agent": "WikidataDataFetcher/1.0 (Python/3.8)"
        }
        
    def fetch_entity(self, entity_id: str) -> Dict[str, Any]:
        """Fetch a single entity from Wikidata."""
        params = {
            "action": "wbgetentities",
            "ids": entity_id,
            "format": "json",
            "languages": "en",
            "props": "labels|descriptions|claims|sitelinks"
        }
        
        response = requests.get(self.base_url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()["entities"][entity_id]
    
    def fetch_multiple_entities(self, entity_ids: List[str], batch_size: int = 50) -> Dict[str, Any]:
        """Fetch multiple entities in batches."""
        all_entities = {}
        
        for i in range(0, len(entity_ids), batch_size):
            batch = entity_ids[i:i + batch_size]
            params = {
                "action": "wbgetentities",
                "ids": "|".join(batch),
                "format": "json",
                "languages": "en",
                "props": "labels|descriptions|claims|sitelinks"
            }
            
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            all_entities.update(response.json()["entities"])
            
            # Respect rate limits
            time.sleep(1)
            
        return all_entities
    
    def save_to_json(self, data: Dict[str, Any], filename: str):
        """Save fetched data to a JSON file."""
        output_dir = Path("data")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    fetcher = WikidataFetcher()
    
    # Example: Fetch data about China (Q148)
    china_data = fetcher.fetch_entity("Q148")
    fetcher.save_to_json(china_data, "china_data.json")
    
    # Example: Fetch data about multiple countries
    country_ids = ["Q148", "Q30", "Q145"]  # China, USA, UK
    countries_data = fetcher.fetch_multiple_entities(country_ids)
    fetcher.save_to_json(countries_data, "countries_data.json")

if __name__ == "__main__":
    main() 