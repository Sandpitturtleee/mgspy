from datetime import datetime, timedelta
from io import BytesIO
import matplotlib.pyplot as plt
from backend.db_operations import DbOperations
from typing import Any


class ActivityPageHelpers:
    """
    Helper class for collecting, processing, and visualizing player activity data.

    This class interfaces with a PostgreSQL-backed database to retrieve player activity data
    (timestamps), aggregates that data into intervals, and provides plotting methods for
    display or embedding (via PNG output).

    Attributes
    ----------
    interval_minutes : int
        Minutes per aggregation interval in visualizations (default: 1).
    start_date : datetime
        Start timestamp for analysis range.
    end_date : datetime
        End timestamp for analysis range.
    db_name : str
        Name of the database.
    db : DbOperations
        Instance for database operations.
    connection : Any
        Active database connection.

    Methods
    -------
    get_player_activity(nick: str, start_date: datetime) -> list[datetime] | None
        Retrieves activity timestamps for a player by nickname and date range.
    plot_player_activity(timestamps: list[datetime])
        Plots a bar chart on the screen of activity presence per interval.
    gui_plot_player_activity(timestamps: list[datetime]) -> BytesIO
        Returns a PNG image of the player activity plot, for GUI or web use.
    generate_intervals() -> list[datetime]
        Builds a list of interval boundaries over the selected time range.
    activity_presence_array(intervals: list[datetime], timestamps: list[datetime]) -> list[int]
        Computes array: 1 if player was active in interval, else 0.
    render_bar_chart(interval_labels: list[str], activity_presence: list[int])
        Renders an on-screen bar chart of activity.
    render_bar_chart_to_bytesio(interval_labels: list[str], activity_presence: list[int]) -> BytesIO
        Exports activity bar chart to a BytesIO PNG image object.
    calculate_end_date(start_date: datetime) -> datetime
        Computes the default end of interval window (1 hour ahead).
    """

    def __init__(self):
        """
        Initialize ActivityPageHelpers, allowing customizable intervals and date ranges.

        Database defaults to "mgspy", and the aggregation interval to 1 minute,
        but start and end dates must be set via method calls.
        """
        self.interval_minutes = 1
        self.start_date = None
        self.end_date = None
        self.db_name = "mgspy"
        self.db: DbOperations = DbOperations(db_name=self.db_name)
        self.connection: Any = self.db.connect_to_db()

    def get_player_activity(
        self, nick: str, start_date: datetime
    ) -> list[datetime] | None:
        """
        Retrieve a list of activity timestamp datetimes for a given player, using
        the provided start_date and a computed (+1 hour) end_date.

        Parameters
        ----------
        nick : str
            Nickname of the player whose activity is being queried.
        start_date : datetime
            Start time for the retrieval interval.

        Returns
        -------
        list[datetime] or None
            List of activity datetimes, or None if the player profile is not found.

        Side Effects
        -----------
        Sets self.start_date and self.end_date for future plotting.
        """
        profile_char_rows = self.db.select_data(
            db_connection=self.connection,
            table="profile_data",
            columns="profile, char",
            where_clause="nick = %s",
            params=(nick,),
        )
        if not profile_char_rows:
            print(f"No profile/char found for nick: {nick}")
            return None
        profile, char = profile_char_rows[0]

        where_clause = "profile = %s AND char = %s AND datetime >= %s AND datetime < %s"
        end_date = self.calculate_end_date(start_date=start_date)
        params = (profile, char, start_date, end_date)
        tuples = self.db.select_data(
            db_connection=self.connection,
            table="activity_data",
            columns="profile, char, datetime",
            where_clause=where_clause,
            params=params,
        )
        timestamps = [dt for _, _, dt in tuples]
        self.start_date = start_date
        self.end_date = end_date
        return timestamps

    def plot_player_activity(self, timestamps: list[datetime]):
        """
        Plot a bar chart of player activity within the selected interval window.

        Parameters
        ----------
        timestamps : list[datetime]
            List of datetime objects indicating player activity events.

        Returns
        -------
        None
        """
        intervals = self.generate_intervals()
        activity_presence = self.activity_presence_array(intervals, timestamps)
        interval_labels = [dt.strftime("%H:%M") for dt in intervals[:-1]]
        self.render_bar_chart(interval_labels, activity_presence)

    def gui_plot_player_activity(self, timestamps: list[datetime]) -> BytesIO:
        """
        Prepare the activity plot as a PNG image in a BytesIO object (for use in GUIs).

        Parameters
        ----------
        timestamps : list[datetime]
            Player activity event timestamps to visualize.

        Returns
        -------
        BytesIO
            In-memory PNG chart, ready for embedding in GUI or web applications.
        """
        intervals = self.generate_intervals()
        activity_presence = self.activity_presence_array(intervals, timestamps)
        interval_labels = [dt.strftime("%H:%M") for dt in intervals[:-1]]
        return self.render_bar_chart_to_bytesio(interval_labels, activity_presence)

    def generate_intervals(self) -> list[datetime]:
        """
        Generate boundary datetimes separating each aggregation interval between start_date and end_date.

        Returns
        -------
        list[datetime]
            List of interval "start" boundary datetimes, followed by final end_date.
        """
        intervals = []
        current = self.start_date
        while current < self.end_date:
            intervals.append(current)
            current += timedelta(minutes=self.interval_minutes)
        intervals.append(self.end_date)
        return intervals

    @staticmethod
    def activity_presence_array(
        intervals: list[datetime], timestamps: list[datetime]
    ) -> list[int]:
        """
        Indicate for each interval whether any activity event occurred.

        This generates a binary array (length = len(intervals) - 1), where '1' means
        the user was active in the given interval, and '0' means no activity was detected.

        Parameters
        ----------
        intervals : list[datetime]
            List of datetime interval boundaries.
        timestamps : list[datetime]
            Sorted list of recorded activity event datetimes.

        Returns
        -------
        list[int]
            Binary array of activity presence/absence (1 = present, 0 = absent).
        """
        activity_presence = [0] * (len(intervals) - 1)
        ts_idx = 0
        timestamps = sorted(timestamps)
        for i in range(len(intervals) - 1):
            while (
                ts_idx < len(timestamps)
                and intervals[i] <= timestamps[ts_idx] < intervals[i + 1]
            ):
                activity_presence[i] = 1
                ts_idx += 1
        return activity_presence

    def render_bar_chart(
        self, interval_labels: list[str], activity_presence: list[int]
    ):
        """
        Render an on-screen bar chart (via matplotlib) of activity presence per interval.

        Parameters
        ----------
        interval_labels : list[str]
            Human-readable string labels for each aggregation interval.
        activity_presence : list[int]
            Binary array of activity (output of activity_presence_array).

        Returns
        -------
        None
        """
        plt.figure(figsize=(12, 5))
        plt.bar(interval_labels, activity_presence, width=0.8, align="center")
        plt.xticks(rotation=45)
        plt.yticks([0, 1])
        plt.xlabel("Time interval (minutes)")
        plt.ylabel("Activity presence (0 or 1)")
        plt.title(f"Activity from {self.start_date} to {self.end_date}")
        plt.tight_layout()
        plt.show()

    def render_bar_chart_to_bytesio(
        self, interval_labels: list[str], activity_presence: list[int]
    ) -> BytesIO:
        """
        Create a PNG image in memory of player activity (useful for GUIs or web apps).

        Parameters
        ----------
        interval_labels : list[str]
            Interval string labels.
        activity_presence : list[int]
            Activity binary presence array.

        Returns
        -------
        BytesIO
            PNG image in a BytesIO (ready for GUI/HTML embedding).
        """
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.bar(
            range(len(interval_labels)), activity_presence, width=0.8, align="center"
        )
        ax.set_xticks(range(len(interval_labels)))
        ax.set_xticklabels(interval_labels, rotation=45)
        ax.set_yticks([0, 1])
        ax.set_xlabel("Time interval (minutes)")
        ax.set_ylabel("Activity presence (0 or 1)")
        ax.set_title(f"Activity from {self.start_date} to {self.end_date}")
        plt.tight_layout()
        img = BytesIO()
        plt.savefig(img, format="png", dpi=100)
        plt.close(fig)
        img.seek(0)
        return img

    @staticmethod
    def calculate_end_date(start_date: datetime) -> datetime:
        """
        Given a start datetime, return an end datetime exactly one hour later.

        Parameters
        ----------
        start_date : datetime
            Beginning of analysis window.

        Returns
        -------
        datetime
            End of analysis window (start_date + 1 hour).
        """
        return start_date + timedelta(hours=1)
