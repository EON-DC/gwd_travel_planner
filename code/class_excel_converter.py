from class_time_line import TimeLine
from class_plan_date import PlanDate
from openpyxl.styles import Alignment, Font, Border, Side, PatternFill

from class_location import Location
import openpyxl


class ExcelConverter:
    def __init__(self, timeline_obj: TimeLine = None):
        self.time_line = timeline_obj
        self.work_book = None

    def make_workbook(self):
        # 워크북 생성
        wb = openpyxl.Workbook()
        # 시트 활성화
        ws = wb.worksheets[0]  # wb.active 로 써도 됨
        # 시트 이름바꾸기
        ws.title = 'worksheet'
        # 새로운 시트만들기
        ws['B2'] = 'cell'

        # 가운데 정렬
        align_center = Alignment(horizontal='center', vertical='center')

        # 글씨체 굵게
        font_bold = Font(size=12, bold=True, color='000000')  # 000000: black

        # 셀 색깔 채우기
        fill_blue = PatternFill('solid', fgColor='819FF7')

        # 테두리 선넣기
        thin_border = Border(left=Side(border_style='thin', color='000000'),
                             right=Side(border_style='thin', color='000000'),
                             top=Side(border_style='thin', color='000000'),
                             bottom=Side(border_style='thin', color='000000'))

        # 위의 4가지 B2 cell에 적용시키기 + 값 'cell'에서 'text'로 바꾸기
        ws['B2'].alignment = align_center
        ws['B2'].font = font_bold
        ws['B2'].fill = fill_blue
        ws['B2'].border = thin_border
        ws['B2'].value = 'text'
        # 워크북 filename 으로 저장(없으면 새로생성)
        filename = "../csv_data/test.xlsx"
        wb.save(filename)

if __name__ == '__main__':
    plan_date = PlanDate(1, '2023-04-05', '2023-04-08')
    location = Location(7, '망상해수욕장', '1', '1.11111', '2.22222', '강원도어쩌구', '망상하는해수욕장')
    location2 = Location(3, '해수욕장', '1', '1.41111', '2.62222', '강원도저쩌구', '그냥해수욕장')
    location3 = Location(85, '오죽헌', '1', '1.41111', '2.62222', '강원도머시기', '오죽헌이올시다')
    # conn.insert_plan_date(plan_date)
    # conn.insert_location(location)
    # print(a)
    timeline = TimeLine(1, plan_date, [[location], [location2, location3], []], '사용자', '사용자여행')
    ec = ExcelConverter(timeline)
    ec.make_workbook()
