LOCATION_CATEGORY_HOTEL=0
LOCATION_CATEGORY_ATTRACTION=1


class Location:
    def __init__(self, location_id, name, category, w_do, g_do, address, description):
        self.location_id = location_id
        self.name = name
        self.category = category
        self.w_do = w_do
        self.g_do = g_do
        self.address = address
        self.description = description


