from backend.web_scrapper import WebScrapper

if __name__ == '__main__':
    web_scrapper = WebScrapper()
    # profiles, elapsed_time = web_scrapper.scrap_character_activity()
    # print(profiles)
    # print(elapsed_time)
    profiles = [{'profile': '4797201', 'char': '117571', 'datetime': '2025-06-11 19:25:34'},
                {'profile': '5250610', 'char': '229627', 'datetime': '2025-06-11 19:25:34'}]
    data = web_scrapper.scrap_profile_data(player_activity=profiles)
    print(data)
    for x in data:
        print(x)