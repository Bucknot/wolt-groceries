from bidi.algorithm import get_display

class ConsoleReportFormatter:
    def generate_console_report(self, wolt_venues, average_price_map, items_to_search, chp_venues=None):
        print("\n=== Wolt Venues Report ===")
        self._generate_wolt_report(wolt_venues, average_price_map, items_to_search)
        
        if chp_venues:
            print("\n=== Online Stores Report ===")
            self._generate_chp_report(chp_venues)

        print("\n===================")
        self._print_statistics(wolt_venues, average_price_map, chp_venues)

    def _generate_wolt_report(self, venues, average_price_map, items_to_search):
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

    def _generate_chp_report(self, venues):
        if not venues:
            print("\nNo online stores found with all required items.")
            return

        print("\nOnline stores with complete baskets:")
        for venue in sorted(venues, key=lambda v: v.total_price()):
            print(f"\nStore: {get_display(venue.name)}")
            print(f"Website: {venue.website_url}")
            print(f"Total Price: {venue.total_price():.2f}")
            print("Items:")
            for item_name, (price, url) in venue.items.items():
                item_text = f"  - {get_display(item_name)}: {price:.2f}"
                if url:
                    item_text += f" ({url})"
                print(item_text)

    def print_venue(self, venue, average_price_map, rank=None):
        if rank:
            print(f"\nOption {rank}:")
        print(f"Venue: {get_display(venue.name)}")
        print(venue.url)
        print(f"Total Normalized Price: {venue.total_normalized_price(average_price_map)}")
        print("Items:")
        for item in venue.items:
            print(f"  - {get_display(item.name)}: {item.price}")

    def _print_statistics(self, venues, average_price_map, chp_venues=None):
        must_include_items = [venue for venue in venues.values() if all(
            any(item.searched_name == item_to_search for item in venue.items) 
            for item_to_search, must_include in average_price_map.items() if must_include
        )]
        
        num_venues = len(must_include_items)
        if num_venues > 0:
            total_prices = [venue.total_normalized_price(average_price_map) for venue in must_include_items]
            min_price = min(total_prices) if total_prices else 0
            max_price = max(total_prices) if total_prices else 0

            print(get_display(f"\nחנויות שמצאו את כל הפריטים החיוניים: {num_venues}"))
            stats_text = f"מחיר מינימלי: ₪{min_price}   |   מחיר מקסימלי: ₪{max_price}"
            
            # Add CHP venue statistics if available
            if chp_venues:
                chp_prices = [venue.total_price() for venue in chp_venues]
                if chp_prices:
                    chp_min_price = min(chp_prices)
                    stats_text += f"   |   מחיר מינימלי באונליין: ₪{chp_min_price:.2f}"
            
            print(get_display(stats_text))
