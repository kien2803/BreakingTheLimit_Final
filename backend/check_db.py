"""
Script to check database and user data
"""
import sqlite3
import os
import sys
from datetime import datetime

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def check_database():
    """Check database status and user data"""
    db_path = 'btl.db'
    
    if not os.path.exists(db_path):
        print(f"[X] Database not found at {db_path}")
        print("[*] Run 'python init_db.py' to create the database")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"[*] Database: {db_path}")
        print(f"[*] Tables: {len(tables)}")
        for table in tables:
            print(f"    [OK] {table[0]}")
        
        # Check users
        print("\n[*] USERS TABLE:")
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"    Total users: {user_count}")
        
        if user_count > 0:
            cursor.execute("""
                SELECT id, name, email, role, created_at, last_login, is_active 
                FROM users 
                ORDER BY id
            """)
            users = cursor.fetchall()
            
            print("\n[*] User Details:")
            print("-" * 100)
            print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'Role':<10} {'Created':<20} {'Last Login':<20} {'Active'}")
            print("-" * 100)
            
            for user in users:
                user_id, name, email, role, created_at, last_login, is_active = user
                created = created_at[:10] if created_at else 'N/A'
                login = last_login[:19] if last_login else 'Never'
                active = 'Yes' if is_active else 'No'
                print(f"{user_id:<5} {name:<25} {email:<30} {role:<10} {created:<20} {login:<20} {active}")
        
        # Check journals
        print("\n[*] JOURNALS TABLE:")
        cursor.execute("SELECT COUNT(*) FROM journals")
        journal_count = cursor.fetchone()[0]
        print(f"    Total journals: {journal_count}")
        
        # Check family connections
        print("\n[*] FAMILY CONNECTIONS:")
        cursor.execute("SELECT COUNT(*) FROM family_connections")
        family_count = cursor.fetchone()[0]
        print(f"    Total connections: {family_count}")
        
        # Check daily messages
        print("\n[*] DAILY MESSAGES:")
        cursor.execute("SELECT COUNT(*) FROM daily_messages")
        message_count = cursor.fetchone()[0]
        print(f"    Total messages: {message_count}")
        
    except sqlite3.Error as e:
        print(f"[X] Error checking database: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    check_database()

