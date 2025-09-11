from gui import Gui
from nicegui import ui

if __name__ in {"__main__", "__mp_main__"}:
    Gui()
    ui.run(host="127.0.0.1", port=8080)
