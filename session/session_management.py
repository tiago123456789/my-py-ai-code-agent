

import sqlite3
import datetime

class Session:
    
    def __init__(self, old_session_id):
        self.conn = sqlite3.connect("./db.db")
        self.cursor = self.conn.cursor()
        if old_session_id == None:
            self.__setup()
            self.session_id = self.__startNewOne()
        else:
            self.session_id = old_session_id
       
    def __setup(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                created_at TIMESTAMP
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                session_id INTEGER,
                role TEXT,
                message TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            );
        ''')
        self.conn.commit()
        
    def __startNewOne(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO sessions (created_at) VALUES (?)", (f'{current_time}',))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_session_id(self):
        return self.session_id
    
    def get_back_messages_history(self):
        self.cursor.execute("SELECT id, role, message, * FROM messages WHERE session_id = ? ORDER BY created_at asc", (self.session_id,))
        rows = self.cursor.fetchall()
    
        messages: list[dict] = []
        for row in rows:
            if row[2] == None:
                continue;
            item = {
                "role": row[1],
                "message": row[2]
            }
            messages.append(item)
            
        return messages
            
    def save(self, role, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("INSERT INTO messages (role, message, session_id, created_at) VALUES (?, ?, ?, ?)", (
            role, message, self.session_id, f'{current_time}',)
        )
        
        self.conn.commit()
        
    def close(self):
        self.conn.close()
        