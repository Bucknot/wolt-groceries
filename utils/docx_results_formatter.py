from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, RGBColor
import os

class DocxResultFormatter:
    def __init__(self, file_name):
        self.document = Document()
        self.file_name = file_name

    def add_heading(self, text, level=1):
        heading = self.document.add_heading(text, level=level)
        heading.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for run in heading.runs:
            run.font.rtl = True

    def add_paragraph(self, text, font_size=11, color=RGBColor(0, 0, 0)):
        paragraph = self.document.add_paragraph(text)
        paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for run in paragraph.runs:
            run.font.rtl = True
            run.font.size = font_size
            run.font.color.rgb = color

    def add_hyperlink(self, paragraph, url, text):
        part = paragraph.part
        r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
        hyperlink = OxmlElement('w:hyperlink')
        hyperlink.set(qn('r:id'), r_id)
        new_run = OxmlElement('w:r')
        rPr = OxmlElement('w:rPr')
        new_run.append(rPr)
        new_run.text = text
        hyperlink.append(new_run)
        paragraph._p.append(hyperlink)
        paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for run in paragraph.runs:
            run.font.rtl = True

    def add_venue(self, venue, average_price_map):
        self.add_heading(f"חנות - {venue.name} - מחיר כולל: ₪{venue.total_normalized_price(average_price_map)} ", level=2)
        paragraph = self.document.add_paragraph()
        self.add_hyperlink(paragraph, venue.url, venue.url)
        paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for run in paragraph.runs:
            run.font.rtl = True
        self.add_heading("פריטים:", level=3)
        for item in venue.items:
            self.add_bullet_point(f"{item.name}: ₪{item.price}", url=item.url)
        if venue.missing_items:
            self.add_heading("פריטים חסרים:", level=3)
            for missing_item in venue.missing_items:
                self.add_bullet_point(f"{missing_item.name}. (מחיר ממוצע - ₪{average_price_map[missing_item.searched_name]})", font_size=10, color=RGBColor(128, 128, 128))

    def add_secondary_venue(self, venue, average_price_map, rank):
        self.add_heading(f"חנות {rank} - {venue.name} - מחיר כולל: ₪{venue.total_normalized_price(average_price_map)} ", level=3)
        paragraph = self.document.add_paragraph()
        self.add_hyperlink(paragraph, venue.url, venue.url)
        paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for run in paragraph.runs:
            run.font.rtl = True
        self.add_heading("פריטים:", level=4)
        for item in venue.items:
            self.add_bullet_point(f"{item.name}: ₪{item.price}", font_size=10, color=RGBColor(128, 128, 128), url=item.url)
        if venue.missing_items:
            self.add_heading("פריטים חסרים:", level=4)
            for missing_item in venue.missing_items:
                self.add_bullet_point(f"{missing_item.name}. (מחיר ממוצע - ₪{average_price_map[missing_item.searched_name]})", font_size=10, color=RGBColor(128, 128, 128))

    def add_bullet_point(self, text, font_size=12, color=RGBColor(0, 0, 0), url=None):
        paragraph = self.document.add_paragraph(style='ListBullet')
        paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run = paragraph.add_run()
        if url:
            self.add_hyperlink(paragraph, url, text)
        else:
            run.text = text
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
        run.font.rtl = True
        run.font.name = 'Arial'

    def add_most_expensive_venue(self, venue, average_price_map):
        self.add_heading("הסל היקר ביותר", level=1)
        self.add_venue(venue, average_price_map)

    def add_statistics(self, venues, average_price_map):
        num_venues = len(venues)
        total_prices = [venue.total_normalized_price(average_price_map) for venue in venues]
        avg_price = round(sum(total_prices) / num_venues, 2) if num_venues > 0 else 0
        min_price = min(total_prices) if total_prices else 0
        max_price = max(total_prices) if total_prices else 0

        self.add_heading(f"מספר חנויות שמצאו את כל הפריטים החיוניים: {num_venues}", level=1)
        self.add_paragraph(f"מחיר ממוצע: ₪{avg_price}   |   מחיר מינימלי: ₪{min_price}  |   מחיר מקסימלי: ₪{max_price}", font_size=9)

    def save(self):
        base_name, extension = os.path.splitext(self.file_name)
        attempt = 1
        while True:
            if os.path.exists(self.file_name):
                attempt += 1
                self.file_name = f"{base_name}({attempt}){extension}"
                continue
            try:
                self.document.save(self.file_name)
                break
            except PermissionError:
                attempt += 1
                self.file_name = f"{base_name}({attempt}){extension}"