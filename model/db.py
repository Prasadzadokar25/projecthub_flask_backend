"""
Centralized database connection module.

All model files should import get_db_connection() or get_db_cursor()
instead of creating connections directly in each file.
"""
import pymysql
from pymysql.cursors import DictCursor
import os


def get_db_config():
    """Get database configuration from environment or defaults.
    
    Returns a dictionary with host, user, password, database keys.
    Can be overridden via environment variables:
      - DB_HOST
      - DB_USER
      - DB_PASSWORD
      - DB_NAME
    """
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', '##Prasad25'),
        'database': os.getenv('DB_NAME', 'projecthubdb'),
    }


def get_db_connection():
    """Create and return a new database connection.
    
    Returns a pymysql connection object with DictCursor and autocommit enabled.
    Raises pymysql.MySQLError if connection fails.
    
    """
    config = get_db_config()
    try:
        con = pymysql.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            cursorclass=DictCursor
        )
        con.autocommit = True
        print(f"✓ Connected to {config['database']} successfully")
        return con
    except pymysql.MySQLError as err:
        print(f"✗ Failed to connect to database: {err}")
        raise


def get_db_cursor(connection=None):
    """Get a cursor from an existing connection or create a new one.
    
    Args:
        connection: optional existing pymysql connection. If None, creates a new one.
    
    Returns:
        A pymysql cursor object (DictCursor by default).
    """
    if connection is None:
        connection = get_db_connection()
    return connection.cursor()


def close_db_connection(connection):
    """Safely close a database connection.
    
    Args:
        connection: pymysql connection object to close.
    """
    if connection:
        try:
            connection.close()
            print("✓ Database connection closed")
        except Exception as e:
            print(f"⚠ Error closing connection: {e}")
