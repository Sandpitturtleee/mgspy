from datetime import datetime, timedelta
from io import BytesIO

import matplotlib.pyplot as plt

from backend.db_operations import DbOperations


class DataCollectors:
    """
    A class for collecting and visualizing player activity data from the database.

    Attributes
    ----------
    db_name : str
        Name of the database to use for queries (default: "mgspy").
    interval_minutes : int
        The interval in minutes for aggregating activity data during plotting.

    Methods
    -------
    get_player_activity(nick: str, start_dt: datetime, end_dt: datetime) -> list[datetime]
        Retrieves player activity timestamp data for a given user nickname within a time range.

    plot_player_activity(start_dt: datetime, end_dt: datetime, timestamps: list[datetime])
        Plots a bar chart of player activity counts across time intervals.

    gui_plot_player_activity(start_dt: datetime, end_dt: datetime, timestamps: list[datetime]) -> BytesIO
        Prepares player activity chart as a PNG image (for GUI embedding/use).
    """

    def __init__(self, start_dt, end_dt):
        """
        Initialize the data collector with a time range.

        Parameters
        ----------
        start_dt : datetime
            The start of the time range for activity data analysis.
        end_dt : datetime
            The end of the time range for activity data analysis.
        """
        self.db_name = "mgspy"
        self.interval_minutes = 1
        self.start_dt = start_dt
        self.end_dt = end_dt

    def get_player_activity(self, nick: str) -> list[datetime] | None:
        """
        Retrieve player activity timestamps for a specific user (by nick) between two dates.

        Parameters
        ----------
        nick : str
            The nickname of the player.

        Returns
        -------
        list[datetime]
            A list of datetime objects corresponding to the player's activity timestamps
            within the specified time range.
            Returns None if profile/char is not found for the given nick.
        """
        db = DbOperations(db_name=self.db_name)
        connection = db.connect_to_db()

        # 1: Look up profile and char by nick in profile_data
        profile_char_rows = db.select_data(
            db_connection=connection,
            table="profile_data",
            columns="profile, char",
            where_clause="nick = %s",
            params=(nick,),
        )

        if not profile_char_rows:
            print(f"No profile/char found for nick: {nick}")
            return
        profile, char = profile_char_rows[0]

        # 2: Get activity records for this profile/char in the given interval
        where_clause = "profile = %s AND char = %s AND datetime >= %s AND datetime < %s"
        params = (profile, char, self.start_dt, self.end_dt)
        tuples = db.select_data(
            db_connection=connection,
            table="activity_data",
            columns="profile, char, datetime",
            where_clause=where_clause,
            params=params,
        )
        timestamps = [dt for _, _, dt in tuples]
        return timestamps

    def plot_player_activity(self, timestamps: list[datetime]):
        """
        Plot player activity as a bar chart of counts per interval between start_dt and end_dt.

        Parameters
        ----------
        timestamps : list[datetime]
            List of player activity timestamps, typically as returned by get_player_activity.

        Returns
        -------
        None
        """
        intervals = []
        current = self.start_dt
        while current < self.end_dt:
            intervals.append(current)
            current += timedelta(minutes=self.interval_minutes)
        intervals.append(self.end_dt)

        activity_presence = [0] * (len(intervals) - 1)
        ts_idx = 0
        timestamps.sort()
        for i in range(len(intervals) - 1):
            while (
                ts_idx < len(timestamps)
                and intervals[i] <= timestamps[ts_idx] < intervals[i + 1]
            ):
                activity_presence[i] = 1
                ts_idx += 1

        interval_labels = [dt.strftime("%H:%M") for dt in intervals[:-1]]
        plt.figure(figsize=(12, 5))
        plt.bar(interval_labels, activity_presence, width=0.8, align="center")
        plt.xticks(rotation=45)
        plt.yticks([0, 1])
        plt.xlabel("Time interval (minutes)")
        plt.ylabel("Activity presence (0 or 1)")
        plt.title(f"Activity from {self.start_dt} to {self.end_dt}")
        plt.tight_layout()
        plt.show()

    def gui_plot_player_activity(self, timestamps: list[datetime]) -> BytesIO:
        """
        Plot player activity as a bar chart and save as a PNG image in a BytesIO object (for GUI use).

        Parameters
        ----------
        timestamps : list[datetime]
            List of player activity timestamps, typically as returned by get_player_activity.

        Returns
        -------
        BytesIO
            An in-memory file-like object containing the PNG image data of the chart.
        """
        intervals = []
        current = self.start_dt
        while current < self.end_dt:
            intervals.append(current)
            current += timedelta(minutes=self.interval_minutes)
        intervals.append(self.end_dt)

        activity_presence = [0] * (len(intervals) - 1)
        ts_idx = 0
        timestamps.sort()
        for i in range(len(intervals) - 1):
            while (
                ts_idx < len(timestamps)
                and intervals[i] <= timestamps[ts_idx] < intervals[i + 1]
            ):
                activity_presence[i] = 1
                ts_idx += 1

        interval_labels = [dt.strftime("%H:%M") for dt in intervals[:-1]]
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.bar(
            range(len(interval_labels)), activity_presence, width=0.8, align="center"
        )

        ax.set_xticks(range(len(interval_labels)))
        ax.set_xticklabels(interval_labels, rotation=45)
        ax.set_yticks([0, 1])
        ax.set_xlabel("Time interval (minutes)")
        ax.set_ylabel("Activity presence (0 or 1)")
        ax.set_title(f"Activity from {self.start_dt} to {self.end_dt}")

        plt.tight_layout()
        img = BytesIO()
        plt.savefig(img, format="png", dpi=100)
        plt.close(fig)
        img.seek(0)
        return img
