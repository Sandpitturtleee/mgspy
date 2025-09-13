import pytest
from datetime import datetime
from unittest.mock import MagicMock
from backend.web_scrapper import WebScrapper
from bs4 import BeautifulSoup

import backend.web_scrapper as ws


@pytest.fixture
def webscraper():
    return WebScrapper()


def test_scrap_character_activity(mocker, activity_html, webscraper, player_activity_test):
    mock_response = MagicMock()
    mock_response.text = activity_html
    mock_response.content = activity_html.encode()
    mocker.patch('requests.get', return_value=mock_response)
    mocker.patch('time.time', side_effect=[1000, 1001])
    mocker.patch('backend.web_scrapper.datetime', autospec=True)
    ws.datetime.now.return_value = datetime(2025, 1, 1, 12, 0, 0)
    player_activity, elapsed = webscraper.scrap_character_activity()
    assert elapsed == 1
    assert player_activity == player_activity_test


def test_scrap_character_activity_empty(mocker, empty_activity_html, webscraper):
    mock_response = MagicMock()
    mock_response.text = empty_activity_html
    mock_response.content = empty_activity_html.encode()
    mocker.patch('requests.get', return_value=mock_response)
    mocker.patch('time.time', side_effect=[1000, 1001])
    mocker.patch('backend.web_scrapper.datetime', autospec=True)
    ws.datetime.now.return_value = datetime(2025, 1, 1, 12, 0, 0)
    player_activity, elapsed = webscraper.scrap_character_activity()
    assert elapsed == 1
    assert player_activity == [{
        "profile": 0,
        "char": 0,
        "datetime": "2025-01-01 12:00:00"
    }]


def test_scrap_profile_data_multiple(mocker, webscraper, player_profiles, profile_5111553, profile_973998, player_profiles_test):
    mocker.patch('time.sleep', return_value=None)
    mock_response1 = MagicMock()
    mock_response1.text = profile_5111553
    mock_response1.content = profile_5111553.encode()
    mock_response2 = MagicMock()
    mock_response2.text = profile_973998
    mock_response2.content = profile_973998.encode()
    mocker.patch('requests.get', side_effect=[mock_response1, mock_response2])
    result = webscraper.scrap_profile_data(player_profiles)
    assert result == player_profiles_test


def test_scrap_character_activity_real_response(webscraper):
    player_activity, elapsed_time = webscraper.scrap_character_activity()
    assert isinstance(player_activity, list)
    assert isinstance(elapsed_time, float)
    assert len(player_activity) >= 1
    first = player_activity[0]
    assert "profile" in first
    assert "char" in first
    assert "datetime" in first


def test_scrap_profile_data_real_response(webscraper, player_profiles):
    result = webscraper.scrap_profile_data(player_profiles)
    assert isinstance(result, list)
    if result:
        first = result[0]
        assert isinstance(first, dict)
        for k in ("profile", "char", "nick", "lvl", "world"):
            assert k in first


def test_parse_profile_char_from_link(webscraper):
    link = "/profile/view,5111553#char_142716"
    result = webscraper.parse_profile_char_from_link(link)
    assert result == ("5111553", "142716")
    assert webscraper.parse_profile_char_from_link("invalid_link") is None


def test_get_stats_inner_div(activity_html, webscraper):
    soup = BeautifulSoup(activity_html, "html.parser")
    inner = webscraper.get_stats_inner_div(soup)
    assert inner is not None
    assert inner.find("a", class_="statistics-rank") is not None
    soup = BeautifulSoup("<div></div>", "html.parser")
    assert webscraper.get_stats_inner_div(soup) is None


def test_construct_profile_url(webscraper):
    assert webscraper.construct_profile_url("5111553", "142716") \
           == "https://www.margonem.pl/profile/view,5111553#char_142716,berufs"


def test_extract_player_activity_from_inner_div(activity_html, webscraper, mocker, activity_html_result):
    soup = BeautifulSoup(activity_html, "html.parser")
    inner = webscraper.get_stats_inner_div(soup)
    mocker.patch.object(WebScrapper, "get_now", return_value="2025-01-01 12:00:00")
    act = webscraper.extract_player_activity_from_inner_div(inner)
    assert act == activity_html_result


def test_extract_characters_from_profiles(profile_5111553, profile_973998, webscraper, player_profiles_test):
    soup = BeautifulSoup(profile_5111553, "html.parser")
    result1 = webscraper.extract_characters_from_profile(soup, "5111553")
    soup = BeautifulSoup(profile_973998, "html.parser")
    result2 = webscraper.extract_characters_from_profile(soup, "973998")
    result = result1 + result2
    assert isinstance(result, list)
    assert result == player_profiles_test
