"""
Database Setup Script
Run this script to verify database connection and initialize the database
Works with both MySQL (local) and PostgreSQL (Render)
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Detect database type
DATABASE_URL = os.getenv('DATABASE_URL', '')  # Render PostgreSQL uses this
USE_POSTGRESQL = bool(DATABASE_URL)

if USE_POSTGRESQL:
    # Production: PostgreSQL (Render)
    import psycopg2
    from psycopg2 import Error
    print("🐘 Using PostgreSQL (Render)")
else:
    # Local: MySQL
    import mysql.connector
    from mysql.connector import Error
    print("🐬 Using MySQL (Local)")

# Database Configuration
if USE_POSTGRESQL:
    # Render PostgreSQL - uses DATABASE_URL
    DB_CONFIG = DATABASE_URL
    DB_TYPE = 'postgresql'
    DATABASE_NAME = 'PostgreSQL (from DATABASE_URL)'
else:
    # Local MySQL - uses individual parameters from .env
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'password'),
    }
    DATABASE_NAME = os.getenv('DB_NAME', 'ml_webapp_db')
    DB_TYPE = 'mysql'

def test_connection():
    """Test database connection"""
    print(f"Testing {DB_TYPE.upper()} connection...")
    try:
        if DB_TYPE == 'postgresql':
            # PostgreSQL connection
            connection = psycopg2.connect(DB_CONFIG)
            
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                print(f"✓ Successfully connected to PostgreSQL")
                print(f"✓ Version: {version[0][:50]}...")
                
                cursor.execute("SELECT current_database();")
                db_name = cursor.fetchone()[0]
                print(f"✓ Current database: {db_name}")
                
                cursor.close()
                connection.close()
                return True
        else:
            # MySQL connection
            connection = mysql.connector.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
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
        print(f"✗ Error connecting to {DB_TYPE.upper()}: {e}")
        print("\nPlease check:")
        print("1. Database server is running")
        print("2. Your .env file is configured correctly")
        print("3. Username and password in .env are correct")
        if DB_TYPE == 'mysql':
            print("4. MySQL is accessible on localhost:3306")
        return False

def create_database():
    """Create/verify the application database"""
    if DB_TYPE == 'postgresql':
        # PostgreSQL: Database is already created by Render
        print(f"\nVerifying PostgreSQL database connection...")
        try:
            connection = psycopg2.connect(DB_CONFIG)
            cursor = connection.cursor()
            
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"✓ Connected to database: {db_name}")
            
            # Show some database info
            cursor.execute("SELECT COUNT(*) FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
            table_count = cursor.fetchone()[0]
            print(f"✓ Number of tables: {table_count}")
            
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"✗ Error verifying PostgreSQL database: {e}")
            return False
    else:
        # MySQL: Create database if it doesn't exist
        print(f"\nCreating database '{DATABASE_NAME}' (if not exists)...")
        try:
            connection = mysql.connector.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
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
            print(f"✗ Error creating MySQL database: {e}")
            return False

def main():
    print("=" * 70)
    print("ML Web App - Database Setup")
    print("=" * 70)
    print()
    
    # Show configuration
    print("📋 Configuration:")
    print(f"   Database Type: {DB_TYPE.upper()}")
    
    if DB_TYPE == 'postgresql':
        print(f"   Connection: Using DATABASE_URL from environment")
        print(f"   Database: {DATABASE_NAME}")
    else:
        print(f"   Host: {DB_CONFIG['host']}")
        print(f"   Port: {DB_CONFIG['port']}")
        print(f"   User: {DB_CONFIG['user']}")
        print(f"   Database: {DATABASE_NAME}")
        print(f"   Password: {'*' * len(DB_CONFIG['password'])} (hidden)")
    print()
    
    # Test connection
    if not test_connection():
        print("\n" + "=" * 70)
        print("❌ Setup failed - Could not connect to database")
        print("=" * 70)
        
        if DB_TYPE == 'postgresql':
            print("\nFor Render PostgreSQL:")
            print("1. Make sure you created a PostgreSQL database in Render")
            print("2. Copy the Internal Database URL")
            print("3. Add it as DATABASE_URL environment variable")
        else:
            print("\nFor local MySQL:")
            print("1. Make sure MySQL is running")
            print("2. Check your .env file credentials")
            print("3. Run: python setup_env.py (to reconfigure)")
        
        return
    
    # Create/verify database
    if not create_database():
        print("\n" + "=" * 70)
        print("❌ Setup failed - Database creation/verification error")
        print("=" * 70)
        return
    
    # Success!
    print("\n" + "=" * 70)
    print("✅ Setup completed successfully!")
    print("=" * 70)
    print()
    print("Next steps:")
    
    if DB_TYPE == 'postgresql':
        print("1. Your PostgreSQL database on Render is ready!")
        print("2. Deploy your app to Render")
        print("3. Your app will connect automatically using DATABASE_URL")
    else:
        print("1. Your local MySQL database is configured and working!")
        print("2. Run: python app.py")
        print("3. Open browser to: http://localhost:5000")
    
    print()
    print("💡 Tip:")
    if DB_TYPE == 'postgresql':
        print("   The app automatically detects PostgreSQL when DATABASE_URL is set")
    else:
        print("   The app automatically uses MySQL when running locally")
    print("   Same code works in both environments! 🎉")

if __name__ == "__main__":
    main()