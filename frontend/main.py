from datetime import datetime
from nicegui import ui
from frontend.data_collectors import DataCollectors
from frontend.gui import Gui

if __name__ in {"__main__", "__mp_main__"}:
    # start_dt = datetime(2025, 6, 28, 11, 0, 0)
    # end_dt = datetime(2025, 6, 28, 12, 0, 0)
    # collector = DataCollectors(start_dt=start_dt, end_dt=end_dt)
    # timestamps = collector.get_player_activity(nick="Luxvyu")
    # collector.plot_player_activity(timestamps=timestamps)

    Gui()
    ui.run()
