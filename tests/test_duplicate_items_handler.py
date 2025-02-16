import unittest
from models.venue_item import VenueItem
from utils.duplicate_items_handler import DuplicateItemsHandler

class TestDuplicateItemsHandler(unittest.TestCase):
    def test_exact_name_match(self):
        items = [
            VenueItem("item1", "1", "item1 extra", 10.0, "venue1"),
            VenueItem("item1 extra", "2", "item1 extra", 15.0, "venue1"),
            VenueItem("item1 extra words", "3", "item1 extra", 20.0, "venue1")
        ]
        average_price_map = {"item1 extra": 15.0}
        filtered_item = DuplicateItemsHandler.filter_out_duplicates(items, average_price_map)
        self.assertEqual(filtered_item.name, "item1 extra")

    def test_exclude_expensive_items(self):
        items = [
            VenueItem("item1", "1", "item1", 10.0, "venue1"),
            VenueItem("item1 expensive", "2", "item1", 25.0, "venue1"),
            VenueItem("item1 very expensive", "3", "item1", 30.0, "venue1")
        ]
        average_price_map = {"item1": 15.0}
        filtered_item = DuplicateItemsHandler.filter_out_duplicates(items, average_price_map)
        self.assertEqual(filtered_item.price, 10.0)

    def test_more_words_in_common(self):
        items = [
            VenueItem("item1 other words", "1", "item1 extra words", 15.0, "venue1"),
            VenueItem("item1 extra mambo jambo", "2", "item1 extra words", 15.0, "venue1"),
            VenueItem("item1 extra words long", "3", "item1 extra words", 16.0, "venue1")
        ]
        average_price_map = {"item1 extra words": 15.0}
        filtered_item = DuplicateItemsHandler.filter_out_duplicates(items, average_price_map)
        self.assertEqual(filtered_item.name, "item1 extra words long")

    def test_fewer_words_match(self):
        items = [
            VenueItem("item1", "1", "item1", 10.0, "venue1"),
            VenueItem("item1 extra", "2", "item1", 15.0, "venue1"),
            VenueItem("item1 extra words", "3", "item1", 20.0, "venue1")
        ]
        average_price_map = {"item1": 15.0}
        filtered_item = DuplicateItemsHandler.filter_out_duplicates(items, average_price_map)
        self.assertEqual(filtered_item.name, "item1")

if __name__ == '__main__':
    unittest.main()
