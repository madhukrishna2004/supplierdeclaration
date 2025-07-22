import os
import psycopg2
import urllib.parse as urlparse
from dotenv import load_dotenv
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet

# === Load environment variables ===
load_dotenv()
db_url = os.getenv("DATABASE_URL")
parsed_url = urlparse.urlparse(db_url)
DB_CONFIG = {
    "dbname": parsed_url.path[1:],
    "user": parsed_url.username,
    "password": parsed_url.password,
    "host": parsed_url.hostname,
    "port": parsed_url.port
}

PDF_FILE = "postgres_full_report_landscape.pdf"
styles = getSampleStyleSheet()

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

def fetch(cursor, query):
    cursor.execute(query)
    return cursor.fetchall(), [desc[0] for desc in cursor.description]

def build_table(title, headers, rows):
    if not rows:
        return [Paragraph(f"<b>{title}</b>", styles['Heading3']),
                Paragraph("No data found.", styles['Normal']),
                Spacer(1, 12)]

    data = [headers] + rows
    table = Table(data, repeatRows=1, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#d1e0e0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#000000")),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
    ]))
    return [Paragraph(f"<b>{title}</b>", styles['Heading3']), table, Spacer(1, 12)]

def get_all_table_data(cursor, table_list, limit=100):
    all_data = []
    for (table_name,) in table_list:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        all_data += build_table(f"📦 Data from '{table_name}' (max {limit} rows)", headers, rows)
        all_data.append(PageBreak())
    return all_data

def generate_pdf():
    doc = SimpleDocTemplate(PDF_FILE, pagesize=landscape(A4), rightMargin=20, leftMargin=20)
    story = []

    story.append(Paragraph("📄 <b>PostgreSQL Full Schema & Data Report</b>", styles['Title']))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 20))

    conn = connect_db()
    cur = conn.cursor()

    queries = [
        ("📄 Tables", """
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """),
        ("📑 Columns", """
            SELECT table_name, column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """),
        ("🔐 Primary Keys", """
            SELECT tc.table_name, kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
            WHERE tc.constraint_type = 'PRIMARY KEY' AND tc.table_schema = 'public';
        """),
        ("🔗 Foreign Keys", """
            SELECT 
                tc.table_name AS source_table,
                kcu.column_name AS source_column,
                ccu.table_name AS target_table,
                ccu.column_name AS target_column
            FROM 
                information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY';
        """),
        ("📊 Table Row Counts", """
            SELECT relname AS table_name, n_live_tup AS row_count
            FROM pg_stat_user_tables
            ORDER BY n_live_tup DESC;
        """),
        ("🛠️ Indexes", """
            SELECT 
                t.relname AS table_name, 
                i.relname AS index_name, 
                a.attname AS column_name
            FROM 
                pg_class t, pg_class i, pg_index ix, pg_attribute a
            WHERE 
                t.oid = ix.indrelid
                AND i.oid = ix.indexrelid
                AND a.attrelid = t.oid
                AND a.attnum = ANY(ix.indkey)
            ORDER BY t.relname, i.relname;
        """),
        ("⏱️ Vacuum/Analyze Activity", """
            SELECT relname, last_vacuum, last_autovacuum, last_analyze, last_autoanalyze
            FROM pg_stat_all_tables
            WHERE schemaname = 'public';
        """)
    ]

    for title, query in queries:
        rows, headers = fetch(cur, query)
        story += build_table(title, headers, rows)

    table_list, _ = fetch(cur, """
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
    """)
    story += get_all_table_data(cur, table_list)

    cur.close()
    conn.close()

    doc.build(story)
    print(f"✅ PDF saved in landscape mode at: {PDF_FILE}")

if __name__ == "__main__":
    generate_pdf()
