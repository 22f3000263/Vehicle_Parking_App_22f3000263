import sqlite3
import hashlib
from config import Config
from datetime import datetime

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with all required tables"""
    conn = get_db_connection()
    
    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT,
            user_type TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Parking lots table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS parking_lots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prime_location_name TEXT NOT NULL,
            address TEXT NOT NULL,
            pin_code TEXT NOT NULL,
            price_per_hour REAL NOT NULL,
            maximum_number_of_spots INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Parking spots table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS parking_spots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lot_id INTEGER NOT NULL,
            spot_number INTEGER NOT NULL,
            status TEXT DEFAULT 'A',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lot_id) REFERENCES parking_lots (id),
            UNIQUE(lot_id, spot_number)
        )
    ''')
    
    # Reservations table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spot_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            parking_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            leaving_timestamp TIMESTAMP,
            parking_cost REAL,
            status TEXT DEFAULT 'active',
            vehicle_number TEXT,
            FOREIGN KEY (spot_id) REFERENCES parking_spots (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_admin_user():
    """Create default admin user if not exists"""
    conn = get_db_connection()
    
    # Check if admin exists
    admin = conn.execute(
        'SELECT id FROM users WHERE username = ? AND user_type = ?',
        (Config.ADMIN_USERNAME, 'admin')
    ).fetchone()
    
    if not admin:
        password_hash = hashlib.sha256(Config.ADMIN_PASSWORD.encode()).hexdigest()
        conn.execute(
            '''INSERT INTO users (username, email, password_hash, full_name, user_type)
               VALUES (?, ?, ?, ?, ?)''',
            (Config.ADMIN_USERNAME, 'admin@parking.com', password_hash, 'System Administrator', 'admin')
        )
        conn.commit()
        print("Admin user created successfully!")
    
    conn.close()

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify password against hash"""
    return hashlib.sha256(password.encode()).hexdigest() == password_hash
