import re
import os
import sqlite3
import logging
from datetime import datetime

def remove_ansi_escape_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def parse_top_summary(lines, device_serial=None):
    data = {}
    if len(lines) < 4:
        logging.error("Insufficient top output lines.")
        return None

    try:
        # Line 1: Tasks
        task_matches = re.findall(r'(\d+)\s+(\w+)', lines[0])
        for value, label in task_matches:
            data[f'tasks_{label.lower()}'] = int(value)

        # Line 2: Memory
        mem_matches = re.findall(r'(\d+)K\s+(\w+)', lines[1])
        for value, label in mem_matches:
            data[f'mem_{label.lower()}'] = int(value)

        # Line 3: Swap
        swap_matches = re.findall(r'(\d+)K\s+(\w+)', lines[2])
        for value, label in swap_matches:
            data[f'swap_{label.lower()}'] = int(value)

        # Line 4: CPU
        cpu_matches = re.findall(r'(\d+)%(\w+)', lines[3])
        for value, label in cpu_matches:
            data[f'cpu_{label.lower()}'] = int(value)

        # Add timestamp
        data['timestamp'] = datetime.now()
        if device_serial:
            data['device_serial'] = device_serial

        return data
    except Exception as e:
        logging.error(f"Parsing failed: {e}")
        return None

# database functions
def initialize_database():
    """Create or open the SQLite database and initialize the required tables"""

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(root_dir, 'droic.db')

    logging.info(f"Database path: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS device_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        device_serial TEXT NOT NULL,
        model TEXT,
        connection_type TEXT,
        tasks_total INTEGER,
        tasks_running INTEGER,
        tasks_sleeping INTEGER,
        tasks_stopped INTEGER,
        tasks_zombie INTEGER,
        mem_total INTEGER,
        mem_used INTEGER,
        mem_free INTEGER,
        mem_buffers INTEGER,
        swap_total INTEGER,
        swap_used INTEGER,
        swap_free INTEGER,
        swap_cached INTEGER,
        cpu_cpu INTEGER,
        cpu_user INTEGER,
        cpu_nice INTEGER,
        cpu_sys INTEGER,
        cpu_idle INTEGER,
        cpu_iow INTEGER,
        cpu_irq INTEGER,
        cpu_sirq INTEGER,
        cpu_host INTEGER
    )
    ''')

    conn.commit()
    conn.close()
    logging.info("Database initialized successfully.")
    return db_path

def save_data_to_db(data_point):
    """Save a single data point to the SQLite database"""
    db_path = DATABASE_PATH

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        fields = {
            'timestamp': data_point['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            'device_serial': data_point.get('device_serial', 'unknown'),
            'model': data_point.get('model', 'Unknown'),
            'connection_type': data_point.get('connection_type', 'Unknown'),
            'tasks_total': data_point.get('tasks_total', 0),
            'tasks_running': data_point.get('tasks_running', 0),
            'tasks_sleeping': data_point.get('tasks_sleeping', 0),
            'tasks_stopped': data_point.get('tasks_stopped', 0),
            'tasks_zombie': data_point.get('tasks_zombie', 0),
            'mem_total': data_point.get('mem_total', 0),
            'mem_used': data_point.get('mem_used', 0),
            'mem_free': data_point.get('mem_free', 0),
            'mem_buffers': data_point.get('mem_buffers', 0),
            'swap_total': data_point.get('swap_total', 0),
            'swap_used': data_point.get('swap_used', 0),
            'swap_free': data_point.get('swap_free', 0),
            'swap_cached': data_point.get('swap_cached', 0),
            'cpu_cpu': data_point.get('cpu_cpu', 0),
            'cpu_user': data_point.get('cpu_user', 0),
            'cpu_nice': data_point.get('cpu_nice', 0),
            'cpu_sys': data_point.get('cpu_sys', 0),
            'cpu_idle': data_point.get('cpu_idle', 0),
            'cpu_iow': data_point.get('cpu_iow', 0),
            'cpu_irq': data_point.get('cpu_irq', 0),
            'cpu_sirq': data_point.get('cpu_sirq', 0),
            'cpu_host': data_point.get('cpu_host', 0)
        }

        columns = ', '.join(fields.keys())
        placeholders = ', '.join(['?'] * len(fields))
        values = tuple(fields.values())

        query = f"INSERT INTO device_metrics ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"[ERROR] Failed to save data to database: {e}")
        return False


if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    DATABASE_PATH = initialize_database()
else:
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'adb_monitor.db')
