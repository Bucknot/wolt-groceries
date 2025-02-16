
class VenueItem:
    def __init__(self, name, id, searched_name, price, venue_id):
        self.name = name
        self.id = id
        self.searched_name = searched_name
        self.price = round(price, 2)
        self.url = f"https://wolt.com/he/isr/tel-aviv/venue/{venue_id}/itemid-{id}"

    def __str__(self):
        return f"{self.name} - ₪{self.price}"

    def __hash__(self):
        return hash(self.name + str(self.price))

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price
