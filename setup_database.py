"""
Database Setup Script
Run this script to verify MySQL connection and initialize the database
Now automatically reads credentials from .env file!
"""
import psycopg2
from psycopg2 import Error
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration - Automatically loaded from .env file
DATABASE_URL = os.getenv('DATABASE_URL', '')

if DATABASE_URL:
    DB_CONFIG = DATABASE_URL
else:
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'database': os.getenv('DB_NAME', 'ml_webapp_db')
    }

DATABASE_NAME = os.getenv('DB_NAME', 'ml_webapp_db')

def test_connection():
    """Test PostgreSQL connection"""
    print("Testing PostgreSQL connection...")
    try:
        if isinstance(DB_CONFIG, str):
            connection = psycopg2.connect(DB_CONFIG)
        else:
            connection = psycopg2.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG.get('database', 'postgres')
            )
        
        if connection:
            print(f"✓ Successfully connected to PostgreSQL Server")
            
            cursor = connection.cursor()
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print(f"✓ PostgreSQL version: {record[0]}")
            
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"✗ Error connecting to PostgreSQL: {e}")
        print("\nPlease check:")
        print("1. PostgreSQL Server is running")
        print("2. Your .env file is configured correctly")
        print("3. Username and password in .env are correct")
        return False

def create_database():
    """Verify database (PostgreSQL on Render creates it automatically)"""
    print(f"\nVerifying database connection...")
    try:
        if isinstance(DB_CONFIG, str):
            connection = psycopg2.connect(DB_CONFIG)
        else:
            connection = psycopg2.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG.get('database', 'postgres')
            )
        
        cursor = connection.cursor()
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]
        print(f"✓ Connected to database: {db_name}")
        
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"✗ Error verifying database: {e}")
        return False

def main():
    print("=" * 60)
    print("ML Web App - Database Setup")
    print("=" * 60)
    print()
    
    # Show that we're using .env
    print("📋 Loading configuration from .env file...")
    print(f"   Database Host: {DB_CONFIG['host']}")
    print(f"   Database User: {DB_CONFIG['user']}")
    print(f"   Database Name: {DATABASE_NAME}")
    print(f"   Password: {'*' * len(DB_CONFIG['password'])} (hidden)")
    print()
    
    # Test connection
    if not test_connection():
        return
    
    # Create database
    if not create_database():
        return
    
    print("\n" + "=" * 60)
    print("✓ Setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Your .env file is configured and working!")
    print("2. Run: python app.py")
    print("3. Open browser to: http://localhost:5000")
    print("\n💡 Tip: app.py uses the same .env credentials automatically")

if __name__ == "__main__":
    main()