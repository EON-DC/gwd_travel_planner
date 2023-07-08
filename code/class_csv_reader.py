
import numpy as np
import pandas as pd

from class_dbconnect import DBConnector


class CSVReader:
    PATH = "../csv_data/gwd_location_data_cleaned_data.xlsx"
    LOCATION_COLUMN = ["ID", "CATEGORY", "ADRESS", "NAME", "W_DO", "K_DO", "DESCRIPTION"]
    ENCODING_TYPE = "WIN"

    def __init__(self, db_connector):
        self.data = None
        self.db_connector = db_connector

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

    def set_timeline_data_from_xlxs(self):
        df = pd.read_excel("csv_data/gwd_location_data_cleaned_data.xlsx")

        conn = self.db_connector
        c = conn.start_conn()

        # c.execute("""insert into tb_location(ID, CATEGORY, ADDRESS, NAME, W_DO, g_do, DESCRIPTION)
        #              values (?, ?, ?, ?, ?, ?, ?)""",)


        # todo : add real dummy data
        # conn.commit_db()
        conn.end_conn()


if __name__ == '__main__':
    conn = DBConnector(test_option=True)
    conn.create_tables()

    reader = CSVReader(conn)
    reader.set_location_data_from_xlxs()

