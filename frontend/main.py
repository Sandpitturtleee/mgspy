from nicegui import ui
from gui import Gui
from data_page import DataPage
from activity_page import ActivityPage


class App(Gui):
    def __init__(self):
        super().__init__()
        self.table_page = DataPage()
        self.activity_page = ActivityPage()
        ui.page('/')(self.table_page.page)
        ui.page('/activity')(self.activity_page.page)


if __name__ in {"__main__", "__mp_main__"}:
    App()
    ui.run(host="127.0.0.1", port=8080)
