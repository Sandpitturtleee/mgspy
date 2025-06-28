import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


class WebScrapper:
    def __init__(self, url):
        self.url = url

    def scrap_character_activity1(self):
        # Send a GET request to fetch the HTML source
        response = requests.get(self.url)

        # Parse the HTML source
        soup = BeautifulSoup(response.text, 'html.parser')
        outer_div = soup.find('div', class_='light-brown-box news-container no-footer berufs-popup')
        inner_div = outer_div.find('div', class_='news-body')

        profiles = []
        for a_tag in inner_div.find_all('a', class_='statistics-rank'):
            profile_link = a_tag['href']
            nickname = a_tag.get_text(strip=True)

            # Use regular expression to extract profile number and char number
            profile_match = re.search(r"/profile/view,(\d+)#char_(\d+)", profile_link)
            if profile_match:
                profile_number = profile_match.group(1)
                char_number = profile_match.group(2)

                # Get current date and time
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                profiles.append({
                    'profile': profile_number,
                    'char': char_number,
                    'datetime': current_datetime
                })
        return profiles

    def scrap_character_activity(self):
        profiles = []

        start_time = time.time()  # Start timing
        elapsed_time = 0
        try:
            # Send a GET request to fetch the HTML source
            response = requests.get(self.url, timeout=30)  # Add timeout here
            elapsed_time = time.time() - start_time  # End timing here (success)

            # Parse the HTML source
            soup = BeautifulSoup(response.text, 'html.parser')
            outer_div = soup.find('div', class_='light-brown-box news-container no-footer berufs-popup')
            if not outer_div:
                raise Exception("outer_div not found")
            inner_div = outer_div.find('div', class_='news-body')
            if not inner_div:
                raise Exception("inner_div not found")

            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for a_tag in inner_div.find_all('a', class_='statistics-rank'):
                profile_link = a_tag['href']

                # Use regular expression to extract profile number and char number
                profile_match = re.search(r"/profile/view,(\d+)#char_(\d+)", profile_link)
                if profile_match:
                    profile_number = profile_match.group(1)
                    char_number = profile_match.group(2)

                    profiles.append({
                        'profile': profile_number,
                        'char': char_number,
                        'datetime': current_datetime
                    })
            if not profiles:  # If parsing succeeded but no profiles found, also treat as failure if you want
                profiles.append({
                    'profile': 0,
                    'char': 0,
                    'datetime': current_datetime
                })

        except Exception as e:
            elapsed_time = time.time() - start_time  # End timing here (success)
            print(str(e))
            return profiles, elapsed_time
        return profiles, elapsed_time

    def get_profile_data(self, profile_data_list):
        base_url = "https://www.margonem.pl/profile/view"
        all_characters = []

        for profile_data in profile_data_list:
            profile = profile_data.get('profile')
            char = profile_data.get('char')

            if profile and char:
                constructed_url = f"{base_url},{profile}#char_{char},berufs"
                # Send a GET request to fetch the HTML source
                response = requests.get(constructed_url)

                # Parse the HTML source
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find the div with class 'character-list'
                character_list_div = soup.find('div', class_='character-list')

                # Extract all list elements with data-world matching '#xxx'
                if character_list_div:
                    for li in character_list_div.find_all('li', class_='char-row'):
                        data_world = li.get('data-world', '')
                        if data_world and data_world.startswith('#berufs'):
                            character_info = {
                                'profile': profile,
                                'char': li.get('data-id', ''),
                                'nick': li.get('data-nick', ''),
                                'lvl': li.get('data-lvl', ''),
                                'world': data_world,
                            }
                            all_characters.append(character_info)

        return all_characters
