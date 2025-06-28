import multiprocessing
import time

from backend.db_operations import DbOperations
from backend.web_scrapper import WebScrapper


class AppProcesses:
    def data_producer1(self,profiles, control_event):
        # Simulate data production every minute
        web_scrapper = WebScrapper(url="https://www.margonem.pl/stats")
        while not control_event.is_set():
            timestamp = time.time()
            #shared_dict[timestamp] = {"value": f"SampleData_{timestamp}"}
            #print(shared_dict)
            profiles, elapsed_time = web_scrapper.scrap_character_activity()
            print(f"Scrapped data at {time.ctime(timestamp)}")
            print(profiles)
            print(elapsed_time)
            if 60-elapsed_time > 0:
                time.sleep(60-elapsed_time)


    def data_consumer1(self,profiles, control_event):
        # Simulate reading from the dictionary every 10 minutes and saving to a "database"
        while not control_event.is_set():
            time.sleep(30)  # Wait for 10 minutes
            # Mimic saving to a database
            print(f"Consuming data at {time.ctime()}")
            all_data = list(profiles.items())
            for timestamp, data in all_data:
                print(f"Saving data: {data}")
                print(profiles)
                del profiles[timestamp]
                print(profiles)

    def data_producer(self,all_profiles, control_event):
        web_scrapper = WebScrapper(url="https://www.margonem.pl/stats")
        while not control_event.is_set():
            timestamp = time.time()
            profiles, elapsed_time = web_scrapper.scrap_character_activity()
            all_profiles += profiles
            print(f"Scrapped data at {time.ctime(timestamp)}")
            if 60-elapsed_time > 0:
                time.sleep(60-elapsed_time)

    def data_consumer(self,all_profiles, control_event):
        db = DbOperations()
        connection = db.connect_to_db("mgspy")
        while not control_event.is_set():
            time.sleep(600)  # Wait for 10 minutes
            # Mimic saving to a database
            print(f"Saved data at {time.ctime()}")
            db.insert_data(connection, all_profiles)
            all_profiles[:] = []




    def process_app(self):
        manager = multiprocessing.Manager()
        all_profiles = manager.list()  # Shared dictionary for data exchange
        control_event = multiprocessing.Event()

        producer_process = multiprocessing.Process(target=self.data_producer, args=(all_profiles, control_event))
        consumer_process = multiprocessing.Process(target=self.data_consumer, args=(all_profiles, control_event))

        # Start the processes
        producer_process.start()
        consumer_process.start()

        # Allow execution for a set time, then stop
        try:
            time.sleep(3840)  # Let the processes run for an hour
        finally:
            # Signal processes to stop
            control_event.set()
            producer_process.join()
            consumer_process.join()
            print("Processes terminated.")