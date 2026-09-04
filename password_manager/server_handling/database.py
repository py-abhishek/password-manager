import sqlite3
import logging
import os

class Database:
    def __init__(self):
        self.db_file = "passwords.db"
        self.create_table()

    def close(self):
        if self.conn:
            self.conn.close()

    # General Query Executor
    def execute_query(self, query, data=None, fetch=False):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()

                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)

                conn.commit()

                if fetch:
                    return cursor.fetchall()
                return True
        except sqlite3.Error as e:
            logging.exception(f"Database Error: {e}")
            return False

    def create_table(self):
        print("DB Path:", os.path.abspath(self.db_file))
        query = """
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        return self.execute_query(query)

    def add_password(self, platform, username, password):
        print(f"User Input = {platform, username, password}")
        query = """
            INSERT INTO passwords(platform, username, password)
            VALUES(?,?,?)
            """
        success = self.execute_query(query, (platform, username, password))
        print(success)
        return success

    def search_password(self, search_term):
        query = """
            SELECT id, platform, username, password FROM passwords
            WHERE platform LIKE ? OR username LIKE ?
            """
        return self.execute_query(query,(f"%{search_term}%", f"%{search_term}%"), fetch=True)

    def update_password(self, id, platform, username, password):
        query = """
            UPDATE passwords
            SET platform = ?, username = ?, password = ?
            WHERE id = ?
            """
        return self.execute_query(query,(platform, username, password, id))

    def delete_password(self, id):
        query = """
            DELETE FROM passwords 
            WHERE id = ?
            """
        return self.execute_query(query, (id,))
        
    def get_all(self):
        query = """
            SELECT * FROM passwords
            """
        return self.execute_query(query, fetch=True)
        

if __name__ == "__main__":
    print(Database().getAll())
