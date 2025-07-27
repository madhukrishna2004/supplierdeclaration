import os
import psycopg2

# ✅ Get the PostgreSQL connection string from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in environment!")

# ✅ Connect and alter the table
def alter_table_constraints():
    conn = None
    try:
        # Connect using the DATABASE_URL
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Alter table to drop NOT NULL constraints if columns exist
        alter_query = """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='email_logs' AND column_name='sheet_link'
            ) THEN
                EXECUTE 'ALTER TABLE email_logs ALTER COLUMN sheet_link DROP NOT NULL';
            END IF;

            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='email_logs' AND column_name='username'
            ) THEN
                EXECUTE 'ALTER TABLE email_logs ALTER COLUMN username DROP NOT NULL';
            END IF;

            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='email_logs' AND column_name='password'
            ) THEN
                EXECUTE 'ALTER TABLE email_logs ALTER COLUMN password DROP NOT NULL';
            END IF;

            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='email_logs' AND column_name='created_at'
            ) THEN
                EXECUTE 'ALTER TABLE email_logs ALTER COLUMN created_at DROP NOT NULL';
            END IF;

            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='email_logs' AND column_name='sent_time'
            ) THEN
                EXECUTE 'ALTER TABLE email_logs ALTER COLUMN sent_time DROP NOT NULL';
            END IF;
        END;
        $$;
        """
        cur.execute(alter_query)
        conn.commit()
        print("✅ NOT NULL constraints dropped where applicable.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    alter_table_constraints()
