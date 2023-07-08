import io
import folium
from class_location import Location


class FoliumMapFactory:
    def __init__(self, location_obj: Location = None, location_list: list[Location] = None):
        self.location = location_obj
        self.location_list = location_list
        self.folium_map = None
        self.set_folium_map()

    def set_folium_map(self):
        location_ = self.location
        if location_ is not None:
            self.folium_map = folium.Map(
                location=[location_.w_do, location_.g_do], zoom_start=13
            )
        else:
            self.folium_map = folium.Map(
                location=[37.8853984, 127.7297758], zoom_start=9
            )  # 강원도청

    def set_location(self, location_obj):
        self.location = location_obj
        self.set_folium_map()

    def clear(self):
        self.location = None
        self.location_list = None

    def set_markers(self, location_list: list[Location]):
        self.location_list = location_list

    def make_html(self):
        if self.location is None:
            data = io.BytesIO()
            self.folium_map.save(data, close_file=False)
            return data.getvalue().decode()

        # 선택 로케이션 마커 추가
        self.folium_map: folium.Map
        location_ = self.location
        folium.Marker(location=[location_.w_do, location_.g_do],
                      icon=folium.Icon(color='purple', icon='star')).add_to(self.folium_map)

        # 리스트마커 추가
        if self.location_list is not None:
            att_marker_group = folium.FeatureGroup(name="attraction").add_to(self.folium_map)
            hotel_marker_group = folium.FeatureGroup(name="hotel").add_to(self.folium_map)
            for location_ in self.location_list:
                category = location_.category
                w_do = location_.w_do
                g_do = location_.g_do
                if category == "숙소":
                    icon = folium.Icon(color='blue', icon='star', prefix='fa')
                    att_marker_group.add_child(folium.Marker((w_do, g_do), icon=icon).add_to(self.folium_map))
                elif category == "명소":
                    icon = folium.Icon(color='red', icon='house', prefix='fa')
                    hotel_marker_group.add_child(folium.Marker((w_do, g_do), icon=icon).add_to(self.folium_map))

        data = io.BytesIO()
        self.folium_map.save(data, close_file=False)
        return data.getvalue().decode()

