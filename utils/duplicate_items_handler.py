class DuplicateItemsHandler:
    @staticmethod
    def filter_out_duplicates(items, average_price_map):
        searched_item = items[0].searched_name
        average_price = DuplicateItemsHandler._calculate_average_price(items, average_price_map)
        # print("\n\n---------------------")
        # print(f"Filtering out duplicates for item: {searched_item}")
        # print(f"Average price: ₪{average_price}")
        # print("Contestants: ")
        # for item in items:
        #     print(f"  - {item.name}: ₪{item.price}")

        # Filter out items that are more than 50% cheaper or more expensive than the average price
        avg_price_filtered_items = [
            item for item in items
            if average_price * 0.5 <= item.price <= average_price * 1.5
        ]
        if not avg_price_filtered_items:
            # print("No items within 50% of the average price")
            return None

        if len(avg_price_filtered_items) == 1:
            # print(f"Winner: {avg_price_filtered_items[0]} (only one item within 50% range)")
            return avg_price_filtered_items[0]

        exact_match = DuplicateItemsHandler._first_exact_match(avg_price_filtered_items, searched_item)
        if exact_match:
            # print(f"Winner: {exact_match} (exact match)")
            return exact_match

        similar_words_items = DuplicateItemsHandler._most_similar_words(avg_price_filtered_items, searched_item)
        if len(similar_words_items) == 1:
            # print(f"Winner: {similar_words_items[0]} (words count match)")
            return similar_words_items[0]

        # check for item with lowest words counts
        similar_words_items.sort(key=lambda x: len(x.name.split()))
        # print(f"Winner: {similar_words_items[0]} (lowest words count)")
        return similar_words_items[0]

    @staticmethod
    def _calculate_average_price(items, average_price_map):
        searched_item = items[0].searched_name
        return average_price_map.get(searched_item, 0)

    @staticmethod
    def _first_exact_match(items, searched_item):
        for item in items:
            if item.name == searched_item:
                return item
        return None

    @staticmethod
    def _most_similar_words(items, searched_item):
        deconstructed_searched_item = searched_item.split()
        hits = []
        for item in items:
            deconstructed_item = item.name.split()
            hits.append((item, len(set(deconstructed_searched_item) & set(deconstructed_item))))
        hits.sort(key=lambda x: x[1], reverse=True)
        return [item for item, hit in hits if hit == hits[0][1]]