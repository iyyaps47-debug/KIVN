"""
setup_admin.py - Create Admin Account
Run this ONCE to create your admin account
Then delete or keep this file
"""

import sqlite3
import hashlib

def hash_password(password: str) -> str:
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_admin_account():
    """Create initial admin account"""
    
    print("=" * 50)
    print("🔐 ADMIN ACCOUNT SETUP")
    print("=" * 50)
    print("\nThis will create your admin account")
    print("You'll use these credentials to view all users' chat history\n")
    
    # Get admin details
    admin_id = input("Enter Admin ID (e.g., admin@learnmate.com): ").strip()
    admin_name = input("Enter Admin Name (e.g., Admin User): ").strip()
    admin_password = input("Enter Admin Password (min 8 characters): ").strip()
    confirm_password = input("Confirm Admin Password: ").strip()
    
    # Validation
    if not admin_id or not admin_name or not admin_password:
        print("\n❌ All fields are required!")
        return
    
    if len(admin_password) < 8:
        print("\n❌ Password must be at least 8 characters!")
        return
    
    if admin_password != confirm_password:
        print("\n❌ Passwords do not match!")
        return
    
    # Create admin account
    try:
        conn = sqlite3.connect("chat_history.db")
        cursor = conn.cursor()
        
        hashed_password = hash_password(admin_password)
        
        cursor.execute("""
            INSERT INTO admin_users 
            (admin_id, admin_password, admin_name)
            VALUES (?, ?, ?)
        """, (admin_id, hashed_password, admin_name))
        
        conn.commit()
        conn.close()
        
        print("\n" + "=" * 50)
        print("✅ ADMIN ACCOUNT CREATED SUCCESSFULLY!")
        print("=" * 50)
        print(f"\n📧 Admin ID: {admin_id}")
        print(f"👤 Admin Name: {admin_name}")
        print("\n✅ You can now:")
        print("1. Open the app")
        print("2. Go to Chat History page")
        print("3. Enter Admin ID and Password")
        print("4. View ALL users' chat history")
        print("\n⚠️ Keep your admin credentials secure!")
        print("=" * 50)
        
    except sqlite3.IntegrityError:
        print(f"\n❌ Admin ID '{admin_id}' already exists!")
        print("Use a different Admin ID")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    create_admin_account()
