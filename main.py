
from services.wolt_service import WoltService


# A list of tuples where each tuple contains an item to search and a boolean indicating whether
#  the item must be included in the search results.
#
# Try to include as many words as possible in the item name to increase the chances of finding
#  the correct item and differentiate it from other similar items.
#
# for example:
# use "קורנפלקס אלופים 850 גרם" instead of "קורנפלקס"
# use "שעועית לבנה סנפרוסט" instead of "שעועית"

ITEMS_TO_SEARCH = [
    ("קורנפלקס אלופים 850 גרם", True),
    ("שעועית לבנה סנפרוסט 800 גרם", True),
    ("כוסמת 500 גרם", True),
    ("שוקולית 500 גרם", False),
    ("אינסטלטור נוזלי", False),
    ("גבינה צהובה עמק 28% 400 גרם", True),
    ("ביצים L 12", True),
    ("קוקה קולה זירו 1.5 ליטר", True),
]

ADDRESS = "ז'בוטינסקי 2, רמת גן"

def main():
    wolt_service = WoltService(ADDRESS, ITEMS_TO_SEARCH)
    wolt_service.fetch_items()
    wolt_service.map_venues()
    wolt_service.check_missing_items()
    wolt_service.calculate_average_prices()
    wolt_service.filter_duplicates()
    wolt_service.generate_report("results.docx")

if __name__ == "__main__":
    main()