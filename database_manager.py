"""
database_manager.py - Chat History Database Management with ADMIN FEATURE
Handles storing and retrieving chat messages using SQLite
Includes admin authentication
"""

import sqlite3
import os
from datetime import datetime
import hashlib

class ChatHistoryDB:
    def __init__(self, db_path: str = "chat_history.db"):
        """Initialize SQLite database connection"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create database tables if they don't exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create chat history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_email TEXT NOT NULL,
                    user_name TEXT NOT NULL,
                    user_message TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    course TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create admin users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admin_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id TEXT UNIQUE NOT NULL,
                    admin_password TEXT NOT NULL,
                    admin_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_email 
                ON chat_history(user_email)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_admin_id 
                ON admin_users(admin_id)
            """)
            
            conn.commit()
            conn.close()
            print("✅ Database initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
    
    def hash_password(self, password: str) -> str:
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_admin(self, admin_id: str, password: str, admin_name: str) -> bool:
        """Create a new admin user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            hashed_password = self.hash_password(password)
            
            cursor.execute("""
                INSERT INTO admin_users 
                (admin_id, admin_password, admin_name)
                VALUES (?, ?, ?)
            """, (admin_id, hashed_password, admin_name))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error creating admin: {e}")
            return False
    
    def verify_admin(self, admin_id: str, password: str) -> bool:
        """Verify admin credentials"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            hashed_password = self.hash_password(password)
            
            cursor.execute("""
                SELECT id FROM admin_users 
                WHERE admin_id = ? AND admin_password = ?
            """, (admin_id, hashed_password))
            
            result = cursor.fetchone()
            conn.close()
            
            return result is not None
        except Exception as e:
            print(f"❌ Error verifying admin: {e}")
            return False
    
    def get_admin_name(self, admin_id: str) -> str:
        """Get admin name"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT admin_name FROM admin_users 
                WHERE admin_id = ?
            """, (admin_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
        except Exception as e:
            print(f"❌ Error getting admin name: {e}")
            return None
    
    def save_message(self, user_email: str, user_name: str, 
                     user_message: str, ai_response: str, course: str) -> bool:
        """Save a chat message to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO chat_history 
                (user_email, user_name, user_message, ai_response, course, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_email, user_name, user_message, ai_response, course, 
                  datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error saving message: {e}")
            return False
    
    def get_user_chat_history(self, user_email: str) -> list:
        """Get all chat messages for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, user_email, user_name, user_message, ai_response, 
                       course, created_at
                FROM chat_history
                WHERE user_email = ?
                ORDER BY created_at ASC
            """, (user_email,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ Error retrieving history: {e}")
            return []
    
    def get_all_users(self) -> list:
        """Get all unique users (ADMIN ONLY)"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT user_email, user_name, course, 
                       COUNT(*) as total_messages,
                       MAX(created_at) as last_chat
                FROM chat_history
                GROUP BY user_email
                ORDER BY last_chat DESC
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ Error getting all users: {e}")
            return []
    
    def get_total_chats(self) -> int:
        """Get total number of chats (ADMIN ONLY)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM chat_history")
            result = cursor.fetchone()[0]
            conn.close()
            
            return result
        except Exception as e:
            print(f"❌ Error getting total chats: {e}")
            return 0
    
    def get_total_users(self) -> int:
        """Get total unique users (ADMIN ONLY)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(DISTINCT user_email) FROM chat_history")
            result = cursor.fetchone()[0]
            conn.close()
            
            return result
        except Exception as e:
            print(f"❌ Error getting total users: {e}")
            return 0
    
    def delete_message(self, message_id: int) -> bool:
        """Delete a specific message"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chat_history WHERE id = ?", (message_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error deleting message: {e}")
            return False
    
    def clear_user_history(self, user_email: str) -> bool:
        """Delete all messages for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chat_history WHERE user_email = ?", (user_email,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error clearing history: {e}")
            return False


# Global database instance
_db_instance = None

def get_db():
    """Get database instance (singleton pattern)"""
    global _db_instance
    if _db_instance is None:
        _db_instance = ChatHistoryDB()
    return _db_instance
