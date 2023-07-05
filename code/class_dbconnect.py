import datetime
import random
import sqlite3

from faker import Faker

from class_plan_date import PlanDate


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
        c.executescript("""
            DROP TABLE IF EXISTS tb_location;
            CREATE TABLE "tb_location" (
                "id"	INTEGER,
                "name"	TEXT NOT NULL,
                "category"	INTEGER NOT NULL,
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
        self.commit_db()
        self.end_conn()

    ## Timeline ======================================================================= ##
    def find_all_timeline(self):
        c = self.start_conn()
        c.execute("select ")
        self.end_conn()

    ## Location ======================================================================= ##


    def find_all_location(self):
        c = self.start_conn()
        c.execute("select ")
        self.end_conn()

    ## PlanDate ======================================================================= ##
    def find_all_plan_date(self):
        c = self.start_conn()
        rows_data = c.execute("select * from tb_plan_date").fetchall()
        if len(rows_data) == 0:
            return None

        find_result_list = list()
        for row in rows_data:
            find_result_list.append(PlanDate(*row))
        self.end_conn()
        return rows_data

    def make_fake_date_data(self):
        c = self.start_conn()

        for i in range(1000):
            start_date_obj = self.faker.date_between()
            day_length = random.randint(2, 10)
            end_date_obj = start_date_obj + datetime.timedelta(days=day_length)
            end_date_str = PlanDate.date_obj_to_str(end_date_obj)
            c.execute('insert into tb_plan_date(start, end) values (?, ?)',
                      (PlanDate.date_obj_to_str(start_date_obj), end_date_str,))
        self.commit_db()

        self.end_conn()


if __name__ == '__main__':
    conn = DBConnector(test_option=False)
