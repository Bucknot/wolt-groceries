import unittest
from utils.docx_results_formatter import DocxResultFormatter
from models.venue import Venue
from models.venue_item import VenueItem
import os

class TestDocxResultFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = DocxResultFormatter("test_results.docx")
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

    def tearDown(self):
        if os.path.exists("test_results.docx"):
            os.remove("test_results.docx")

if __name__ == '__main__':
    unittest.main()
