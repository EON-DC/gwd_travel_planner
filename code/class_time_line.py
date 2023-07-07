class TimeLine:
    def __init__(self, timeline_id, plan_date,  location_list,username, trip_name):
        self.time_line_id = timeline_id
        self.plan_date = plan_date
        self.location_list = location_list
        self.username = username
        self.trip_name = trip_name
    def __str__(self):
        return f"{self.__repr__()}"

    def __repr__(self):
        return f"{self.__dict__}"

    # 솔팅 함수 추가
    def __lt__(self, other):
        return self.plan_date.end_date > other.plan_date.end_date


