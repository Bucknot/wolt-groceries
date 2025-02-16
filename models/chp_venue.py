class ChpVenue:
    def __init__(self, name, website_url):
        self.name = name
        self.website_url = website_url
        self.items = {}  # Dict of item_name to (price, item_url)
        self.missing_items = set()

    def add_item(self, item_name, price, item_url=None):
        self.items[item_name] = (price, item_url)

    def add_missing_item(self, item_name):
        self.missing_items.add(item_name)

    def total_price(self):
        return round(sum(price for price, _ in self.items.values()), 2)

    def __str__(self):
        return self.name
