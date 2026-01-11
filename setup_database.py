"""
Database Setup Script
Run this script to verify MySQL connection and initialize the database
Now automatically reads credentials from .env file!
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration - Automatically loaded from .env file
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'password'),
}

DATABASE_NAME = os.getenv('DB_NAME', 'ml_webapp_db')

def test_connection():
    """Test MySQL connection"""
    print("Testing MySQL connection...")
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✓ Successfully connected to MySQL Server version {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"✓ Current database: {record}")
            
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"✗ Error connecting to MySQL: {e}")
        print("\nPlease check:")
        print("1. MySQL Server is running")
        print("2. Your .env file is configured correctly")
        print("3. Run 'python setup_env.py' if you haven't set up .env yet")
        print("4. Username and password in .env are correct")
        print("5. MySQL is accessible on localhost:3306")
        return False

def create_database():
    """Create the application database"""
    print(f"\nCreating database '{DATABASE_NAME}'...")
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"✓ Database '{DATABASE_NAME}' created successfully")
        
        # Verify database exists
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if DATABASE_NAME in databases:
            print(f"✓ Database '{DATABASE_NAME}' verified")
        
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"✗ Error creating database: {e}")
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