import requests
from bs4 import BeautifulSoup


class WebScrapper:
    def __init__(self, url):
        self.url = url

    def read_website_content(self):
        # Send a GET request to fetch the HTML source
        response = requests.get(self.url)

        # Print the HTML source
        soup = BeautifulSoup(response.text, 'html.parser')
        outer_div = soup.find('div', class_='light-brown-box news-container no-footer berufs-popup')
        inner_div = outer_div.find('div', class_='news-body')
        print(inner_div)
        profiles = []
        for a_tag in inner_div.find_all('a', class_='statistics-rank'):
            profile_link = a_tag['href']
            nickname = a_tag.get_text(strip=True)
            profiles.append({'profile': profile_link, 'nickname': nickname})

        # Example output
        for profile in profiles:
            print(profile)
        return response
