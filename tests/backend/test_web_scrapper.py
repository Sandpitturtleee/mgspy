import pytest
import re
import time
from datetime import datetime
from unittest.mock import patch, MagicMock
from backend.web_scrapper import WebScrapper

import backend.web_scrapper as ws


@pytest.fixture
def webscraper():
    return WebScrapper()


def test_scrap_character_activity(mocker, activity_html, webscraper,player_activity_test):
    mock_response = MagicMock()
    mock_response.text = activity_html
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


def test_scrap_profile_data_multiple(mocker, webscraper, player_profiles, profile_5111553, profile_973998,player_profiles_test):
    # Patch time.sleep to do nothing
    mocker.patch('time.sleep', return_value=None)
    # Create two different mocked responses
    mock_response1 = MagicMock()
    mock_response1.text = profile_5111553
    mock_response2 = MagicMock()
    mock_response2.text = profile_973998
    # Patch requests.get so each call returns the next response
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
