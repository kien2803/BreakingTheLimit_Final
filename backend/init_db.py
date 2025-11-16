"""
Script to initialize the database from schema.sql
"""
import sqlite3
import os
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def init_database():
    """Initialize database from schema.sql"""
    db_path = 'btl.db'
    
    # Remove existing database if exists
    if os.path.exists(db_path):
        print(f"[!] Existing database found at {db_path}")
        response = input("Do you want to recreate it? (y/n): ")
        if response.lower() != 'y':
            print("[X] Database initialization cancelled.")
            return
        os.remove(db_path)
        print(f"[*] Removed existing database")
    
    # Read schema file
    schema_path = os.path.join('database', 'schema.sql')
    if not os.path.exists(schema_path):
        print(f"[X] Schema file not found at {schema_path}")
        return
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Execute schema
        cursor.executescript(schema)
        conn.commit()
        print(f"[OK] Database initialized successfully at {db_path}")
        
        # Verify tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"[*] Created {len(tables)} tables:")
        for table in tables:
            print(f"    - {table[0]}")
        
        # Check users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"[*] Users in database: {user_count}")
        
        if user_count > 0:
            cursor.execute("SELECT id, name, email, role FROM users")
            users = cursor.fetchall()
            print("\n[*] User list:")
            for user in users:
                print(f"    ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Role: {user[3]}")
        
    except sqlite3.Error as e:
        print(f"[X] Error initializing database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("Initializing Breaking The Limits Database...")
    init_database()

