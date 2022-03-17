from datetime import datetime
import sqlite3
'''
This class will be used for handling all sqlite3 processes,
Such as inserting used clips into memory and scanning memory
to avoid story duplication.
'''

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("stories.db")
        self.curr = self.conn.cursor()
        self.date = datetime.now().date()
        self.create_table()


    # CREATES TABLE IF IT DOES NOT EXISTS IN OUT DB
    def create_table(self):
        # self.curr.execute("""DROP TABLE stories""")
        self.curr.execute("""CREATE TABLE IF NOT EXISTS stories(
            id Text PRIMARY KEY,
            topic TEXT,
            title TEXT,
            sub_title TEXT,
            date_created DATE
        ) """)

    def insert(self, story):
        self.curr.execute("""INSERT OR IGNORE INTO stories VALUES(?,?,?,?,?) """, story)
        self.conn.commit()

    def verifyClip(self, clip_id):
        self.curr.execute("""SELECT * FROM stories""")
        rows = self.curr.fetchall()
        for i in rows:
            if i[0] == clip_id:
                return False
            else:
                return True
        



