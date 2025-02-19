import unittest
from unittest.mock import Mock, patch
from utils.docx_results_formatter import DocxResultFormatter
from models.venue import Venue
from models.venue_item import VenueItem
from models.chp_venue import ChpVenue
import os

class TestDocxResultFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = DocxResultFormatter("test.docx")
        self.venue = Venue("Test Venue", "test_slug", True, "30-40 min", True)
        self.item = VenueItem("item1", "1", "item1", 10.0, "test_slug")
        self.venue.add_item(self.item)

    def test_add_heading(self):
        self.formatter.add_heading("Test Heading", level=1)
        self.assertEqual(self.formatter.document.paragraphs[0].text, "Test Heading")

    def test_add_paragraph(self):
        self.formatter.add_paragraph("Test Paragraph")
        self.assertEqual(self.formatter.document.paragraphs[0].text, "Test Paragraph")

    def test_add_venue(self):
        self.formatter.add_venue(self.venue, {"item1": 10.0})
        self.assertIn("Test Venue", self.formatter.document.paragraphs[0].text)

    def test_add_chp_venues(self):
        # Create test CHP venues
        venue1 = ChpVenue("Test Store 1", "http://store1.com")
        venue1.add_item("item1", 10.0, "http://store1.com/item1")
        venue1.add_item("item2", 20.0, "http://store1.com/item2")

        venue2 = ChpVenue("Test Store 2", "http://store2.com")
        venue2.add_item("item1", 15.0, "http://store2.com/item1")
        
        chp_venues = [venue1, venue2]
        
        # Test adding CHP venues
        self.formatter.add_chp_venues(chp_venues)
        
        # Verify document structure (check if paragraphs were added)
        self.assertTrue(any('חנויות אונליין' in p.text for p in self.formatter.document.paragraphs))

    def test_statistics_with_chp_venues(self):
        # Create test data
        venues = [Mock(total_normalized_price=lambda x: 100)]
        average_price_map = {}
        
        chp_venue = ChpVenue("Online Store", "http://store.com")
        chp_venue.add_item("item1", 90.0)
        chp_venues = [chp_venue]

        # Add statistics with CHP venues
        self.formatter.add_statistics(venues, average_price_map, chp_venues)

        # Verify statistics include online price
        stats_paragraphs = [p for p in self.formatter.document.paragraphs if 'מחיר מינימלי באונליין' in p.text]
        self.assertTrue(len(stats_paragraphs) > 0)

    def tearDown(self):
        if os.path.exists("test_results.docx"):
            os.remove("test_results.docx")

if __name__ == '__main__':
    unittest.main()
