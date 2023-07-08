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
    def insert_timeline(self, timeline_obj: TimeLine):
        c = self.start_conn()
        plan_date_object = timeline_obj.plan_date
        plan_date_object: PlanDate
        plan_date_id = plan_date_object.plan_date_id

        location_object_list = timeline_obj.location_list
        location_object_list: Location
        location_id_list = list()
        for list_object in location_object_list:
            tmp_list = list()
            for location_object in list_object:
                tmp_list.append(location_object.location_id)
            location_id_list.append(tmp_list)

        username = timeline_obj.username
        trip_name = timeline_obj.trip_name

        c.execute('insert into tb_timeline(plan_date_id, location_id_list, username, trip_name) values (?, ?, ?, ?)',
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
        return find_result_list

    def find_recent_timelines(self):
        all_timeline_list = self.find_all_timeline()
        all_timeline_list.sort()
        recent_timeline_list = list()
        for row in all_timeline_list[:10]:
            recent_timeline_list.append(row)
        return recent_timeline_list

    def create_plan_date_obj(self, start_date_str, end_date_str) -> PlanDate:
        """db에 등록하여 autoincrement된 id를 가진 개체가 반환됨"""
        c = self.start_conn()
        c.execute('insert into tb_plan_date(start, end) values (?, ?)', (start_date_str, end_date_str))
        self.commit_db()
        # id 최댓값으로 선택하게 쿼리변경, 객체가 넘어오게 인스턴스화-date클래스에서
        created_date_row = c.execute('select * from tb_plan_date order by id desc limit 1').fetchone()
        # date_id = created_date_row[0]
        # start = created_date_row[1]
        # end = created_date_row[2]
        # created_date_obj = PlanDate(date_id, start, end)
        # created_date_obj = PlanDate(created_date_row[0], created_date_row[1], created_date_row[2])
        created_date_obj = PlanDate(*created_date_row)
        self.end_conn()
        return created_date_obj

    def create_time_line_obj(self, location_list: list[Location],
                             start_date_str: str,
                             end_date_str: str,
                             trip_name: str,
                             username_str = 'username') -> TimeLine:
        plan_date = self.create_plan_date_obj(start_date_str, end_date_str)
        c = self.start_conn()
        last_row = c.execute('select * from tb_timeline order by id desc limit 1').fetchone()
        if last_row is None:
            last_id = 1
        else:
            last_id = last_row[0] + 1
        time_line = TimeLine(last_id, plan_date, location_list, username_str, trip_name)
        self.insert_timeline(time_line)
        """db에 등록하여 autoincrement된 id를 가진 timeline개체가 반환됨
        위에서 만든 plan_date 함수와 기존 insert timeline 함수를 활용하여 str과 location 개체만으로도 time_line_obj를 database에 등록할 수 있음"""
        created_timeline_row = c.execute('select * from tb_timeline order by id desc limit 1').fetchone()
        t_id = created_timeline_row[0]
        created_timeline_obj = self.find_timeline_by_id(t_id)
        self.end_conn()
        return created_timeline_obj

    def find_timeline_by_id(self, user_id: int):
        c = self.start_conn()
        row = c.execute('select * from tb_timeline where id = ?', (user_id,)).fetchone()
        time_line_id = row[0]
        plan_date_id = row[1]
        plan_date_obj = self.find_plan_date_by_id(plan_date_id)
        location_id_list_str = row[2]
        username = row[3]
        trip_name = row[4]
        location_id_list = self.convert_str_to_int_list(location_id_list_str)
        location_list = self.convert_location_id_list_to_location_list(location_id_list)
        time_line_obj = TimeLine(time_line_id, plan_date_obj, location_list, username, trip_name)

        self.end_conn()
        return time_line_obj

    def find_timeline_by_username(self, username: str):
        c = self.start_conn()
        lines = c.execute('select * from tb_timeline where username = ?', (username,)).fetchall()
        line_obj_list = list()
        for row in lines:
            line_obj_list.append(self.find_timeline_by_id(row[0]))
        self.end_conn()
        return line_obj_list

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

    def update_timeline_by_id_username(self, timeline_id, username):
        c = self.start_conn()
        c.execute('update tb_timeline set username = (?) where id = (?)', (username, timeline_id))
        self.commit_db()
        self.end_conn()
        line_obj = self.find_timeline_by_id(timeline_id)
        return line_obj

    def delete_timeline_by_id(self, timeline_id: int):
        c = self.start_conn()
        c.execute("delete from tb_timeline where id = ?", (timeline_id,))
        self.commit_db()
        self.end_conn()

    ## Location ======================================================================= ##
    def insert_location(self, location_obj):
        c = self.start_conn()
        name = location_obj.name
        category = location_obj.category
        if isinstance(category, str):
            if category == '숙소':
                category = 0
            else:
                category = 1
        address = location_obj.address
        w_do = location_obj.w_do
        g_do = location_obj.g_do
        description = location_obj.description
        c.execute('insert into tb_location(name, category, w_do, g_do, address, description) values (?, ?, ?, ?, ?, ?)', \
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
        category_list = ['숙소', '명소']
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
        return find_result_list

    def find_location_list_by_name(self, location_name_str: str) -> list:
        location_list = list()
        c = self.start_conn()
        # print(c.execute("select * from tb_location where name like ?", ("%수민%", )).fetchall())
        locations = c.execute("select * from tb_location where name like ?", (f"%{location_name_str}%",)).fetchall()
        if len(locations) == 0:
            return None

        for i in locations:
            location_list.append(i[1])
        self.end_conn()
        return location_list

    # 장소이름 혹은 주소에 검색어가 포함된 결과 추출
    def find_location_list_by_name_or_address(self, location_name_str: str) -> list:
        location_list = list()
        c = self.start_conn()
        # print(c.execute("select * from tb_location where name like ?", ("%수민%", )).fetchall())
        locations = c.execute("select * from tb_location where name like ? or address like ?", (f"%{location_name_str}%", f"%{location_name_str}%")).fetchall()
        if len(locations) == 0:
            return None

        for i in locations:
            location_list.append((i[1], i[5]))
        self.end_conn()
        return location_list

    def delete_location_by_id(self, location_id: int):
        c = self.start_conn()
        cur = c.execute("delete from tb_location where id = ?", (location_id,))
        self.commit_db()
        self.end_conn()

    ## PlanDate ======================================================================= ##
    def insert_plan_date(self, plan_date_obj: PlanDate):
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
                      (fake_location_name, random_category_num, w_do, k_do, fake_address, fake_description,))

            # fake timeline
            # 인자 timeline_id, plan_date, location_list, username, trip_name
            random_plan_date_id = random.randrange(1, 1001)
            random_location_id_list = list()
            random_day_count = random.randint(1, 6)
            for _ in range(random_day_count):
                random_location_id_list.append(list())
            temp_list = random.sample(range(1, 1001), random.randint(2, 10))
            for l_id in temp_list:
                random_location_id_list[random.randint(0, random_day_count - 1)].append(l_id)

            fake_username = self.faker.name()
            fake_trip_name = self.faker.town()
            c.execute('''
            insert into tb_timeline(plan_date_id, location_id_list, username, trip_name) 
            values (?, ?, ?, ?)''',
                      (random_plan_date_id, f'{random_location_id_list}', fake_username, fake_trip_name,))

        self.commit_db()
        self.end_conn()

    def delete_plan_date_by_id(self, plan_date_id: int):
        c = self.start_conn()
        c.execute("delete from tb_plan_date where id = ?", (plan_date_id,))
        self.commit_db()
        self.end_conn()

    #ui측 전달함수===========================================================
    # [(이름1, 주소1), (이름2, 주소2)] 형태로 전달 필요한지 확인
    def get_recommended_hotel(self):
        all_locations = self.find_all_location()
        result_list = list()
        for location_ in all_locations:
            if location_.category == '숙소':
                result_list.append(location_)
        recommended_hotel_list = list()
        for obj in result_list:
            obj: Location
            name, address = obj.name, obj.address
            recommended_hotel_list.append((name, address))
        return recommended_hotel_list

    def get_recommended_attraction(self):
        all_locations = self.find_all_location()
        result_list = list()
        for location_ in all_locations:
            if location_.category == '명소':
                result_list.append(location_)
        # recommended_attraction_list = list()
        # for obj in result_list:
        #     obj: Location
        #     name, address = obj.name, obj.address
        #     recommended_attraction_list.append((name, address))
        return result_list

    def get_recent_location_name_address(self):
        location_name_address_list = list()
        for timeline_obj in self.find_recent_timelines():
            for location_obj_list in timeline_obj.location_list:
                tmp_list = list()
                for location_obj in location_obj_list:
                    tmp_list.append((location_obj.name, location_obj.address))
                location_name_address_list.append(tmp_list)
        return location_name_address_list

    def get_recent_trip_name_date(self):
        trip_name_date_list = list()
        for timeline_obj in self.find_recent_timelines():
            date_to_str = PlanDate.date_obj_to_str
            trip_name_date_list.append((timeline_obj.trip_name, date_to_str(timeline_obj.plan_date.start_date), date_to_str(timeline_obj.plan_date.end_date)))
        return trip_name_date_list

if __name__ == '__main__':
    conn = DBConnector(test_option=False)
    conn.create_tables()
    conn.make_fake_date_data()
    # plan_date = PlanDate(1, '2023-04-05', '2023-04-08')
    # # conn.insert_plan_date(plan_date)
    # # conn.insert_location(location)
    # # print(a)
    # timeline = TimeLine(1, plan_date, [[location], [location2, location3], []], '사용자', '사용자여행')
    # conn.insert_timeline(timeline)
    # print(conn.find_location_list_by_name('이'))
    # conn.insert_timeline(timeline)
    # for plan_date in conn.find_all_plan_date():
    #     print(plan_date)
    # for location in conn.find_all_location():
    #     print(location)
    # for timeline in conn.find_all_timeline():
    #     print(timeline)
    # l = conn.find_all_timeline()
    # l.sort()
    # # print(l)
    # for row in l[:10]:
    #     print(row)
    # location = Location(90, '망상해수욕장', '1', '1.11111', '2.22222', '강원도어쩌구', '망상하는해수욕장')
    # location2 = Location(55, '해수욕장', '1', '1.41111', '2.62222', '강원도저쩌구', '그냥해수욕장')
    # location3 = Location(23, '오죽헌', '1', '1.41111', '2.62222', '강원도머시기', '오죽헌이올시다')


    # print(conn.delete_location_by_id(998))
    # print(conn.delete_timeline_by_id(1001))
    # print(conn.delete_plan_date_by_id(1001))
    # print(conn.find_timeline_by_username('노영미'))
    # print(conn.find_timeline_by_id(999).username)
    # print(conn.update_timeline_by_id_username(999, '사무엘잭슨'))
    # print(conn.update_timeline_by_id_username(999, '사무엘잭슨').username)
    # print(conn.find_timeline_by_id(999).username)

    # print(conn.create_plan_date_obj('2023-07-06', '2023-07-09'))
    # print(conn.create_time_line_obj('레이디가가,', ([location3], [location2, location], []), '2023-08-10', '2023-08-13', '여행이름'))
    print(conn.get_recommended_attraction())
    # print(len(conn.get_recommended_attraction()))
    # print(conn.get_recommended_hotel())
    # print(len(conn.get_recommended_hotel()))
    # print(conn.find_all_location())
    # print(conn.find_location_list_by_name_or_address('민수'))
    #
    # 이전 여행 불러오기 클릭시 최근 10개 반환
    # location_name_list =list()
    # for timeline_obj in conn.find_recent_timelines():
    #     # print(timeline_obj)
    #
    #     # date_to_str = PlanDate.date_obj_to_str
    #     # print(timeline_obj.trip_name, date_to_str(timeline_obj.plan_date.start_date), date_to_str(timeline_obj.plan_date.end_date))
    #     for location_obj_list in timeline_obj.location_list:
    #         tmp_list = list()
    #         for location_obj in location_obj_list:
    #             tmp_list.append((location_obj.name, location_obj.address))
    #         location_name_list.append(tmp_list)
    #     print(location_name_list)

    # print(conn.get_recent_location_name_address())
    # print(conn.get_recent_trip_name_date())
    # print(conn.find_recent_timelines())

