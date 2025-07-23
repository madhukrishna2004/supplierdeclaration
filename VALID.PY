import psycopg2
import os

# Load DATABASE_URL from env
DATABASE_URL = os.getenv('DATABASE_URL')

def fetch_tables_and_columns():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Step 1: Get all user-defined table names
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public' AND table_type='BASE TABLE';
        """)
        tables = cursor.fetchall()

        all_table_columns = {}

        # Step 2: For each table, get column names and data types
        for table in tables:
            table_name = table[0]
            cursor.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = %s
            """, (table_name,))
            columns = cursor.fetchall()
            all_table_columns[table_name] = columns

        return all_table_columns

    except Exception as e:
        print(f"❌ Error: {e}")
        return {}

    finally:
        cursor.close()
        conn.close()

# Example usage
tables_info = fetch_tables_and_columns()
for table, columns in tables_info.items():
    print(f"\n🗂 Table: {table}")
    for col in columns:
        print(f" - {col[0]} ({col[1]})")
