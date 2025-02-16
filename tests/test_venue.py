import unittest
from models.venue import Venue
from models.venue_item import VenueItem

class TestVenue(unittest.TestCase):
    def setUp(self):
        self.venue = Venue("Test Venue", "test_slug", True, "30-40 min", True)

    def test_add_item(self):
        item = VenueItem("item1", "1", "item1", 10.0, "test_slug")
        self.venue.add_item(item)
        self.assertIn(item, self.venue.items)

    def test_add_missing_item(self):
        item = VenueItem("item1", "1", "item1", 10.0, "test_slug")
        self.venue.add_missing_item(item)
        self.assertIn(item, self.venue.missing_items)

    def test_total_price(self):
        item1 = VenueItem("item1", "1", "item1", 10.0, "test_slug")
        item2 = VenueItem("item2", "2", "item2", 20.0, "test_slug")
        self.venue.add_item(item1)
        self.venue.add_item(item2)
        self.assertEqual(self.venue.total_price(), 30.0)

    def test_total_normalized_price(self):
        item1 = VenueItem("item1", "1", "item1", 10.0, "test_slug")
        self.venue.add_item(item1)
        missing_item = VenueItem("item2", "2", "item2", 0, "test_slug")
        self.venue.add_missing_item(missing_item)
        average_price_map = {"item2": 20.0}
        self.assertEqual(self.venue.total_normalized_price(average_price_map), 30.0)

if __name__ == '__main__':
    unittest.main()
