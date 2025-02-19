import os
from datetime import datetime

__all__ = ['HtmlReportFormatter']

class HtmlReportFormatter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.content = []
        self.statistics = {}
        self.items_to_search = []  # Initialize empty list for searched items
        self._saved_content = []  # Add this line
        self.average_price_map = {}  # Add this line
        self._init_template()

    def set_items_to_search(self, items):
        """Set the items to search after initialization"""
        self.items_to_search = items

    def _init_template(self):
        self.html_template = '''
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>השוואת מחירים - {date}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #009de0;
            --secondary-color: #5c636a;
            --success-color: #198754;
            --bg-light: #f8f9fa;
        }}
        
        body {{
            background-color: var(--bg-light);
        }}
        
        .venue-card {{
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
            background: white;
            margin: 1rem 0;
            padding: 1.5rem;
        }}
        
        .cheapest-venue {{
            border: 3px solid var(--success-color);
            background-color: rgba(25, 135, 84, 0.05);
            box-shadow: 0 4px 12px rgba(25, 135, 84, 0.15);
        }}
        
        .most-expensive {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            color: #6c757d;
        }}
        
        .most-expensive .price-tag {{
            color: #6c757d;
        }}
        
        .venue-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stats-section {{
            background-color: var(--primary-color);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
        }}
        
        .price-tag {{
            font-size: 1.5rem;
            color: var(--success-color);
            font-weight: bold;
        }}
        
        .item-list {{
            list-style-type: none;
            padding: 0;
        }}
        
        .item-list li {{
            padding: 0.5rem 0;
            border-bottom: 1px solid #eee;
        }}
        
        .missing-items {{
            color: var(--secondary-color);
            font-size: 0.9rem;
        }}
        
        .carousel-control-prev,
        .carousel-control-next {{
            width: 5%;
            background-color: rgba(0,0,0,0.2);
            border-radius: 50%;
            height: 50px;
            top: 50%;
            transform: translateY(-50%);
        }}
        
        .online-stores {{
            background-color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-top: 2rem;
        }}
        
        .section-title {{
            color: var(--primary-color);
            margin-bottom: 1.5rem;
            font-weight: bold;
        }}
        
        @media (max-width: 768px) {{
            .venue-card {{
                margin: 0.5rem 0;
                padding: 1rem;
            }}
            
            .stats-section {{
                padding: 1rem;
                margin-bottom: 1rem;
            }}
        }}
        
        .main-header {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        
        .main-title {{
            font-size: 2.5rem;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }}
        
        .sub-title {{
            font-size: 1.2rem;
            color: var(--secondary-color);
        }}
        
        .items-carousel {{
            margin: 2rem 0;
            padding: 1rem;
            background: white;
            border-radius: 15px;
        }}
        
        .search-item {{
            padding: 0.5rem 1rem;
            margin: 0.25rem;
            border-radius: 8px;
            display: inline-block;
            font-weight: 500;
            color: var(--bg-light);
            z-index: 1;
        }}
        
        .must-include {{
            background-color: var(--primary-color) !important;
            color: var(--bg-light) !important;
            border: 1px solid var(--primary-color);
            z-index: 2;
            opacity: 0.8;
        }}
        
        .optional {{
            background-color: var(--secondary-color) !important;
            color: var(--bg-light) !important;
            border: 1px solid var(--secondary-color);
            opacity: 0.8;
            z-index: 2;
        }}
        
        .stats-section {{
            font-size: 1.2rem;
        }}
        
        .stats-number {{
            font-size: 1.4rem;
            font-weight: bold;
        }}
        
        .tooltip {{
            position: relative;
            display: inline-block;
            cursor: help;
        }}
        
        .tooltip .tooltiptext {{
            visibility: hidden;
            width: 120px;
            background-color: var(--secondary-color);
            color: white;
            text-align: center;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -60px;
            opacity: 0;
            transition: opacity 0.3s;
        }}
        
        .tooltip:hover .tooltiptext {{
            visibility: visible;
            opacity: 1;
        }}
        
        .stats-main {{
            font-size: 1.4rem;
            text-align: center;
            margin-bottom: 1.5rem;
        }}
        
        .carousel-inner {{
            padding: 1rem 3rem;
        }}
        
        .carousel-control-prev,
        .carousel-control-next {{
            width: 3rem;
            background-color: rgba(0,0,0,0.2);
            border-radius: 50%;
            height: 3rem;
            top: 50%;
            transform: translateY(-50%);
            margin: 0 1rem;
        }}
        .carousel {{
            margin: 2rem 0;
        }}
        
        .carousel-inner {{
            padding: 0.5rem;
        }}
        
        .carousel-control-prev,
        .carousel-control-next {{
            width: 40px;
            height: 40px;
            background-color: rgba(0, 0, 0, 0.3);
            border-radius: 50%;
            top: 50%;
            transform: translateY(-50%);
            opacity: 0.8;
            display: flex !important;  /* Always show controls */
            align-items: center;
            justify-content: center;
            z-index: 100;
        }}
        
        .carousel-control-prev {{
            left: -20px;
        }}
        
        .carousel-control-next {{
            right: -20px;
        }}
        
        .carousel-control-prev.disabled,
        .carousel-control-next.disabled {{
            opacity: 0.3;
            cursor: not-allowed;
        }}
        
        @media (max-width: 768px) {{
            .carousel-control-prev {{
                left: 0;
            }}
            
            .carousel-control-next {{
                right: 0;
            }}
            
            .carousel-inner {{
                padding: 0;
            }}
        }}
        
        .container {{
            max-width: 800px !important;
            margin: 0 auto;
        }}
        
        .carousel {{
            margin: 2rem 0;
        }}
        
        .carousel-control-prev,
        .carousel-control-next {{
            display: none;  /* Hide controls when they're not applicable */
        }}
        
        .carousel-item:not(:last-child) .carousel-control-next,
        .carousel-item:not(:first-child) .carousel-control-prev {{
            display: flex;  /* Show controls when applicable */
        }}
    </style>
</head>
<body>
    <div class="container py-4">
        {header}
        {searched_items}
        {content}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

    def add_statistics(self, venues, average_price_map, chp_venues=None):
        """Add statistics and store average prices for later use"""
        self.average_price_map = average_price_map  # Store the average prices
        
        num_venues = len(venues)
        total_prices = [venue.total_normalized_price(average_price_map) for venue in venues]
        min_price = min(total_prices) if total_prices else 0
        max_price = max(total_prices) if total_prices else 0

        chp_min_price = None
        if chp_venues:
            chp_prices = [venue.total_price() for venue in chp_venues]
            if chp_prices:
                chp_min_price = min(chp_prices)

        stats_html = f'''
        <div class="stats-section">
            <div class="stats-main mb-4">
                <p><span class="stats-number">{num_venues}</span> חנויות מוכרות את כל הפריטים החיוניים</p>
            </div>
            <div class="row text-center">
                <div class="col-md-4">
                    <p>מחיר מינימלי: <span class="stats-number">₪{min_price:.2f}</span></p>
                </div>
                <div class="col-md-4">
                    <p>מחיר מקסימלי: <span class="stats-number">₪{max_price:.2f}</span></p>
                </div>
                {f'<div class="col-md-4"><p>מחיר מינימלי באונליין: <span class="stats-number">₪{chp_min_price:.2f}</span></p></div>' if chp_min_price else ''}
            </div>
        </div>
        '''
        self.content.append(stats_html)

    def _get_sorted_items_html(self, venue, average_price_map):
        """Helper method to get items HTML in consistent order"""
        items_html = []
        
        # Create a map of searched name to item for quick lookup
        item_map = {item.searched_name: item for item in venue.items}
        
        # Generate HTML following the search list order
        for search_name, _ in self.items_to_search:
            if search_name in item_map:
                item = item_map[search_name]
                items_html.append(
                    f'<li><a href="{item.url}" class="text-decoration-none">{item.name}: ₪{item.price:.2f}</a></li>'
                )
        
        return "".join(items_html)

    def add_venue_card(self, venue, average_price_map, title=None, card_class=""):
        # Create HTML content for items in consistent order
        items_html = self._get_sorted_items_html(venue, average_price_map)
        
        # Create HTML content for missing items
        missing_items_html = ""
        if venue.missing_items:
            missing_items = []
            for item in venue.missing_items:
                avg_price = average_price_map.get(item.searched_name, 0)
                missing_items.append(f'<li>{item.name} (מחיר ממוצע - ₪{avg_price:.2f})</li>')
            
            missing_items_html = f'''
            <div class="missing-items mt-3">
                <h6>פריטים חסרים:</h6>
                <ul>{''.join(missing_items)}</ul>
            </div>
            '''

        # Build the complete venue card HTML with consistent price formatting
        venue_title = f"{title} - {venue.name}" if title else venue.name
        venue_html = f'''
        <div class="venue-card {card_class}">
            <h3>{venue_title}</h3>
            <a href="{venue.url}" class="text-decoration-none" target="_blank">קישור לחנות</a>
            <div class="price-tag mt-2">₪{venue.total_normalized_price(average_price_map):.2f}</div>
            <ul class="item-list mt-3">
                {items_html}
            </ul>
            {missing_items_html}
        </div>
        '''
        self.content.append(venue_html)

    def add_carousel(self, venues, average_price_map, id_prefix, title):
        if not venues:
            return

        carousel_items = []
        venues = sorted(venues, 
                      key=lambda v: v.total_normalized_price(average_price_map))
        
        for i, venue in enumerate(venues):
            # Create items HTML in consistent order
            items_html = self._get_sorted_items_html(venue, average_price_map)
            
            # Create missing items HTML
            missing_items_html = ""
            if venue.missing_items:
                missing_items = []
                for item in venue.missing_items:
                    avg_price = average_price_map.get(item.searched_name, 0)
                    missing_items.append(f'<li>{item.name} (מחיר ממוצע - ₪{avg_price:.2f})</li>')
                
                missing_items_html = f'''
                <div class="missing-items mt-3">
                    <h6>פריטים חסרים:</h6>
                    <ul>{''.join(missing_items)}</ul>
                </div>
                '''
            
            carousel_items.append(f'''
            <div class="carousel-item{' active' if i == 0 else ''}" data-bs-interval="false">
                <div class="venue-card">
                    <h3>{venue.name}</h3>
                    <a href="{venue.url}" class="text-decoration-none" target="_blank">קישור לחנות</a>
                    <div class="price-tag mt-2">₪{venue.total_normalized_price(average_price_map):.2f}</div>
                    <ul class="item-list mt-3">
                        {items_html}
                    </ul>
                    {missing_items_html}
                </div>
            </div>
            ''')

        carousel_html = f'''
        <div class="section-title mt-4">{title}</div>
        <div id="{id_prefix}Carousel" class="carousel slide" data-bs-ride="false" data-bs-touch="true" data-bs-interval="false">
            <div class="carousel-inner">
                {''.join(carousel_items)}
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#{id_prefix}Carousel" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous (Cheaper)</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#{id_prefix}Carousel" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next (More expensive)</span>
            </button>
            <div class="carousel-indicators">
                {' '.join([f'<button type="button" data-bs-target="#{id_prefix}Carousel" data-bs-slide-to="{i}"{" class=active aria-current=true" if i == 0 else ""} aria-label="Slide {i+1}"></button>' for i in range(len(venues))])}
            </div>
        </div>
        '''
        self.content.append(carousel_html)

    def add_chp_venues(self, chp_venues):
        if not chp_venues:
            return

        carousel_items = []
        # Sort by price ascending (cheapest first)
        sorted_venues = sorted(chp_venues, 
                             key=lambda v: v.total_price())
        
        for i, venue in enumerate(sorted_venues):
            items_html = "".join([
                f'<li><a href="{url}" class="text-decoration-none">{item_name}: ₪{price:.2f}</a></li>'
                for item_name, (price, url) in venue.items.items()
            ])
            
            # Create missing items HTML
            missing_items_html = ""
            if venue.missing_items:
                missing_items = []
                for item in venue.missing_items:
                    avg_price = average_price_map.get(item.searched_name, 0)
                    missing_items.append(f'<li>{item.name} (מחיר ממוצע - ₪{avg_price:.2f})</li>')
                
                missing_items_html = f'''
                <div class="missing-items mt-3">
                    <h6>פריטים חסרים:</h6>
                    <ul>{''.join(missing_items)}</ul>
                </div>
                '''
            
            carousel_items.append(f'''
            <div class="carousel-item{' active' if i == 0 else ''}" data-bs-interval="false">
                <div class="venue-card">
                    <h3>{venue.name}</h3>
                    <a href="{venue.website_url}" class="text-decoration-none" target="_blank">אתר החנות</a>
                    <div class="price-tag mt-2">₪{venue.total_price():.2f}</div>
                    <ul class="item-list mt-3">
                        {items_html}
                    </ul>
                    {missing_items_html}
                </div>
            </div>
            ''')

        online_stores_html = f'''
        <div class="online-stores">
            <h2 class="section-title">חנויות אונליין</h2>
            <div id="onlineStoresCarousel" class="carousel slide" data-bs-ride="false" data-bs-touch="true" data-bs-interval="false">
                <div class="carousel-inner">
                    {''.join(carousel_items)}
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#onlineStoresCarousel" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous (Cheaper)</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#onlineStoresCarousel" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next (More expensive)</span>
                </button>
                <div class="carousel-indicators">
                    {' '.join([f'<button type="button" data-bs-target="#onlineStoresCarousel" data-bs-slide-to="{i}"{" class=active aria-current=true" if i == 0 else ""} aria-label="Slide {i+1}"></button>' for i in range(len(sorted_venues))])}
                </div>
            </div>
        </div>
        '''
        self.content.append(online_stores_html)

    def save(self):
        formatted_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Create header section
        header_html = f'''
        <div class="main-header">
            <h1 class="main-title">דו"ח מחירים</h1>
            <div class="sub-title">{formatted_date}</div>
        </div>
        '''

        # Create searched items carousel
        searched_items_html = self._create_searched_items_carousel()
        
        # Combine current content with saved content
        self._saved_content.extend(self.content)
        
        try:
            final_html = self.html_template.format(
                date=formatted_date,
                header=header_html,
                searched_items=searched_items_html,
                content='\n'.join(str(item) for item in self._saved_content)
            )
            # Update carousel initialization script with better control handling
            final_html = final_html.replace('</body>',
                '''
                <script>
                document.addEventListener('DOMContentLoaded', function() {
                    var carousels = document.querySelectorAll('.carousel');
                    carousels.forEach(function(carousel) {
                        var carouselInstance = new bootstrap.Carousel(carousel, {
                            interval: false,
                            touch: true,
                            wrap: false
                        });
                        
                        var items = carousel.querySelectorAll('.carousel-item');
                        var prevBtn = carousel.querySelector('.carousel-control-prev');
                        var nextBtn = carousel.querySelector('.carousel-control-next');
                        
                        // Initial state
                        prevBtn.classList.add('disabled');
                        if (items.length <= 1) {
                            nextBtn.classList.add('disabled');
                        }
                        
                        carousel.addEventListener('slide.bs.carousel', function(event) {
                            var nextIndex = event.to;
                            
                            // Update prev button
                            if (nextIndex === 0) {
                                prevBtn.classList.add('disabled');
                            } else {
                                prevBtn.classList.remove('disabled');
                            }
                            
                            // Update next button
                            if (nextIndex === items.length - 1) {
                                nextBtn.classList.add('disabled');
                            } else {
                                nextBtn.classList.remove('disabled');
                            }
                        });
                    });
                });
                </script>
                </body>
                ''')
            self.content = []  # Clear current content after saving
        except KeyError as e:
            print(f"Error formatting template: {e}")
            raise

        # Ensure proper file extension and handle existing files
        base_name, extension = os.path.splitext(self.file_name)
        if not extension or extension != '.html':
            base_name = self.file_name
            extension = '.html'

        attempt = 1
        test_name = f"{base_name}{extension}"
        
        while os.path.exists(test_name):
            test_name = f"{base_name}({attempt}){extension}"
            attempt += 1
        
        self.file_name = test_name

        try:
            with open(self.file_name, 'w', encoding='utf-8') as f:
                f.write(final_html)
            print(f"HTML report saved as: {self.file_name}")
        except Exception as e:
            print(f"Error saving file: {e}")
            raise

    def _create_searched_items_carousel(self):
        if not hasattr(self, 'items_to_search'):
            return ''
            
        items_html = []
        for item, must_include in self.items_to_search:
            class_name = 'must-include' if must_include else 'optional'
            avg_price = self.average_price_map.get(item, 0)
            items_html.append(f'''
                <div class="tooltip search-item {class_name}">
                    {item}
                    <span class="tooltiptext">מחיר ממוצע - ₪{avg_price:.2f}</span>
                </div>
            ''')
        
        return f'''
        <div class="items-carousel">
            <div class="d-flex flex-wrap justify-content-center">
                {''.join(items_html)}
            </div>
        </div>
        '''

    def generate_report(self, file_name, chp_venues=None):
        # ...existing code...
        # Add cheapest venue as main card with special styling
        result_formatter.add_venue_card(
            sorted_venues[0], 
            self.average_price_map,
            "החנות הזולה ביותר",
            "cheapest-venue"
        )
        
        # Change most expensive venue styling
        if most_expensive_venue:
            result_formatter.add_venue_card(
                most_expensive_venue,
                self.average_price_map,
                "החנות היקרה ביותר",
                "most-expensive"
            )
        # ...existing code...
