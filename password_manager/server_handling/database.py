import sqlite3
import logging
import os

class Database:
    def __init__(self):
        self.db_file = "passwords.db"
        self.createTable()

    def close(self):
        if self.conn:
            self.conn.close()

    # General Query Executor
    def executeQuery(self, query, data=None, fetch=False):
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

    def createTable(self):
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
        return self.executeQuery(query)

    def addPassword(self, platform, username, password):
        print(f"User Input = {platform, username, password}")
        query = """
            INSERT INTO passwords(platform, username, password)
            VALUES(?,?,?)
            """
        success = self.executeQuery(query, (platform, username, password))
        print(success)
        return success

    def searchPassword(self, search_term):
        query = """
            SELECT id, platform, username, password FROM passwords
            WHERE platform LIKE ? OR username LIKE ?
            """
        return self.executeQuery(query,(f"%{search_term}%", f"%{search_term}%"), fetch=True)

    def updatePassword(self, id, platform, username, password):
        query = """
            UPDATE passwords
            SET platform = ?, username = ?, password = ?
            WHERE id = ?
            """
        return self.executeQuery(query,(platform, username, password, id))

    def deletePassword(self, id):
        query = """
            DELETE FROM passwords 
            WHERE id = ?
            """
        return self.executeQuery(query, (id,))
        
    def getAll(self):
        query = """
            SELECT * FROM passwords
            """
        return self.executeQuery(query, fetch=True)
        

if __name__ == "__main__":
    print(Database().getAll())
