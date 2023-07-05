import datetime
import random
import sqlite3

from faker import Faker

from class_plan_date import PlanDate
from class_location import Location

from class_time_line import TimeLine


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
                "location_id_list"	TEXT NOT NULL,
                "username"	TEXT NOT NULL,
                "trip_name"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)
        self.commit_db()
        self.end_conn()

    ## Timeline ======================================================================= ##
    def insert_timeline(self, timeline_obj:TimeLine):
        c = self.start_conn()
        plan_date_object = timeline_obj.plan_date
        plan_date_object:PlanDate
        plan_date_id = plan_date_object.plan_date_id

        location_object_list = timeline_obj.location_list
        location_object_list: Location
        location_id_list = []
        for list_object in location_object_list:
            tmp_list = []
            for location_object in list_object:
                tmp_list.append(location_object.location_id)
            location_id_list.append(tmp_list)

        username = timeline_obj.username
        trip_name = timeline_obj.trip_name

        c.execute('insert into tb_timeline(plan_date_id, location_id_list, username, trip_name) values (?, ?, ?, ?)', \
                             (plan_date_id, str(location_id_list), username, trip_name))

        self.commit_db()
        self.end_conn()

    def find_all_timeline(self):
        c = self.start_conn()
        rows_data = c.execute("select * from tb_timeline").fetchall()
        # id, plan_date_id, location_id_list, username, trip_name
        if len(rows_data) == 0:
            return None

        find_result_list = list()
        for row in rows_data:
            time_line_id = row[0]
            plan_date_id = row[1]
            plan_date_obj = self.find_plan_date_by_id(plan_date_id)
            location_id_list_str = row[2]
            username = row[3]
            trip_name = row[4]
            location_id_list = self.convert_str_to_int_list(location_id_list_str)
            location_list = self.convert_location_id_list_to_location_list(location_id_list)
            time_line_obj = TimeLine(time_line_id, plan_date_obj, location_list, username, trip_name)
            find_result_list.append(time_line_obj)
        self.end_conn()
        return rows_data

    def convert_location_id_list_to_location_list(self, location_id_list: list):
        result_list = list()
        for element_list in location_id_list:
            temp_list = list()
            for location_id in element_list:
                temp_list.append(self.find_location_by_id(location_id))
            result_list.append(temp_list)
        return result_list

    @staticmethod
    def convert_str_to_int_list(id_list_str):
        result_list = list()
        c_idx = 0
        inner_element_idx = -1
        while c_idx < len(id_list_str):
            if c_idx == 0 or (c_idx == (len(id_list_str) - 1)):
                c_idx += 1
                continue
            if id_list_str[c_idx] == '[':
                result_list.append(list())
                inner_element_idx += 1
                c_idx += 1
                inner_row = ''
                while id_list_str[c_idx] != ']':
                    inner_row = inner_row + id_list_str[c_idx]
                    c_idx += 1
                ele_list = inner_row.split(',')
                for ele in ele_list:
                    if ele != '':
                        result_list[inner_element_idx].append(int(ele))
            else:
                c_idx += 1
        return result_list

    ## Location ======================================================================= ##
    def insert_location(self, location_obj):
        c = self.start_conn()
        name = location_obj.name
        category = location_obj.category
        address = location_obj.address
        w_do = location_obj.w_do
        g_do = location_obj.g_do
        description = location_obj.description
        c.execute('insert into tb_location(name, category, w_do, g_do, address, description) values (?, ?, ?, ?, ?, ?)',\
                  (name, category, address, w_do, g_do, description))
        self.commit_db()
        self.end_conn()

    def find_location_by_id(self, location_id):
        c = self.start_conn()
        row_data = c.execute("select * from tb_location where id = (?)", (location_id,)).fetchone()
        # location_id, name, category, w_do, g_do, address, description
        if row_data is None:
            return None
        result = Location(*row_data)
        self.end_conn()
        return result

    def find_all_location(self):
        c = self.start_conn()
        rows_data = c.execute("select * from tb_location").fetchall()
        # location_id, name, category, w_do, g_do, address, description
        if len(rows_data) == 0:
            return None
        category_list = ['미정', '숙소', '명소']
        find_result_list = list()
        for row in rows_data:
            l_id = row[0]
            name = row[1]
            category_value = row[2]
            category = category_list[category_value]
            w_do = row[3]
            g_do = row[4]
            address = row[5]
            description = row[6]
            find_result_list.append(Location(l_id, name, category, w_do, g_do, address, description))
        self.end_conn()
        return rows_data

    ## PlanDate ======================================================================= ##
    def insert_plan_date(self, plan_date_obj:PlanDate):
        c = self.start_conn()
        start = plan_date_obj.date_obj_to_str(plan_date_obj.start_date)
        end = plan_date_obj.date_obj_to_str(plan_date_obj.end_date)
        c.execute('insert into tb_plan_date(start, end) values (?, ?)', (start, end))
        self.commit_db()
        self.end_conn()

    def find_plan_date_by_id(self, plan_date_id):
        c = self.start_conn()
        row_data = c.execute("select * from tb_plan_date where id = (?)", (plan_date_id,)).fetchone()
        # plan_date_id, start_date_str, end_date_str
        if row_data is None:
            return None

        result = PlanDate(*row_data)
        self.end_conn()
        return result

    def find_all_plan_date(self):
        c = self.start_conn()
        rows_data = c.execute("select * from tb_plan_date").fetchall()
        # plan_date_id, start_date_str, end_date_str
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
            # fake plan_date
            start_date_obj = self.faker.date_between()
            day_length = random.randint(2, 10)
            end_date_obj = start_date_obj + datetime.timedelta(days=day_length)
            end_date_str = PlanDate.date_obj_to_str(end_date_obj)
            c.execute('insert into tb_plan_date(start, end) values (?, ?)',
                      (PlanDate.date_obj_to_str(start_date_obj), end_date_str,))

            # fake location
            # 인자 location_id, name, category, w_do, g_do, address, description
            fake_location_name = self.faker.building_name()
            fake_address = self.faker.address()
            random_category_num = random.randrange(0, 2)
            w_do = (random.random() * 90) - 45
            k_do = (random.random() * 90) - 45
            fake_description = self.faker.catch_phrase()
            c.execute('''
            insert into tb_location(name, category, w_do, g_do, address, description) 
            values (?, ?, ?, ?, ?, ?)''',
                      (fake_location_name, random_category_num, fake_address, w_do, k_do, fake_description,))

            # fake timeline
            # 인자 timeline_id, plan_date, location_list, username, trip_name
            random_plan_date_id = random.randrange(1, 1001)
            random_location_id_list = list()
            random_day_count = random.randint(1, 6)
            for _ in range(random_day_count):
                random_location_id_list.append(list())
            temp_list = random.sample(range(1, 1001), random.randint(2, 10))
            for l_id in temp_list:
                random_location_id_list[random.randint(0, random_day_count-1)].append(l_id)

            fake_username = self.faker.name()
            fake_trip_name = self.faker.town()
            c.execute('''
            insert into tb_timeline(plan_date_id, location_id_list, username, trip_name) 
            values (?, ?, ?, ?)''',
                      (random_plan_date_id, f'{random_location_id_list}', fake_username, fake_trip_name,))

        self.commit_db()

        self.end_conn()


if __name__ == '__main__':
    conn = DBConnector(test_option=False)
    conn.create_tables()
    conn.make_fake_date_data()
    plan_date = PlanDate(1, '2023-04-05', '2023-04-08')
    location = Location(7, '망상해수욕장', '1', '1.11111', '2.22222', '강원도어쩌구', '망상하는해수욕장')
    location2 = Location(3, '해수욕장', '1', '1.41111', '2.62222', '강원도저쩌구', '그냥해수욕장')
    location3 = Location(85, '오죽헌', '1', '1.41111', '2.62222', '강원도머시기', '오죽헌이올시다')
    # # conn.insert_plan_date(plan_date)
    # # conn.insert_location(location)
    # # print(a)
    timeline = TimeLine(1, plan_date, [[location], [location2, location3], []], '사용자', '사용자여행')
    conn.insert_timeline(timeline)
    # conn.insert_timeline(timeline)
    # for plan_date in conn.find_all_plan_date():
    #     print(plan_date)
    # for location in conn.find_all_location():
    #     print(location)
    # for timeline in conn.find_all_timeline():
    #     print(timeline)

