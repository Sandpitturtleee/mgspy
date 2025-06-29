from backend.db_operations import DbOperations
from backend.web_scrapper import WebScrapper

if __name__ == '__main__':
    web_scrapper = WebScrapper()
    # profiles, elapsed_time = web_scrapper.scrap_character_activity()
    # print(profiles)
    # print(elapsed_time)
    profiles = [{'profile': '4797201', 'char': '117571', 'datetime': '2025-06-11 19:25:34'},
                {'profile': '5250610', 'char': '229627', 'datetime': '2025-06-11 19:25:34'},
                {'profile': '4797201', 'char': '117571', 'datetime': '2025-06-11 19:25:34'}]

    # # Keep only the first occurrence for each profile
    # unique_profiles = {}
    # for entry in profiles:
    #     if entry['profile'] not in unique_profiles:
    #         unique_profiles[entry['profile']] = entry
    # result = list(unique_profiles.values())
    # print(result)
    #
    # data = web_scrapper.scrap_profile_data(player_activity=profiles)
    #
    # db = DbOperations(db_name='mgspy')
    # connection = db.connect_to_db()
    # data = []
    # db.insert_profile_data(db_connection=connection, profile_data=data)
    # print(data)
    # for x in data:
    #     print(x)