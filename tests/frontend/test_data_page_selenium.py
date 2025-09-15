from selenium.webdriver.common.by import By
import time

BASE_URL = "http://127.0.0.1:8080"


def test_navbar_links_exist(driver):
    driver.get(BASE_URL)
    navbar_links = driver.find_elements(By.CSS_SELECTOR, "a.text-black")
    assert any("Data" in link.text for link in navbar_links)
    assert any("Activity" in link.text for link in navbar_links)


def test_navigation_to_activity(driver):
    driver.get(BASE_URL)
    navbar_links = driver.find_elements(By.CSS_SELECTOR, "a.text-black")
    activity_link = next(link for link in navbar_links if "Activity" in link.text)
    activity_link.click()
    time.sleep(1)
    assert "activity" in driver.current_url


def test_table_displays_initial_data(driver):
    driver.get(BASE_URL)
    table_rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    assert len(table_rows) > 0


def test_data_input_and_filtering(driver):
    driver.get(BASE_URL)
    input_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter player nick']")
    input_box.clear()
    input_box.send_keys("TEST")

    button = driver.find_element(By.XPATH, "//button[contains(.,'Show player data')]")
    button.click()
    time.sleep(1)

    table_rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    assert len(table_rows) > 0
