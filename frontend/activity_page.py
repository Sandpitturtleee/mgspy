from nicegui import ui
import base64
from datetime import datetime
from frontend.data_collectors import DataCollectors
from frontend.gui import Gui


class ActivityPage(Gui):
    def __init__(self):
        super().__init__()
        self.input_nick = None
        self.plot_area = None
        self.start_dt = datetime(2025, 6, 28, 11, 0, 0)
        self.end_dt = datetime(2025, 6, 28, 12, 0, 0)
        self.collector = DataCollectors(start_dt=self.start_dt, end_dt=self.end_dt)

    def page(self):
        ui.page_title("Activity")
        with ui.column().classes(f"{self.background} w-full min-h-screen items-center justify-start"):
            self.navbar()
            self.input_nick = ui.input("Nick", placeholder="Enter player nick").classes(
                "w-[400px] text-lg mt-14"
            )
            ui.button(
                "Show player activity",
                on_click=self.make_plot,
            ).props("size=lg").classes(
                "bg-blue-700 text-white text-xl font-bold px-8 py-2 mt-4 rounded-lg hover:bg-blue-800 transition"
            )
            self.plot_area = ui.image().classes(
                "w-[900px] h-[400px] mt-10 bg-gray-50 border border-gray-300"
            )

    def make_plot(self):
        nick = self.input_nick.value.strip()
        if not nick:
            self.plot_area.source = None
            ui.notify("Please enter a nick!", color="red")
            return
        timestamps = self.collector.get_player_activity(nick=nick)
        if not timestamps:
            self.plot_area.source = None
            ui.notify(f"No activity found for nick {nick}", color="red")
            return
        img = self.collector.gui_plot_player_activity(timestamps=timestamps)
        img_b64 = base64.b64encode(img.read()).decode("ascii")
        data_url = f"data:image/png;base64,{img_b64}"
        self.plot_area.source = data_url
