import unittest
from unittest.mock import patch, Mock
from infrastructure.wolt_client import WoltClient
from services.wolt_service import WoltService
from models.venue import Venue
from models.venue_item import VenueItem

class TestWoltService(unittest.TestCase):
    def setUp(self):
        self.items_to_search = [("item1", True), ("item2", False)]
        with patch('infrastructure.wolt_client.WoltClient._get_lat_lon_by_address', return_value=(32.0853, 34.7818)):
            self.service = WoltService("Test Address", self.items_to_search)

    @patch('infrastructure.wolt_client.WoltClient.search')
    def test_fetch_items(self, mock_search):
        mock_search.return_value = [{'menu_item': {'name': 'item1'}, 'link': {'menu_item_details': {'venue_slug': 'venue1'}}}]
        self.service.fetch_items()
        self.assertIn('venue1', self.service.venue_to_items_map)

    def test_map_venues(self):
        self.service.venue_to_items_map = {
            'venue1': [{'name': 'item1', 'id': '1', 'searched_name': 'item1', 'price': 1000, 'is_wolt_plus': True, 'delivery_time': '30-40 min', 'is_available': True, 'venue_name': 'Test Venue'}]
        }
        self.service.map_venues()
        self.assertIn('venue1', self.service.venue_id_to_venue)

    def test_check_missing_items(self):
        venue = Venue("Test Venue", "venue1", True, "30-40 min", True)
        venue.add_item(VenueItem("item1", "1", "item1", 10.0, "venue1"))
        self.service.venue_id_to_venue = {'venue1': venue}
        self.service.check_missing_items()
        self.assertIn(VenueItem("item2", "2", "item2", 0, "venue1"), venue.missing_items)

    def test_calculate_average_prices(self):
        venue = Venue("Test Venue", "venue1", True, "30-40 min", True)
        venue.add_item(VenueItem("item1", "1", "item1", 10.0, "venue1"))
        self.service.venue_id_to_venue = {'venue1': venue}
        self.service.calculate_average_prices()
        self.assertEqual(self.service.average_price_map['item1'], 10.0)

    def test_filter_duplicates(self):
        venue = Venue("Test Venue", "venue1", True, "30-40 min", True)
        venue.add_item(VenueItem("item1", "1", "item1", 10.0, "venue1"))
        venue.add_item(VenueItem("item1 duplicate", "2", "item1", 15.0, "venue1"))
        self.service.venue_id_to_venue = {'venue1': venue}
        self.service.average_price_map = {'item1': 12.5}
        self.service.filter_duplicates()
        self.assertEqual(len(venue.items), 1)

if __name__ == '__main__':
    unittest.main()
