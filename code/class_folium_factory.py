from class_plan_date import PlanDate
from class_location import Location
from class_time_line import TimeLine
import folium

class FoliumMapFactory:
    def __init__(self, location_obj:Location = None):
        self.location = location_obj
        self.folium_map = folium.Map(
            location=[location_obj.w_do, location_obj.g_do], zoom_start=13
        )

    def add_marker(self, location_list:list[Location]):
        pass
    def make_html(self):
        # self.folium_map
        pass

if __name__ == '__main__':
    plan_date = PlanDate(1, '2023-04-05', '2023-04-08')
    location = Location(7, '망상해수욕장', '1', '1.11111', '2.22222', '강원도어쩌구', '망상하는해수욕장')
    location2 = Location(3, '해수욕장', '1', '1.41111', '2.62222', '강원도저쩌구', '그냥해수욕장')
    location3 = Location(85, '오죽헌', '1', '1.41111', '2.62222', '강원도머시기', '오죽헌이올시다')
    # conn.insert_plan_date(plan_date)
    # conn.insert_location(location)
    # print(a)
    timeline = TimeLine(1, plan_date, [[location], [location2, location3], []], '사용자', '사용자여행')

