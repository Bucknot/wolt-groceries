import os  # New import
from infrastructure.wolt_client import WoltClient
from models.venue import Venue
from models.venue_item import VenueItem
from utils.duplicate_items_handler import DuplicateItemsHandler
from utils.html_report_formatter import HtmlReportFormatter  # Change import
from utils.console_report_formatter import ConsoleReportFormatter
from bidi.algorithm import get_display

class WoltService:
    def __init__(self, address, items_to_search):
        self.address = address
        self.items_to_search = items_to_search
        self.wolt_client = WoltClient(address)
        self.venue_id_to_venue = {}
        self.venue_to_items_map = {}
        self.item_price_map = {item[0]: [] for item in items_to_search}
        self.average_price_map = {}
        self.console_report_formatter = ConsoleReportFormatter()

    def fetch_items(self):
        print("Fetching items from Wolt client...")
        total_items_fetched = 0
        print(f"Searching for {len(self.items_to_search)} items in Wolt venues...")
        for item_to_search, must_include in self.items_to_search:
            items = self.wolt_client.search(item_to_search)
            total_items_fetched += len(items)
            venue_to_items = self.sort_found_items_by_venue(items, item_to_search)
            for venue_id, venue_items in venue_to_items.items():
                if venue_id not in self.venue_to_items_map:
                    self.venue_to_items_map[venue_id] = []
                self.venue_to_items_map[venue_id].extend(venue_items)
        print(f"Finished fetching {total_items_fetched} items.")

    def map_venues(self):
        print("Mapping venues...")
        total_venues_mapped = 0
        for venue_id, venue_items in self.venue_to_items_map.items():
            is_wolt_plus = venue_items[0].get('is_wolt_plus', venue_items[0].get('show_wolt_plus'))
            delivery_time = venue_items[0].get('delivery_time', venue_items[0].get('estimate_range'))
            venue = Venue(venue_items[0]['venue_name'], venue_id, is_wolt_plus, delivery_time, venue_items[0]['is_available'])
            self.venue_id_to_venue[venue_id] = venue
            for item in venue_items:
                venue_item = VenueItem(item['name'], item['id'], item['searched_name'], item['price'] / 100, venue.slug)
                venue.add_item(venue_item)
            total_venues_mapped += 1
        print(f"Finished mapping {total_venues_mapped} venues.")

    def check_missing_items(self):
        print("Checking for missing items in venues...")
        total_missing_items = 0
        for venue in self.venue_id_to_venue.values():
            for item_to_search, must_include in self.items_to_search:
                if not any(item.searched_name == item_to_search for item in venue.items):
                    missing_item = VenueItem(item_to_search, '', item_to_search, 0, venue.slug)
                    venue.add_missing_item(missing_item)
                    total_missing_items += 1
        print(f"Finished checking for missing items. Found {total_missing_items} missing items.")

    def calculate_average_prices(self):
        print("Calculating average prices...")
        total_prices_calculated = 0
        for item_to_search, must_include in self.items_to_search:
            for venue in self.venue_id_to_venue.values():
                matching_items = [item for item in venue.items if item.searched_name == item_to_search]
                if len(matching_items) == 1:
                    self.item_price_map[item_to_search].append(matching_items[0].price)
                    total_prices_calculated += 1
        self.average_price_map = {item: (round(sum(prices) / len(prices), 2)) if prices else 0 for item, prices in self.item_price_map.items()}
        print(f"Finished calculating average prices for {total_prices_calculated} items.")

    def filter_duplicates(self):
        print("Filtering duplicate items...")
        total_duplicates_filtered = 0
        total_venues_processed = 0
        for venue in self.venue_id_to_venue.values():
            for item_to_search, must_include in self.items_to_search:
                matching_items = [item for item in venue.items if item.searched_name == item_to_search]
                if len(matching_items) > 1:
                    filtered_item = DuplicateItemsHandler.filter_out_duplicates(matching_items, self.average_price_map)
                    venue.items = {item for item in venue.items if item.searched_name != item_to_search}
                    if filtered_item:
                        venue.add_item(filtered_item)
                    total_duplicates_filtered += len(matching_items) - 1
            total_venues_processed += 1
        print(f"Finished filtering {total_duplicates_filtered} duplicate items from {total_venues_processed} venues.")

    def generate_report(self, file_name, chp_venues=None):
        print("Generating reports...")
        # Change to HtmlReportFormatter and ensure .html extension
        base_name, extension = os.path.splitext(file_name)
        html_file = f"{base_name}.html"
        
        # Initialize formatter and set items to search
        result_formatter = HtmlReportFormatter(html_file)
        result_formatter.set_items_to_search(self.items_to_search)  # Add this line
        
        must_include_items = [item_to_search for item_to_search, must_include in self.items_to_search if must_include]
        sorted_venues = sorted(
            [venue for venue in self.venue_id_to_venue.values() if all(
                any(item.searched_name == item_to_search for item in venue.items) for item_to_search in must_include_items)],
            key=lambda v: v.total_normalized_price(self.average_price_map)
        )
        
        if sorted_venues:
            # Add statistics at the top
            result_formatter.add_statistics(sorted_venues, self.average_price_map, chp_venues)
            
            # Add cheapest venue as main card with special styling
            result_formatter.add_venue_card(
                sorted_venues[0], 
                self.average_price_map,
                "החנות הזולה ביותר",
                "cheapest-venue"  # Changed from bg-light
            )
            
            # Add other venues in carousel
            if len(sorted_venues) > 1:
                result_formatter.add_carousel(
                    sorted_venues[1:4],  # Show up to 3 other options
                    self.average_price_map,
                    "other",
                    "אפשרויות נוספות"
                )
        else:
            # Handle case when no venues have all required items
            venues_with_one_missing_item = [
                venue for venue in self.venue_id_to_venue.values()
                if len([item for item in venue.missing_items if any(
                    item.searched_name == item_to_search and must_include 
                    for item_to_search, must_include in self.items_to_search)]) == 1
            ]
            venues_with_one_missing_item.sort(key=lambda v: v.total_normalized_price(self.average_price_map))
            
            if venues_with_one_missing_item:
                result_formatter.add_heading("חנויות עם פריט חיוני אחד חסר", level=2)
                for venue in venues_with_one_missing_item[:3]:
                    result_formatter.add_venue_card(venue, self.average_price_map)

        # Add most expensive venue with grey styling
        most_expensive_venue = max(
            [venue for venue in self.venue_id_to_venue.values() if all(
                any(item.searched_name == item_to_search for item in venue.items) 
                for item_to_search in must_include_items)],
            key=lambda v: v.total_normalized_price(self.average_price_map),
            default=None
        )
        if most_expensive_venue:
            result_formatter.add_venue_card(
                most_expensive_venue,
                self.average_price_map,
                "החנות היקרה ביותר",
                "most-expensive"  # Changed from bg-secondary text-white
            )
        
        # Add CHP venues section
        if chp_venues:
            result_formatter.add_chp_venues(chp_venues)
            
        # Save the HTML report
        result_formatter.save()
        print("Report saved to", result_formatter.file_name)
        
        # Generate console report
        self.console_report_formatter.generate_console_report(
            self.venue_id_to_venue,
            self.average_price_map,
            self.items_to_search,
            chp_venues
        )
        
        # Open the created HTML file in default browser
        os.system(f"open \"{result_formatter.file_name}\"")

    def sort_found_items_by_venue(self, items, item_to_search):
        venue_to_items = {}
        for item in items:
            menu_item = item.get('menu_item')
            venue_id = item.get('link').get('menu_item_details').get('venue_slug')
            if venue_id not in venue_to_items:
                venue_to_items[venue_id] = []
            menu_item['searched_name'] = item_to_search
            venue_to_items[venue_id].append(menu_item)
        return venue_to_items
