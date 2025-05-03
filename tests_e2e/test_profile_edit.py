import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def test_edit_profile(driver):
    driver.get("http://127.0.0.1:5000/login")

    # Login
    driver.find_element(By.ID, "username").send_keys("dj")
    driver.find_element(By.ID, "password").send_keys("admin6")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    # Go to profile page
    driver.get("http://127.0.0.1:5000/user/2")

    # Click "Edit Profile"
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.toggle"))
    ).click()

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "edit-form"))
    )

    # Fill new username
    username_input = driver.find_element(By.ID, "username")
    username_input.clear()
    username_input.send_keys("dj_updated")

    # Submit form
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(1)  # Optional: Replace with explicit wait if needed

    assert "User updated successfully" in driver.page_source
