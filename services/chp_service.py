from bidi.algorithm import get_display

from infrastructure.chp_client import ChpClient
from models.chp_venue import ChpVenue

class ChpService:
    def __init__(self, address, items_to_search):
        self.address = address
        self.items_to_search = items_to_search
        self.chp_client = ChpClient(address)
        self.venues = {}  # website -> ChpVenue

    def fetch_items(self):
        print("\nFetching items from CHP...")
        total_items_found = 0
        print("Searching for {len(self.items_to_search)} items in non-Wolt venues...")
        for item_to_search, must_include in self.items_to_search:
                
            results = self.chp_client.search(item_to_search)
            total_items_found += len(results)
            
            for result in results:
                website = result['website']
                if website not in self.venues:
                    self.venues[website] = ChpVenue(result['store_name'], website)
                
                self.venues[website].add_item(
                    item_to_search,
                    result['price'],
                    result['item_url']
                )
        
        print(f"Found {total_items_found} items from {len(self.venues)} online stores.")
        
        # Mark missing items
        for website, venue in self.venues.items():
            for item_to_search, must_include in self.items_to_search:
                if must_include and item_to_search not in venue.items:
                    venue.add_missing_item(item_to_search)

    def get_complete_venues(self):
        """Return venues that have all must-include items"""
        must_include_items = {item[0] for item in self.items_to_search if item[1]}
        return [
            venue for venue in self.venues.values()
            if not any(item in venue.missing_items for item in must_include_items)
        ]
