from bidi.algorithm import get_display

class ConsoleReportFormatter:
    def generate_console_report(self, venues, average_price_map, items_to_search):
        must_include_items = [item_to_search for item_to_search, must_include in items_to_search if must_include]
        sorted_venues = sorted(
            [venue for venue in venues.values() if all(
                any(item.searched_name == item_to_search for item in venue.items) for item_to_search in must_include_items)],
            key=lambda v: v.total_normalized_price(average_price_map)
        )
        if sorted_venues:
            print("\n\n=====================")
            print("\nCheapest total:")
            self.print_venue(sorted_venues[0], average_price_map)
            print("\n=====================\n\n")

            if len(sorted_venues) > 1:
                print("\nOther Options:")
                for rank, venue in enumerate(sorted_venues[1:3], start=2):
                    self.print_venue(venue, average_price_map, rank)
        else:
            print("\nNo venues found that sell all must-have items.")
            venues_with_one_missing_item = [
                venue for venue in venues.values()
                if len([item for item in venue.missing_items if any(
                    item.searched_name == item_to_search and must_include for item_to_search, must_include in items_to_search)]) == 1
            ]
            venues_with_one_missing_item.sort(key=lambda v: v.total_normalized_price(average_price_map))
            print("\nTop 3 venues with at least one missing must-have item:")
            for venue in venues_with_one_missing_item[:3]:
                self.print_venue(venue, average_price_map)
        most_expensive_venue = max(
            [venue for venue in venues.values() if all(
                any(item.searched_name == item_to_search for item in venue.items) for item_to_search in must_include_items)],
            key=lambda v: v.total_normalized_price(average_price_map),
            default=None
        )
        if most_expensive_venue:
            print("---------------------")
            print("\nMost Expensive Venue:")
            self.print_venue(most_expensive_venue, average_price_map)

    def print_venue(self, venue, average_price_map, rank=None):
        if rank:
            print(f"\nOption {rank}:")
        print(f"Venue: {get_display(venue.name)}")  # Updated
        print(venue.url)  # New
        print(f"Total Normalized Price: {venue.total_normalized_price(average_price_map)}")
        print("Items:")
        for item in venue.items:
            print(f"  - {get_display(item.name)}: {item.price}")  # Updated
