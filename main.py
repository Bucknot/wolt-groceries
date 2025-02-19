from services.wolt_service import WoltService
from services.chp_service import ChpService


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
    ("כוסמת 500 גרם", True),
    ("שוקולית 500 גרם", True),
    ("אינסטלטור נוזלי", True),
    ("עמק אצבעות", True),
    ("פיראוס בולגרית 16%", True),
    ("פתיתי מוצרלה 200", True),
    ("גד צפתית 5%", True),
    ("תנובה קוטג' 5%", True),
    ("עוף טוב צ'ונגו", False),
    ("ברילה 500 גרם", True)

]

ADDRESS = "ז'בוטינסקי 2, רמת גן"

def main():
    wolt_service = WoltService(ADDRESS, ITEMS_TO_SEARCH)
    wolt_service.fetch_items()
    wolt_service.map_venues()
    wolt_service.check_missing_items()
    wolt_service.calculate_average_prices()
    wolt_service.filter_duplicates()
    
    chp_service = ChpService(ADDRESS, ITEMS_TO_SEARCH)
    chp_service.fetch_items()
    
    # Generate combined report with .html extension
    wolt_service.generate_report("results.html", chp_service.get_complete_venues())

if __name__ == "__main__":
    main()