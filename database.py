from datetime import datetime
import sqlite3
from decouple import config

'''
This class will be used for handling all sqlite3 processes,
Such as inserting used clips into memory and scanning memory
to avoid story duplication.
'''

db =  config('SQLITE_DB')

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(db)
        self.curr = self.conn.cursor()
        self.date = datetime.now().date()
        self.create_table()


    # CREATES TABLE IF IT DOES NOT EXISTS IN OUT DB
    def create_table(self):
        # self.curr.execute("""DROP TABLE stories""")
        self.curr.execute("""CREATE TABLE IF NOT EXISTS used_clips(
            id Text PRIMARY KEY,
            topic TEXT,
            title TEXT,
            sub_title TEXT,
            date_created DATE
        ) """)

    def insert(self, story):
        self.curr.execute("""INSERT OR IGNORE INTO used_clips VALUES(?,?,?,?,?) """, story)
        self.conn.commit()

    def verifyClip(self, clip_id):
        self.curr.execute("""SELECT * FROM used_clips""")
        rows = self.curr.fetchall()
        for i in rows:
            if i[0] == clip_id:
                return False
            else:
                return True
        


# if __name__ == "__main__":
