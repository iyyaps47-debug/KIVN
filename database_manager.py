"""
database_manager.py - Chat History Database Management
Handles storing and retrieving chat messages using SQLite
"""

import sqlite3
import os
from datetime import datetime

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
            
            # Create index for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_email 
                ON chat_history(user_email)
            """)
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error initializing database: {e}")
    
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
            print(f"Error saving message: {e}")
            return False
    
    def get_user_history(self, user_email: str) -> list:
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
            print(f"Error retrieving history: {e}")
            return []
    
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
            print(f"Error deleting message: {e}")
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
            print(f"Error clearing history: {e}")
            return False


# Global database instance
_db_instance = None

def get_db():
    """Get database instance (singleton pattern)"""
    global _db_instance
    if _db_instance is None:
        _db_instance = ChatHistoryDB()
    return _db_instance
