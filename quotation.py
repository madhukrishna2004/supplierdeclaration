from fpdf import FPDF
import unicodedata

def ascii_safe(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, ascii_safe("UI/UX Design Quotation - TradeSphere Global"), ln=True, align="C")
        self.ln(10)

    def section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 10, ascii_safe(title), ln=True, fill=True)
        self.ln(2)

    def section_body(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, ascii_safe(text))
        self.ln()

pdf = PDF()
pdf.add_page()

pdf.section_title("Scope of Work (11 Screens Total)")
pdf.section_body("""1. Landing Page - Hero, features, CTA, contact, testimonials
2. Main Dashboard - Sidebar, top nav, HS code search, tables, filters
3. HS Code Lookup - Search view with code details + import/export duties
4. Tariff Comparison - Side-by-side country tariff comparison UI
5. Request Demo Page - Clean form, trust elements, image/banner section
6. Chatbot UI - Chat popup layout, minimized/maximized views
7. Trade Agreement Details - Tabular layout with origin rules, duties, etc.
8. User Profile / Settings - Editable user details, password, etc.
9. VAT & Duty Calculator - Interactive form page with breakdown of results
10. Notifications & Updates - Alert/notification center with filters
11. About/Company Page - Info about RKLS, KrisLynx, vision, team section""")

pdf.section_title("Quotation: Mid-Level UI/UX Freelancer")
pdf.set_font("Arial", "B", 11)
pdf.set_fill_color(240, 240, 240)
pdf.cell(60, 8, "Component", 1, 0, "C", True)
pdf.cell(30, 8, "Screens", 1, 0, "C", True)
pdf.cell(40, 8, "Rate per Screen", 1, 0, "C", True)
pdf.cell(40, 8, "Subtotal (INR)", 1, 1, "C", True)

pdf.set_font("Arial", "", 11)
data = [
    ("Landing Page", "1", "Rs 7,500", "Rs 7,500"),
    ("Dashboard UI", "1", "Rs 9,000", "Rs 9,000"),
    ("Inner Pages (x9)", "9", "Rs 6,500", "Rs 58,500"),
    ("", "", "", "------------------"),
    ("Total", "", "", "Rs 75,000")
]
for row in data:
    pdf.cell(60, 8, ascii_safe(row[0]), 1)
    pdf.cell(30, 8, row[1], 1, 0, "C")
    pdf.cell(40, 8, row[2], 1, 0, "C")
    pdf.cell(40, 8, row[3], 1, 1, "C")

pdf.section_title("Deliverables")
pdf.section_body("""* Figma design file with components and assets
* Responsive-ready layout (desktop-first)
* 1-2 rounds of revision
* Color palette, typography system, spacing rules
* Optional: Exported assets (SVG, PNG, button states)""")

pdf.section_title("Timeline")
pdf.section_body("* 7-10 working days for initial delivery\n* 2-3 days for revisions")

pdf.section_title("Optional Add-Ons")
pdf.section_body("""* Full mobile responsive screens - Rs 15,000
* Animated prototypes in Figma - Rs 5,000
* Design system library - Rs 8,000""")

pdf.output("TradeSphere_UIUX_Quotation.pdf")
print("PDF generated successfully!")
