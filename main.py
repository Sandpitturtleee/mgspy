from backend.data_collection.web_scrapper import WebScrapper

if __name__ == '__main__':
    web_scrapper = WebScrapper(url="https://www.margonem.pl/stats")
    print(web_scrapper.read_website_content())