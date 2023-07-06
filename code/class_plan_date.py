import datetime


class PlanDate:

    @staticmethod
    def str_date_parser(date_str):
        # date_str 형태 : 'YYYY-mm-dd'
        datetime_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return datetime_obj

    @staticmethod
    def date_obj_to_str(datetime_obj):
        # 표현형태
        datetime_obj:datetime.datetime
        return datetime_obj.strftime('%Y-%m-%d')

    def __init__(self, plan_date_id, start_date_str, end_date_str):
        self.plan_date_id = plan_date_id
        self.start_date = PlanDate.str_date_parser(start_date_str)
        self.end_date = PlanDate.str_date_parser(end_date_str)

    def __str__(self):
        return f"{self.__repr__()}"

    def __repr__(self):
        return f"{self.__dict__}"

