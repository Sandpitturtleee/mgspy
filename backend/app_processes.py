import multiprocessing
import time
from multiprocessing import Event

from backend.db_operations import DbOperations
from backend.web_scrapper import WebScrapper


class AppProcesses:
    """
    A class to manage the processes for scraping and saving player activity data.

    Attributes:
    ----------
    url : str
        The URL to scrape data from.
    db_name : str
        The name of the database to store data in.
    scrap_player_activity_interval : int
        The interval (in seconds) between scraping operations.
    save_player_activity_interval : int
        The interval (in seconds) between save operations.
    app_run_time : int
        The total run time (in seconds) for the application.

    Methods:
    -------
    scrap_player_activity(scrapped_player_activity: list[dict], control_event: Event)
        Scrape player activity data from a given URL at specified intervals.

    save_player_activity(scrapped_player_activity: list[dict], control_event: Event)
        Save scraped player activity data into a database at specified intervals.

    process_app()
        Start and manage the scraping and saving processes.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.scrap_player_activity_interval = 60
        self.save_player_activity_interval = 120
        self.app_run_time = 3600

    def scrap_player_activity(self, scrapped_player_activity: list[dict], control_event: Event):
        """
        Scrape player activity data from the web scrapper and append it to the list.

        Parameters:
        ----------
        scrapped_player_activity : list[dict]
            A shared list to store scraped player activity data.
        control_event : Event
            An event to control and terminate the scraping process.

        Returns:
        -------
        None
        """
        interval = self.scrap_player_activity_interval
        web_scrapper = WebScrapper()
        while not control_event.is_set():
            timestamp = time.time()
            activity, elapsed_time = web_scrapper.scrap_character_activity()
            scrapped_player_activity += activity
            print(f"Scrapped data at {time.ctime(timestamp)}")
            if interval - elapsed_time > 0:
                time.sleep(interval - elapsed_time)

    def save_player_activity(self, scrapped_player_activity: list[dict], control_event: Event):
        """
        Save player activity data into a database from the list at specified intervals.

        Parameters:
        ----------
        scrapped_player_activity : list[dict]
            A shared list containing player activity data to be saved.
        control_event : Event
            An event to control and terminate the saving process.

        Returns:
        -------
        None
        """
        interval = self.save_player_activity_interval
        db = DbOperations(db_name=self.db_name)
        connection = db.connect_to_db()
        while not control_event.is_set():
            time.sleep(interval)
            print(f"Saved data at {time.ctime()}")
            db.insert_activity_data(db_connection=connection, player_activity=scrapped_player_activity)
            scrapped_player_activity[:] = []

    def scrap_and_save_profile_data(self):
        """
        Scrapes profile data for unique profiles found in 'activity_data' table and saves them to the database.

        Steps:
        1. Connect to the database using DbOperations.
        2. Retrieve all player activity records from 'activity_data'.
        3. Format activity data into dicts and ensure uniqueness by 'profile'.
        4. Use WebScrapper to scrape profile data for these unique profiles.
        5. Insert the scraped profile data into the 'profile_data' table.

        Returns
        -------
        None
        """
        db = DbOperations(self.db_name)
        web_scrapper = WebScrapper()
        connection = db.connect_to_db()
        player_activity = db.select_data(connection, table='activity_data')
        result = [
            {
                'profile': str(profile),
                'char': str(char),
                'datetime': dt.strftime('%Y-%m-%d %H:%M:%S')
            }
            for profile, char, dt in player_activity
        ]

        unique_profiles = {}
        for entry in result:
            if entry['profile'] not in unique_profiles:
                unique_profiles[entry['profile']] = entry
        unique_player_activity = list(unique_profiles.values())
        profile_data = web_scrapper.scrap_profile_data(player_activity=unique_player_activity)
        db.insert_profile_data(db_connection=connection, profile_data=profile_data)


    def process_app(self):
        """
        Manages and runs the scraping and saving processes for the scraper application.

        The method creates two multiprocessing processes for scraping and saving player activities
        data running in parallel. These processes are controlled to run for a specified time before being terminated.

        Returns:
        -------
        None
        """
        manager = multiprocessing.Manager()
        scrapped_player_activity = manager.list()
        control_event = multiprocessing.Event()

        scrap_player_activity_process = multiprocessing.Process(target=self.scrap_player_activity,
                                                                args=(scrapped_player_activity, control_event))
        save_player_activity_process = multiprocessing.Process(target=self.save_player_activity,
                                                               args=(scrapped_player_activity, control_event))

        # Start the processes
        scrap_player_activity_process.start()
        save_player_activity_process.start()

        # Allow execution for a set time, then stop
        try:
            time.sleep(self.app_run_time)  # Let the processes run for an hour
        finally:
            # Signal processes to stop
            control_event.set()
            scrap_player_activity_process.join()
            save_player_activity_process.join()
            print("Processes terminated.")
