from fpdf import FPDF

# Creating a PDF document
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

# Title
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, "Cloud SQL Services Cost Comparison", ln=True, align="C")
pdf.ln(10)

# Table Header
pdf.set_font("Arial", 'B', 12)
pdf.set_fill_color(220, 220, 220)  # Light gray background for header
pdf.cell(40, 10, 'Cloud Provider', border=1, fill=True, align='C')
pdf.cell(50, 10, 'Service Name', border=1, fill=True, align='C')
pdf.cell(40, 10, 'Cost Estimate (Per Month)', border=1, fill=True, align='C')
pdf.cell(60, 10, 'Additional Notes', border=1, fill=True, align='C')
pdf.ln()

# Table Data
data = [
    ("Google Cloud SQL", "MySQL (db-n1-standard-1)", "$30.60", "Includes 1 vCPU, 3.75 GB RAM, 30 GB SSD"),
    ("Amazon RDS", "MySQL db.t3.micro", "$15.00", "Includes 1 vCPU, 1 GB RAM, 20 GB SSD"),
    ("Microsoft Azure SQL Database", "Basic tier", "$5.00", "Includes 1 DTU, 2 GB storage"),
    ("IBM Cloud Databases for MySQL", "Lite plan", "$0", "Includes 1 GB storage (free plan)"),
    ("Oracle Cloud MySQL", "MySQL DB System", "$35.00", "Includes 1 OCPU, 6 GB RAM, 100 GB storage"),
]

pdf.set_font("Arial", size=12)
for row in data:
    pdf.cell(40, 10, row[0], border=1, align='C')
    pdf.cell(50, 10, row[1], border=1, align='C')
    pdf.cell(40, 10, row[2], border=1, align='C')
    pdf.cell(60, 10, row[3], border=1, align='C')
    pdf.ln()

# Save the PDF
output_path = "mysql_cloud_comparison_formatted.pdf"
pdf.output(output_path)

output_path
