from nicegui import ui

LIGHT_GRAY = "bg-gray-100"
TOOLBAR_ROW = "w-full flex flex-row items-center justify-center py-4 gap-0 bg-transparent shadow-none"
TOOLBAR_TEXT = (
    "text-black text-xl font-bold px-6 py-2 rounded-lg transition-all no-underline"
)
TOOLBAR_TEXT_HOVER = "hover:text-blue-600"


class Gui:
    def __init__(self):
        self.background = LIGHT_GRAY

    @staticmethod
    def navbar():
        with ui.row().classes(TOOLBAR_ROW):
            ui.link("Data", "/").classes(f"{TOOLBAR_TEXT} {TOOLBAR_TEXT_HOVER}")
            ui.link("Activity", "/activity").classes(
                f"{TOOLBAR_TEXT} {TOOLBAR_TEXT_HOVER}"
            )
