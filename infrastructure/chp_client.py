import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlencode

class ChpClient:
    def __init__(self, address):
        self.address = address
        self.base_url = "https://chp.co.il/main_page/compare_results"

    def search(self, item_query):
        # Manually build query string
        params = {
            'shopping_address': self.address,
            'shopping_address_street_id': '0',
            'shopping_address_city_id': '0',
            'product_name_or_barcode': item_query,
            'product_barcode': '0',
            'from': '0',
            'num_results': '20'
        }
        
        # Manually encode each parameter and build the URL
        encoded_params = []
        for key, value in params.items():
            encoded_params.append(f"{key}={quote(value)}")
        url = f"{self.base_url}?{'&'.join(encoded_params)}"
        
        headers = {
            'User-Agent': 'wolt-prices-comparer'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        
        # Find all tables and look for the online stores table
        tables = soup.find_all('table', class_='results-table')
        online_stores_table = None
        
        # Look for the header that indicates online stores results
        for h4 in soup.find_all('h4'):
            if 'תוצאות מחנויות באינטרנט' in h4.text:
                online_stores_table = h4.find_next('table', class_='results-table')
                break
        
        if not online_stores_table:
            return results

        # Process rows in the online stores table
        for row in online_stores_table.find_all('tr'):
            if row.find('th') or 'display_when_narrow' in row.get('class', []):
                continue
                
            cols = row.find_all('td')
            if len(cols) >= 5:
                chain_name = cols[0].text.strip()
                store_link = cols[1].find('a')
                store_name = store_link.text.strip() if store_link else cols[1].text.strip()
                website = cols[2].text.strip()
                item_url = store_link['href'] if store_link else None
                try:
                    price = float(cols[4].text.strip().replace('₪', '').strip())
                except ValueError:
                    continue
                
                results.append({
                    'chain_name': chain_name,
                    'store_name': store_name,
                    'website': website,
                    'item_url': item_url,
                    'price': price
                })

        return results
