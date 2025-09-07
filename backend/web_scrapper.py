import re
import time
from datetime import datetime
from typing import Tuple, List, Dict, Any

import requests
from bs4 import BeautifulSoup


class WebScrapper:
    """
    A web scraper class for extracting player activity and profile data from the Margonem game website.

    Attributes
    ----------
    stats_url : str
        The main URL to scrape the character activity from.
    profile_url : str
        The base URL used to scrape detailed profile data for each character.

    Methods
    -------
    scrap_character_activity() -> tuple[list[dict], int]
        Scrape the character activity summary from the provided URL.

    scrap_profile_data(player_activity: list[dict]) -> list[dict]
        Scrape detailed profile data for the player activity list.
    """

    def __init__(self):
        """
        Initialize the WebScrapper for Margonem web game.
        """
        self.stats_url = "https://www.margonem.pl/stats"
        self.profile_url = "https://www.margonem.pl/profile/view"

    def scrap_character_activity(self) -> tuple[list[dict[str, str | Any] | dict[str, int | str]], float]:
        """
        Scrape player activity data from the website.

        Returns
        -------
        tuple[list[dict], int]
            A tuple containing:
              - A list of dictionaries, each containing 'profile', 'char', and 'datetime' keys.
              - The elapsed time (in seconds) taken for the request and processing.

        Example dictionary in the returned list:
            {
                'profile': 'user_profile_id',
                'char': 'character_id',
                'datetime': 'YYYY-MM-DD HH:MM:SS'
            }
        """
        player_activity = []
        start_time = time.time()
        try:
            response = requests.get(self.stats_url, timeout=30)
            elapsed_time = time.time() - start_time
            soup = BeautifulSoup(response.text, "html.parser")
            outer_div = soup.find(
                "div", class_="light-brown-box news-container no-footer berufs-popup"
            )
            if not outer_div:
                raise Exception("outer_div not found")
            inner_div = outer_div.find("div", class_="news-body")
            if not inner_div:
                raise Exception("inner_div not found")

            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for a_tag in inner_div.find_all("a", class_="statistics-rank"):
                profile_link = a_tag["href"]

                profile_match = re.search(
                    r"/profile/view,(\d+)#char_(\d+)", profile_link
                )
                if profile_match:
                    profile_number = profile_match.group(1)
                    char_number = profile_match.group(2)

                    player_activity.append(
                        {
                            "profile": profile_number,
                            "char": char_number,
                            "datetime": current_datetime,
                        }
                    )
            if not player_activity:
                player_activity.append(
                    {"profile": 0, "char": 0, "datetime": current_datetime}
                )

        except Exception as e:
            elapsed_time = time.time() - start_time
            print(str(e))
            # return player_activity, elapsed_time
        return player_activity, elapsed_time

    def scrap_profile_data(self, player_activity: list[dict]) -> list[dict]:
        """
        Scrape detailed profile data for players based on an activity list.

        Parameters
        ----------
        player_activity : list[dict]
            A list of dictionaries with keys 'profile' and 'char' describing player activity.

        Returns
        -------
        list[dict]
            A list of dictionaries, each containing profile and character data such as:
                - profile (str): Profile ID
                - char (str): Character ID
                - nick (str): Character nickname
                - lvl (str): Character level
                - world (str): Character world

        Example return value:
            [
                {
                    'profile': '123456',
                    'char': '654321',
                    'nick': 'SomeNick',
                    'lvl': '123',
                    'world': '#berufs'
                },
                ...
            ]
        """
        player_data = []
        for profile_data in player_activity:
            time.sleep(5)
            profile = profile_data.get("profile")
            char = profile_data.get("char")
            if profile and char:
                constructed_url = f"{self.profile_url},{profile}#char_{char},berufs"
                response = requests.get(constructed_url)
                soup = BeautifulSoup(response.text, "html.parser")
                character_list_div = soup.find("div", class_="character-list")
                if character_list_div:
                    for li in character_list_div.find_all("li", class_="char-row"):
                        data_world = li.get("data-world", "")
                        if data_world and data_world.startswith("#berufs"):
                            character_info = {
                                "profile": profile,
                                "char": li.get("data-id", ""),
                                "nick": li.get("data-nick", ""),
                                "lvl": li.get("data-lvl", ""),
                                "world": data_world,
                            }
                            player_data.append(character_info)
        return player_data
