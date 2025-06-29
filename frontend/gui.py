from nicegui import ui
from datetime import datetime
import base64

from frontend.data_collectors import DataCollectors


class Gui:
    """
    A GUI class for displaying player activity plots using NiceGUI.

    This class creates an interactive user interface for querying a player's activity
    data based on nickname input, and displaying the result as a plot image.

    Attributes
    ----------
    input_nick : ui.input
        The input widget for entering the player nickname.
    plot_area : ui.image
        The area where the activity plot image is displayed.
    start_dt : datetime
        The start of the date range for activity plots.
    end_dt : datetime
        The end of the date range for activity plots.
    collector : DataCollectors
        An instance of DataCollectors to fetch and plot player activity data.

    Methods
    -------
    make_plot()
        Collect activity data for the entered nickname and update the plot image area.
    """
    def __init__(self):
        ui.page_title("mgspy")
        with ui.column().classes('w-full items-center justify-center').style('min-height: 100vh'):
            self.input_nick = ui.input('Nick', placeholder='Enter player nick').style('width: 400px; font-size: 1.2rem')
            ui.button('Show Activity', on_click=self.make_plot).props('size=lg')
            self.plot_area = ui.image().style(
                'width: 900px; height: 400px; margin-top: 40px; background: #fafafa; border: 1px solid #ddd;')
        self.start_dt = datetime(2025, 6, 28, 11, 0, 0)
        self.end_dt = datetime(2025, 6, 28, 12, 0, 0)
        self.collector = DataCollectors(start_dt=self.start_dt, end_dt=self.end_dt)

    def make_plot(self):
        """
        Fetch and plot player activity for the nickname entered by the user.

        Collects the input, validates it, fetches activity data, and updates
        the plot area with a dynamically generated activity chart.

        If there is no input or the nickname is not found, displays a notification.

        Returns
        -------
        None
        """
        nick = self.input_nick.value.strip()
        if not nick:
            self.plot_area.source = None
            ui.notify('Please enter a nick!', color='red')
            return
        timestamps = self.collector.get_player_activity(nick=nick)
        if not timestamps:
            self.plot_area.source = None
            ui.notify(f"No activity found for nick {nick}", color='red')
            return
        img = self.collector.gui_plot_player_activity(timestamps=timestamps)
        img_b64 = base64.b64encode(img.read()).decode('ascii')
        data_url = f'data:image/png;base64,{img_b64}'
        self.plot_area.source = data_url

