from nicegui import ui
from frontend.gui import Gui
from frontend.data_page_helpers import DataPageHelpers


class DataPage(Gui):
    """
    A GUI page to display and filter player data in a sortable table using NiceGUI.

    Attributes
    ----------
    table_data : list[dict]
        List of all player data to be displayed in the table.
    filtered_data : list[dict]
        List of filtered player data.
    input_nick : ui.input
        NiceGUI input widget for the player nickname filter.
    helpers : DataPageHelpers
        Helper class instance for table data and filtering.

    Methods
    -------
    page()
        Build and render the data table UI, input, and filtering button.
    """
    def __init__(self):
        super().__init__()
        self.table_data = []
        self.filtered_data = []
        self.input_nick = None
        self.helpers = DataPageHelpers()

    def page(self):
        """
        Build the user interface for the Data page.

        The page includes:
            - A player nick input for filtering.
            - A button for applying the filter.
            - A table to show player data (filterable by nick).

        Table columns include:
            - Nick: player nickname (sortable)
            - Lvl: player level (sortable)
            - Guild: player guild (not sortable)

        Returns
        -------
        None
        """
        ui.page_title("Data")
        with ui.column().classes(f"{self.background} w-full min-h-screen items-center justify-start"):
            self.navbar()
            self.table_data = self.helpers.fill_table()
            self.input_nick = ui.input("Nick", placeholder="Enter player nick").classes(
                "w-[400px] text-lg mt-14"
            )

            def update_table():
                nick = self.input_nick.value.strip()
                data = self.helpers.fill_table_input(nick)
                if not data:
                    data = self.table_data
                table.rows = data

            ui.button(
                "Show player data",
                on_click=update_table,
            ).props("size=lg").classes(
                "bg-blue-700 text-white text-xl font-bold px-8 py-2 mt-4 rounded-lg hover:bg-blue-800 transition"
            )

            columns = [
                {'name': 'nick', 'label': 'Nick', 'field': 'nick', 'sortable': True, 'align': 'left'},
                {'name': 'lvl', 'label': 'Lvl', 'field': 'lvl', 'sortable': True, 'align': 'right'},
                {'name': 'guild', 'label': 'Guild', 'field': 'guild', 'sortable': False, 'align': 'left'},
            ]

            table = ui.table(
                columns=columns,
                rows=self.table_data,
                row_key='nick'
            ).classes("text-lg w-[700px]")
