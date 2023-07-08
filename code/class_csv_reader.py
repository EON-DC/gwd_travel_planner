import random

import numpy as np
import pandas as pd

from class_dbconnect import DBConnector
from class_plan_date import PlanDate


class CSVReader:
    PATH = "../csv_data/gwd_location_data_cleaned_data.xlsx"
    LOCATION_COLUMN = ["ID", "CATEGORY", "ADRESS", "NAME", "W_DO", "K_DO", "DESCRIPTION"]
    ENCODING_TYPE = "WIN"

    def __init__(self, db_connector):
        assert isinstance(db_connector, DBConnector)
        self.data = None
        self.db_connector = db_connector
        self.set_location_data_from_xlxs()
        self.set_timeline_dummy_data()

    def set_location_data_from_xlxs(self):
        df = pd.read_excel(self.PATH, engine="openpyxl")
        conn = self.db_connector
        c = conn.start_conn()

        for idx in df.index:
            loc_row = df.iloc[idx]
            if np.isnan(loc_row.DESCRIPTION):
                desc = ''
            else:
                desc = loc_row.DESCRIPTION

            c.execute("""insert into tb_location(ID, CATEGORY, ADDRESS, NAME, W_DO, g_do, DESCRIPTION)
             values (?, ?, ?, ?, ?, ?, ?)""",
                      (int(loc_row.ID), int(loc_row.CATEGORY), loc_row.ADDRESS, loc_row.NAME, loc_row.W_DO,
                       loc_row.G_DO, desc,))
        conn.commit_db()
        conn.end_conn()

    def set_timeline_dummy_data(self):

        location_list = self.db_connector.find_all_location()

        sample_list = random.sample(location_list, 10)
        inserted_location_list = [sample_list[0:3], sample_list[3:5], sample_list[5:10]]

        timeline_obj = self.db_connector.create_time_line_obj(inserted_location_list, "2022-03-06", "2022-03-08", '테스트 여행')



if __name__ == '__main__':
    conn = DBConnector(test_option=False)
    conn.create_tables()

    reader = CSVReader(conn)
    reader.set_location_data_from_xlxs()
    reader.set_timeline_dummy_data()
    # for plan_date in conn.find_all_plan_date():
    #     print(plan_date)
    for location in conn.find_all_location():
        print(location)
    for timeline in conn.find_all_timeline():
        print(timeline)
