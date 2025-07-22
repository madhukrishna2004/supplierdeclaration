# db.py
import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_db_connection():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(query, values=None):
    """Execute an SQL query with optional parameters."""
    connection = get_db_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(f"Error executing query: {e}")
        return False
    finally:
        connection.close()

def fetch_one(query, values=None):
    """Fetch a single record from the database."""
    connection = get_db_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, values)
        return cursor.fetchone()
    except Error as e:
        print(f"Error fetching data: {e}")
        return None
    finally:
        connection.close()