import unittest
from unittest.mock import patch, Mock
from infrastructure.wolt_client import WoltClient

class TestWoltClient(unittest.TestCase):
    @patch('infrastructure.wolt_client.requests.get')
    def test_get_lat_lon_by_address(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'lat': '32.0853', 'lon': '34.7818'}]
        mock_get.return_value = mock_response

        client = WoltClient("Tel Aviv")
        lat, lon = client._get_lat_lon_by_address("Tel Aviv")
        self.assertEqual(lat, 32.0853)
        self.assertEqual(lon, 34.7818)

    @patch('infrastructure.wolt_client.requests.post')
    def test_search(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            'sections': [{'items': [{'menu_item': {'name': 'item1'}, 'link': {'menu_item_details': {'venue_slug': 'venue1'}}}]}]
        }
        mock_post.return_value = mock_response

        client = WoltClient("Tel Aviv")
        items = client.search("item1")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['menu_item']['name'], 'item1')

if __name__ == '__main__':
    unittest.main()
