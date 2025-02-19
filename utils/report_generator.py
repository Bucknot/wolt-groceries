import os
from utils.html_report_formatter import HtmlReportFormatter
from utils.console_report_formatter import ConsoleReportFormatter

class ReportGenerator:
    def __init__(self, items_to_search):
        self.items_to_search = items_to_search
        self.console_report_formatter = ConsoleReportFormatter()

    def generate_report(self, file_name, venue_id_to_venue, average_price_map, chp_venues=None):
        print("Generating reports...")
        base_name, extension = os.path.splitext(file_name)
        html_file = f"{base_name}.html"
        
        result_formatter = HtmlReportFormatter(html_file)
        result_formatter.set_items_to_search(self.items_to_search)
        result_formatter.venue_id_to_venue = venue_id_to_venue
        
        must_include_items = [item_to_search for item_to_search, must_include in self.items_to_search if must_include]
        sorted_venues = sorted(
            [venue for venue in venue_id_to_venue.values() if all(
                any(item.searched_name == item_to_search for item in venue.items) for item_to_search in must_include_items)],
            key=lambda v: v.total_normalized_price(average_price_map)
        )
        
        if sorted_venues:
            # Add statistics at the top
            result_formatter.add_statistics(sorted_venues, average_price_map, chp_venues)
            
            # Add cheapest venue as main card with special styling
            result_formatter.add_venue_card(
                sorted_venues[0], 
                average_price_map,
                "החנות הזולה ביותר",
                "cheapest-venue"
            )
            
            # Add other venues in carousel
            if len(sorted_venues) > 1:
                result_formatter.add_carousel(
                    sorted_venues[1:4],
                    average_price_map,
                    "other",
                    "אפשרויות נוספות"
                )
        else:
            # Handle case when no venues have all required items
            venues_with_one_missing_item = [
                venue for venue in venue_id_to_venue.values()
                if len([item for item in venue.missing_items if any(
                    item.searched_name == item_to_search and must_include 
                    for item_to_search, must_include in self.items_to_search)]) == 1
            ]
            venues_with_one_missing_item.sort(key=lambda v: v.total_normalized_price(average_price_map))
            
            if venues_with_one_missing_item:
                result_formatter.add_heading("חנויות עם פריט חיוני אחד חסר", level=2)
                for venue in venues_with_one_missing_item[:3]:
                    result_formatter.add_venue_card(venue, average_price_map)

        # Add most expensive venue with grey styling
        most_expensive_venue = max(
            [venue for venue in venue_id_to_venue.values() if all(
                any(item.searched_name == item_to_search for item in venue.items) 
                for item_to_search in must_include_items)],
            key=lambda v: v.total_normalized_price(average_price_map),
            default=None
        )
        if most_expensive_venue:
            result_formatter.add_venue_card(
                most_expensive_venue,
                average_price_map,
                "החנות היקרה ביותר",
                "most-expensive"
            )
        
        # Add CHP venues section
        if chp_venues:
            result_formatter.add_chp_venues(chp_venues)
            
        # Save the HTML report
        result_formatter.save()
        print("Report saved to", result_formatter.file_name)
        
        # Generate console report
        self.console_report_formatter.generate_console_report(
            venue_id_to_venue,
            average_price_map,
            self.items_to_search,
            chp_venues
        )
        
        # Open the created HTML file in default browser
        os.system(f"open \"{result_formatter.file_name}\"")
