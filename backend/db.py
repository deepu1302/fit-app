"""
Database module for FitLife Tracker
Using SQLite (no setup required!)
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'fitlife.db')

def get_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            age INTEGER,
            height INTEGER,
            weight REAL,
            goal TEXT,
            diet_type TEXT,
            health_conditions TEXT,
            allergies TEXT,
            period TEXT,
            badge_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create weight_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weight_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            weight REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Create badges table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            badge_name TEXT,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def execute_query(query, params=None, fetch=False):
    """Execute a query and optionally fetch results"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            conn.close()
            return result
        
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.close()
        return None

def execute_single(query, params=None):
    """Execute a query and fetch single row"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.close()
        return None

if __name__ == "__main__":
    # Initialize database
    if not os.path.exists(DB_PATH):
        init_database()
    else:
        print(f"Database already exists at: {DB_PATH}")
    
    # Test connection
    conn = get_connection()
    if conn:
        print("Connected to SQLite successfully!")
        conn.close()
    else:
        print("Failed to connect to SQLite")
