import os
import uuid

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_user_can_register_and_add_todo():
    app_url = os.getenv("APP_URL", "http://proxy")
    selenium_url = os.getenv("SELENIUM_URL", "http://selenium:4444/wd/hub")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(command_executor=selenium_url, options=options)
    wait = WebDriverWait(driver, 20)
    username = f"selenium_{uuid.uuid4().hex[:10]}"
    password = "SeleniumPass123!"
    todo_title = "Selenium UI Test Todo"

    try:
        driver.get(app_url)
        wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "register").click()

        todo_input = wait.until(EC.visibility_of_element_located((By.ID, "new-title")))
        todo_input.send_keys(todo_title)
        driver.find_element(By.ID, "add").click()

        wait.until(lambda browser: todo_title in browser.find_element(By.ID, "todos").text)
        assert todo_title in driver.find_element(By.ID, "todos").text
    finally:
        driver.quit()
