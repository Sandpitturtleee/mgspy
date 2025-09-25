import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

BASE_URL = "http://127.0.0.1:8080/activity"


def clear_input(field):
    field.click()
    field.send_keys(Keys.COMMAND + "a")
    field.send_keys(Keys.BACKSPACE)


def test_activity_page_elements_exist(driver):
    driver.get(BASE_URL)
    input_nick = driver.find_element(
        By.CSS_SELECTOR, "input[placeholder='Enter player nick']"
    )
    start_date = driver.find_element(By.CSS_SELECTOR, "input[placeholder='YYYY-MM-DD']")
    start_time = driver.find_element(By.CSS_SELECTOR, "input[placeholder='HH:MM']")
    button = driver.find_element(
        By.XPATH, "//button[contains(.,'Show player activity')]"
    )
    assert input_nick and start_date and start_time and button


def test_navigation_to_data(driver):
    driver.get(BASE_URL)
    navbar_links = driver.find_elements(By.CSS_SELECTOR, "a.text-black")
    activity_link = next(link for link in navbar_links if "Data" in link.text)
    activity_link.click()
    time.sleep(1)
    assert "/" in driver.current_url


def test_activity_page_no_nick_notification(driver):
    driver.get(BASE_URL)
    button = driver.find_element(
        By.XPATH, "//button[contains(.,'Show player activity')]"
    )
    button.click()
    time.sleep(1)
    toast = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Please enter a nick')]")
        )
    )

    assert "Please enter a nick" in toast.text


def test_activity_page_with_valid_nick(driver):
    driver.get(BASE_URL)
    nick = driver.find_element(
        By.CSS_SELECTOR, "input[placeholder='Enter player nick']"
    )
    clear_input(nick)
    nick.send_keys("Cycu Dzik")

    date = driver.find_element(By.CSS_SELECTOR, "input[placeholder='YYYY-MM-DD']")
    clear_input(date)
    date.send_keys("2025-06-28")

    time_field = driver.find_element(By.CSS_SELECTOR, "input[placeholder='HH:MM']")
    clear_input(time_field)
    time_field.send_keys("11:00")
    driver.find_element(
        By.XPATH, "//button[contains(.,'Show player activity')]"
    ).click()

    time.sleep(1)
    img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "img[src^='data:image']"))
    )
    img_src = img.get_attribute("src")
    assert img_src and img_src.startswith("data:image/png;base64")


def test_activity_page_valid_nick_wrong_date(driver):
    driver.get(BASE_URL)
    nick = driver.find_element(
        By.CSS_SELECTOR, "input[placeholder='Enter player nick']"
    )
    clear_input(nick)
    nick.send_keys("Cycu Dzik")

    date = driver.find_element(By.CSS_SELECTOR, "input[placeholder='YYYY-MM-DD']")
    clear_input(date)
    date.send_keys("2026-06-28")

    time_field = driver.find_element(By.CSS_SELECTOR, "input[placeholder='HH:MM']")
    clear_input(time_field)
    time_field.send_keys("11:00")

    driver.find_element(
        By.XPATH, "//button[contains(.,'Show player activity')]"
    ).click()

    time.sleep(1)
    toast = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'No activity found for nick')]")
        )
    )
    assert "No activity found for nick" in toast.text


def test_activity_page_nonexistent_nick(driver):
    driver.get(BASE_URL)
    nick = driver.find_element(
        By.CSS_SELECTOR, "input[placeholder='Enter player nick']"
    )
    clear_input(nick)
    nick.send_keys("TEST")
    driver.find_element(
        By.XPATH, "//button[contains(.,'Show player activity')]"
    ).click()

    time.sleep(1)
    toast = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'No activity found for nick')]")
        )
    )
    assert "No activity found for nick" in toast.text
