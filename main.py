from backend.data_collection.web_scrapper import WebScrapper

if __name__ == '__main__':
    web_scrapper = WebScrapper(url="https://www.margonem.pl/stats")
    profiles = (web_scrapper.scrap_character_activity())
    print(profiles)
    profiles = [{'profile': '4797201', 'char': '117571', 'datetime': '2025-06-11 19:25:34'}]
    data = web_scrapper.get_profile_data(profile_data_list=profiles)
    for x in data:
        print(x)