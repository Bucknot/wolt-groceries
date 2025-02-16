import requests

class WoltClient:
    def __init__(self, address):
        self.search_url = "https://restaurant-api.wolt.com/v1/pages/search"
        self.lat, self.lon = self._get_lat_lon_by_address(address)

    def search(self, query):
        json_data = {
            'q': query,
            'target': 'items',
            'lat': self.lat,
            'lon': self.lon,
        }
        response = requests.post(self.search_url, json=json_data)
        items = response.json().get('sections')[0].get('items')
        if not items:
            print(f"No venues found for item {query}")
            return []
        return items

    def _get_lat_lon_by_address(self, address):
        encoded_address = requests.utils.quote(address)
        url = f"https://nominatim.openstreetmap.org/search?q={encoded_address}&format=json"
        response = requests.get(url, headers={"User-Agent": "wolt-prices-comparer"})
        if response.status_code == 200:
            data = response.json()
            if data:
                location = data[0]
                return float(location['lat']), float(location['lon'])
            else:
                raise ValueError("No results found from Nominatim API")
        else:
            response.raise_for_status()