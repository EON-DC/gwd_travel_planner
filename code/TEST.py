import sqlite3


def main():
    # insert_data()
    # select_data()
    # insert_timeline()
    select_timeline()



def insert_timeline():
    conn = sqlite3.connect("../TEST.db")
    location_list = [1,2,3]

    c = conn.cursor()
    c.execute("insert into tb_timeline values(?, ?, ?)", (1, "someday", f"{location_list}"))
    conn.commit()
    conn.close()


def select_data():
    conn = sqlite3.connect("../TEST.db")
    c = conn.cursor()
    result_list = c.execute("select * from tb_location").fetchall()
    print(result_list)
    conn.close()

def select_timeline():
    conn = sqlite3.connect("../TEST.db")
    c = conn.cursor()
    result_list = c.execute("select * from tb_timeline").fetchall()

    location_name = list()
    for row in result_list:
        timeline_id = row[0]
        timeline_day = row[1]
        timeline_list = row[2]

        for location_id in timeline_list:
            location_name.append(c.execute("select * from tb_location where id= (?)", (location_id, )).fetchone())

    print(location_name)

    conn.close()


def insert_data():
    conn = sqlite3.connect("../TEST.db")
    c = conn.cursor()
    c.execute("insert into tb_location values(?, ?) ", (1, "호텔1",))
    c.execute("insert into tb_location values(?, ?) ", (2, "명소1",))
    c.execute("insert into tb_location values(?, ?) ", (3, "명소2",))
    conn.commit()
    conn.close()



if __name__ == '__main__':
    main()
