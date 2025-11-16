"""
Script to check if backend setup is correct
"""
import sys
import os

print("=" * 60)
print("Breaking The Limits - Backend Setup Check")
print("=" * 60)

# Check Python version
print(f"\n[1] Python Version: {sys.version}")
print(f"    Python Path: {sys.executable}")

# Check if we're in backend directory
current_dir = os.getcwd()
print(f"\n[2] Current Directory: {current_dir}")
if not current_dir.endswith('backend'):
    print("    [WARNING] Not in backend directory!")
    print("    Please run: cd backend")

# Check required modules
print("\n[3] Checking Required Modules:")
required_modules = [
    'flask',
    'flask_cors',
    'flask_sqlalchemy',
    'bcrypt',
    'werkzeug',
    'dotenv',
    'requests'
]

missing_modules = []
for module in required_modules:
    try:
        __import__(module)
        print(f"    [OK] {module}")
    except ImportError:
        print(f"    [X] {module} - MISSING")
        missing_modules.append(module)

if missing_modules:
    print(f"\n[!] Missing modules: {', '.join(missing_modules)}")
    print("\nTo install, run:")
    print("    pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests")
    print("\nOr:")
    print("    pip install -r requirements.txt")
else:
    print("\n[OK] All required modules are installed!")

# Check database
print("\n[4] Checking Database:")
db_path = os.path.join('btl.db')
if os.path.exists(db_path):
    print(f"    [OK] Database found: {db_path}")
    import sqlite3
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"    [OK] Users in database: {user_count}")
        conn.close()
    except Exception as e:
        print(f"    [X] Database error: {e}")
else:
    print(f"    [X] Database not found: {db_path}")
    print("    Run: python init_db.py")

# Check config
print("\n[5] Checking Configuration:")
config_path = os.path.join('config.py')
if os.path.exists(config_path):
    print("    [OK] config.py found")
else:
    print("    [X] config.py not found")

# Summary
print("\n" + "=" * 60)
if not missing_modules and os.path.exists(db_path):
    print("[OK] Setup looks good! You can run: python app.py")
else:
    print("[X] Setup incomplete. Please fix the issues above.")
print("=" * 60)

