from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()  # make sure DATABASE_URL is in your .env file

engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    # Step 1: Check if column exists already
    check_result = conn.execute(text("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name='contact_groups' AND column_name='user_id';
    """)).fetchone()

    if check_result:
        print("🟡 'user_id' column already exists.")
    else:
        print("➕ Adding 'user_id' column...")
        conn.execute(text("ALTER TABLE contact_groups ADD COLUMN user_id INTEGER;"))
        print("✅ Added 'user_id' column.")

    # Step 2: Add Foreign Key Constraint
    try:
        print("🔗 Adding foreign key constraint...")
        conn.execute(text("""
            ALTER TABLE contact_groups
            ADD CONSTRAINT contact_groups_user_id_fkey
            FOREIGN KEY (user_id)
            REFERENCES "user"(id);
        """))
        print("✅ Foreign key constraint added.")
    except Exception as e:
        print("⚠️ Foreign key constraint failed (maybe already exists or column missing):")
        print(e)
