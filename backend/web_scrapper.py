import re
import time
from datetime import datetime
from typing import Tuple, List, Dict, Any
import requests
from bs4 import BeautifulSoup


class WebScrapper:
    def __init__(self):
        self.stats_url = "https://www.margonem.pl/stats"
        self.profile_url = "https://www.margonem.pl/profile/view"

    @staticmethod
    def get_soup(url: str) -> BeautifulSoup:
        response = requests.get(url, timeout=30)
        return BeautifulSoup(response.text, "html.parser")

    @staticmethod
    def get_now() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def parse_profile_char_from_link(link: str) -> Tuple[str, str] | None:
        match = re.search(r"/profile/view,(\d+)#char_(\d+)", link)
        if match:
            return match.group(1), match.group(2)
        return None

    @staticmethod
    def get_stats_inner_div(soup: BeautifulSoup) -> BeautifulSoup | None:
        outer_div = soup.find("div", class_="light-brown-box news-container no-footer berufs-popup")
        if outer_div:
            return outer_div.find("div", class_="news-body")
        return None

    def construct_profile_url(self, profile: str, char: str) -> str:
        return f"{self.profile_url},{profile}#char_{char},berufs"

    def extract_player_activity_from_inner_div(self, inner_div: BeautifulSoup) -> List[Dict[str, Any]]:
        player_activity = []
        current_datetime = self.get_now()
        for a_tag in inner_div.find_all("a", class_="statistics-rank"):
            profile_info = self.parse_profile_char_from_link(a_tag["href"])
            if profile_info:
                profile_number, char_number = profile_info
                player_activity.append({
                    "profile": profile_number,
                    "char": char_number,
                    "datetime": current_datetime,
                })
        return player_activity

    def scrap_character_activity(self) -> Tuple[List[Dict[str, Any]], float]:
        player_activity = []
        start_time = time.time()
        try:
            soup = self.get_soup(self.stats_url)
            inner_div = self.get_stats_inner_div(soup)
            if not inner_div:
                raise Exception("Could not find the required 'news-body' div on the page.")
            player_activity = self.extract_player_activity_from_inner_div(inner_div)
            if not player_activity:
                player_activity.append({"profile": 0, "char": 0, "datetime": self.get_now()})
            elapsed_time = time.time() - start_time
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(str(e))
        return player_activity, elapsed_time

    @staticmethod
    def extract_characters_from_profile(soup: BeautifulSoup, profile: str) -> List[Dict[str, Any]]:
        player_data = []
        character_list_div = soup.find("div", class_="character-list")
        if character_list_div:
            for li in character_list_div.find_all("li", class_="char-row"):
                data_world = li.get("data-world", "")
                if data_world.startswith("#berufs"):
                    player_data.append({
                        "profile": profile,
                        "char": li.get("data-id", ""),
                        "nick": li.get("data-nick", ""),
                        "lvl": li.get("data-lvl", ""),
                        "world": data_world,
                    })
        return player_data

    def scrap_profile_data(self, player_activity: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        player_data = []
        for activity in player_activity:
            time.sleep(5)
            profile = activity.get("profile")
            char = activity.get("char")
            if profile and char:
                url = self.construct_profile_url(profile, char)
                soup = self.get_soup(url)
                player_data.extend(self.extract_characters_from_profile(soup, profile))
        return player_data
