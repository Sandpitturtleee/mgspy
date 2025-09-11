import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def live_server_url():
    return 'http://127.0.0.1:8080/'


@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_nick_blank_displays_error(live_server_url, browser):
    browser.get(live_server_url)
    button = browser.find_element(By.TAG_NAME, "button")
    button.click()
    notif = WebDriverWait(browser, 3).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".q-notification__message"))
    )
    assert "Please enter a nick" in notif.text


def test_nick_not_found_displays_error(live_server_url, browser):
    browser.get(live_server_url)
    input_elem = browser.find_element(By.TAG_NAME, "input")
    input_elem.send_keys("DefinitelyFakeNick")
    button = browser.find_element(By.TAG_NAME, "button")
    button.click()
    notif = WebDriverWait(browser, 3).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".q-notification__message"))
    )
    assert "No activity found for nick DefinitelyFakeNick" in notif.text
