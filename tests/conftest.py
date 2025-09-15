import json
import pytest
import os
from io import BytesIO
from selenium import webdriver

DATA_PATH = os.path.join(os.path.dirname(__file__), "data")


def load_json(filename):
    with open(os.path.join(DATA_PATH, filename), encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def player_activity_test():
    return load_json("player_activity_test.json")


@pytest.fixture
def player_profiles_test():
    return load_json("player_profiles_test.json")


@pytest.fixture
def player_activity_test_db():
    return load_json("player_activity_test_db.json")


@pytest.fixture
def player_profiles_test_db():
    return load_json("player_profiles_test_db.json")


@pytest.fixture
def player_activity_test_short():
    return load_json("player_activity_test_short.json")


@pytest.fixture
def activity_html_result():
    return load_json("activity_html_result.json")


@pytest.fixture
def non_unique_profiles():
    return load_json("non_unique_profiles.json")


@pytest.fixture
def unique_profiles():
    return load_json("unique_profiles.json")


@pytest.fixture
def activity_html():
    file_path = os.path.join(DATA_PATH, "activity.html")
    with open(file_path, encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def empty_activity_html():
    file_path = os.path.join(DATA_PATH, "empty_activity.html")
    with open(file_path, encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def player_profiles():
    return [{"profile": "5111553", "char": "155755"}, {"profile": "973998", "char": "245184"}]


@pytest.fixture
def profile_5111553():
    file_path = os.path.join(DATA_PATH, "5111553_profile.html")
    with open(file_path, encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def profile_973998():
    file_path = os.path.join(DATA_PATH, "973998_profile.html")
    with open(file_path, encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def img():
    return BytesIO(b'12345678')


@pytest.fixture
def driver():
    # Change to webdriver.Firefox() if you prefer Firefox
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    yield driver
    driver.quit()
