"""
Database Manager
Handles SQLite operations for Job Tracker and Version Control
"""

import sqlite3
import os
from datetime import datetime
from config import Settings

class DBManager:
    def __init__(self):
        self.db_path = Settings.DB_PATH
        self._init_db()

    def _init_db(self):
        """Initialize DB with schema."""
        # Ensure dir exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Read schema
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                cursor.executescript(f.read())
        
        conn.commit()
        conn.close()

    def add_application(self, company, role, status, date, score, notes):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO job_applications (company, role, status, date_applied, ats_score, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (company, role, status, date, score, notes))
        conn.commit()
        conn.close()

    def get_applications(self):
        conn = sqlite3.connect(self.db_path)
        # return pandas compatible list
        import pandas as pd
        df = pd.read_sql_query("SELECT * FROM job_applications ORDER BY date_applied DESC", conn)
        conn.close()
        return df

    def update_status(self, app_id, new_status):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("UPDATE job_applications SET status = ? WHERE id = ?", (new_status, app_id))
        conn.commit()
        conn.close()
        
    def delete_application(self, app_id):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM job_applications WHERE id = ?", (app_id,))
        conn.commit()
        conn.close()

    def save_version(self, name, content, parent_id=None):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
            INSERT INTO resume_versions (version_name, content, created_at, parent_version_id)
            VALUES (?, ?, ?, ?)
        """, (name, content, created_at, parent_id))
        conn.commit()
        conn.close()

    def get_versions(self):
        conn = sqlite3.connect(self.db_path)
        import pandas as pd
        df = pd.read_sql_query("SELECT * FROM resume_versions ORDER BY created_at DESC", conn)
        conn.close()
        return df
        
    def delete_version(self, v_id):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM resume_versions WHERE id = ?", (v_id,))
        conn.commit()
        conn.close()

db_manager = DBManager()
