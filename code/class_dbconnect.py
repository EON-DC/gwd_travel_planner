import sqlite3

from faker import Faker

class DBConnector:
    _instance = None

    def __new__(cls, test_option=None):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, test_option=None):
        self.conn = None
        self.test_option = test_option
        self.faker = Faker("ko-KR")

    def start_conn(self):
        if self.test_option is True:
            self.conn = sqlite3.connect('db/db_test.db')
        else:
            self.conn = sqlite3.connect('db/gwd_travel.db')
        return self.conn.cursor()

    def end_conn(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def commit_db(self):
        if self.conn is not None:
            self.conn.commit()
        else:
            raise f"cannot commit database! {self.__name__}"

    ## CREATE TABLES ======================================================================= ##
    def create_tables(self):
        c = self.start_conn()
        c.execute("""
            DROP TABLE IF EXISTS tb_location;
            CREATE TABLE "tb_location" (
                "id"	INTEGER,
                "name"	TEXT NOT NULL,
                "w_do"	REAL NOT NULL,
                "g_do"	REAL NOT NULL,
                "address"	TEXT NOT NULL,
                "description"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            DROP TABLE IF EXISTS tb_plan_date;
            CREATE TABLE "tb_plan_date" (
                "id"	INTEGER,
                "start"	TEXT,
                "end"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            DROP TABLE IF EXISTS tb_timeline;
            CREATE TABLE "tb_timeline" (
                "id"	INTEGER,
                "plan_date_id"	INTEGER NOT NULL,
                "location_id_list"	INTEGER NOT NULL,
                "username"	TEXT NOT NULL,
                "trip_name"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)


    ## Timeline ======================================================================= ##

    ## Location ======================================================================= ##
    ## PlanDate ======================================================================= ##



if __name__ == '__main__':
    conn = DBConnector(test_option=False)
    conn.start_conn()
    conn.end_conn()