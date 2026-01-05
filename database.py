import sqlite3
from datetime import datetime, date
import hashlib

def init_db():
    """Khởi tạo database"""
    conn = sqlite3.connect('meditation.db')
    c = conn.cursor()
    
    # Bảng users
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  created_date DATE DEFAULT CURRENT_DATE)''')
    
    # Bảng meditation sessions
    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER NOT NULL,
                  session_date DATE NOT NULL,
                  total_cycles INTEGER,
                  duration_minutes INTEGER,
                  breathing_type TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Mã hóa password"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Đăng ký user mới"""
    conn = sqlite3.connect('meditation.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                 (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    """Đăng nhập"""
    conn = sqlite3.connect('meditation.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=? AND password=?",
             (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def save_session(user_id, cycles, duration, breathing_type):
    """Lưu session thiền"""
    conn = sqlite3.connect('meditation.db')
    c = conn.cursor()
    c.execute("""INSERT INTO sessions 
                 (user_id, session_date, total_cycles, duration_minutes, breathing_type)
                 VALUES (?, DATE('now'), ?, ?, ?)""",
             (user_id, cycles, duration, breathing_type))
    conn.commit()
    conn.close()

def calculate_streak(user_id):
    """Tính streak (chuỗi ngày liên tiếp thiền)"""
    conn = sqlite3.connect('meditation.db')
    c = conn.cursor()
    
    # Lấy các ngày unique đã thiền
    c.execute("""SELECT DISTINCT session_date 
                 FROM sessions 
                 WHERE user_id=? 
                 ORDER BY session_date DESC""", (user_id,))
    
    dates = [row[0] for row in c.fetchall()]
    conn.close()
    
    if not dates:
        return 0
    
    # Tính streak từ hôm nay trở về trước
    streak = 0
    from datetime import timedelta
    current_date = date.today()
    
    for d in dates:
        check_date = datetime.strptime(d, '%Y-%m-%d').date()
        if check_date == current_date - timedelta(days=streak):
            streak += 1
        else:
            break
    
    return streak

def get_total_days(user_id):
    """Tổng số ngày đã thiền"""
    conn = sqlite3.connect('meditation.db')
    c = conn.cursor()
    c.execute("""SELECT COUNT(DISTINCT session_date) 
                 FROM sessions 
                 WHERE user_id=?""", (user_id,))
    result = c.fetchone()[0]
    conn.close()
    return result

def get_user_stats(user_id):
    """Lấy thống kê user"""
    conn = sqlite3.connect('meditation.db')
    c = conn.cursor()
    c.execute("""SELECT 
                    COUNT(*) as total_sessions,
                    SUM(total_cycles) as total_cycles,
                    SUM(duration_minutes) as total_minutes
                 FROM sessions 
                 WHERE user_id=?""", (user_id,))
    stats = c.fetchone()
    conn.close()
    return {
        'total_sessions': stats[0] or 0,
        'total_cycles': stats[1] or 0,
        'total_minutes': stats[2] or 0
    }
