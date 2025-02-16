from models.venue_item import VenueItem


class Venue:
    def __init__(self, name, slug, is_wolt_plus, delivery_time, is_available):
        self.name = name
        self.items = set()
        self.missing_items = set()
        self.is_wolt_plus = is_wolt_plus
        self.delivery_time = delivery_time
        self.errors = []
        self.is_available = is_available
        self.slug = slug
        self.url = f"https://wolt.com/he/isr/tel-aviv/venue/{slug}"

    def add_item(self, item: VenueItem):
        self.items.add(item)

    def add_missing_item(self, item: VenueItem):
        self.missing_items.add(item)

    def add_error(self, error):
        self.errors.append(error)

    def total_price(self):
        return round(sum(item.price for item in self.items), 2)

    def total_normalized_price(self, average_price_map):
        total_price = self.total_price()
        for missing_item in self.missing_items:
            total_price += average_price_map.get(missing_item.searched_name, 0)
        return round(total_price, 2)

    def __hash__(self):
        return hash(self.v_id)

    def __eq__(self, other):
        return self.v_id == other.v_id

    def __str__(self):
        return self.name