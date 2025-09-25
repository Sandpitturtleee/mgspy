from nicegui import ui
import base64
from datetime import datetime
from frontend.activity_page_helpers import ActivityPageHelpers
from frontend.gui import Gui


class ActivityPage(Gui):
    """
        A GUI page for displaying player activity as an interactive plot using NiceGUI.

        Attributes
        ----------
        start_time : ui.input
            NiceGUI input widget for selecting the start time (HH:MM).
        start_date : ui.input
            NiceGUI input widget for selecting the start date (YYYY-MM-DD).
        start_date_str : str
            Default value for the start date input widget.
        start_time_str : str
            Default value for the start time input widget.
        input_nick : ui.input
            NiceGUI input widget for the player's nick.
        plot_area : ui.image
            NiceGUI image widget for displaying the activity plot.
        helpers : ActivityPageHelpers
            Helper class instance for business logic and plotting.

        Methods
        -------
        page()
            Build and render the activity page UI and widgets.
        convert_datetime() -> datetime
            Combine start date and time input fields into a `datetime` object.
        make_plot()
            Triggered on button click; retrieves player activity, generates and displays the plot.
        """
    def __init__(self):
        super().__init__()
        self.start_time = None
        self.start_date = None
        self.start_date_str = '2025-06-28'
        self.start_time_str = '11:00'
        self.input_nick = None
        self.plot_area = None
        self.helpers = ActivityPageHelpers()

    def page(self):
        """
        Build the user interface for the Activity page.

        The page includes:
            - Player nick input
            - Date and time input fields
            - Button to fetch and plot activity
            - Output area for the plot image

        Returns
        -------
        None
        """
        ui.page_title("Activity")
        with ui.column().classes(f"{self.background} w-full min-h-screen items-center justify-start"):
            self.navbar()
            self.input_nick = ui.input("Nick", placeholder="Enter player nick").classes(
                "w-[400px] text-lg mt-14"
            )
            with ui.column().classes("mt-5 items-start"):
                with ui.row().classes("gap-1 items-center"):
                    self.start_date = ui.input('', value=self.start_date_str) \
                        .props('placeholder=YYYY-MM-DD dense').classes('w-24 text-xs px-1 py-1')
                    self.start_time = ui.input('', value=self.start_time_str) \
                        .props('placeholder=HH:MM dense').classes('w-16 text-xs px-1 py-1 ml-1')

            ui.button(
                "Show player activity",
                on_click=self.make_plot,
            ).props("size=lg").classes(
                "bg-blue-700 text-white text-xl font-bold px-8 py-2 mt-4 rounded-lg hover:bg-blue-800 transition"
            )
            self.plot_area = ui.image().classes(
                "w-[900px] h-[400px] mt-10 bg-gray-50 border border-gray-300"
            )

    def convert_datetime(self):
        """
        Combine start date and start time fields into a single `datetime` object.

        Raises
        ------
        ValueError
            If date or time fields are invalid or not in the expected format.

        Returns
        -------
        datetime
            Combined datetime from provided fields.
        """
        date_str = self.start_date.value  # e.g. '2025-06-28'
        time_str = self.start_time.value  # e.g. '11:00'
        try:
            return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except Exception as e:
            raise ValueError(f"Invalid date or time: {e}")

    def make_plot(self):
        """
        Handler for the "Show player activity" button.

        Gets user input, validates it, fetches player activity data from the helpers,
        and displays the plot image. Shows user notifications on errors or empty results.

        Returns
        -------
        None
        """
        nick = self.input_nick.value.strip()
        date = self.convert_datetime()
        self.plot_area.source = ''

        if not nick:
            ui.notify("Please enter a nick!", color="red")
            return

        timestamps = self.helpers.get_player_activity(nick=nick, start_date=date)
        if not timestamps:
            ui.notify(f"No activity found for nick {nick}", color="red")
            return

        img = self.helpers.gui_plot_player_activity(timestamps=timestamps)
        img_b64 = base64.b64encode(img.read()).decode("ascii")
        data_url = f"data:image/png;base64,{img_b64}"
        self.plot_area.source = data_url
