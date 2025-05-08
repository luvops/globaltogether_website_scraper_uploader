import time
from selenium.webdriver.common.by import By
from config import TARGET_LOGIN_URL

# Login to the admin page
def admin_login(driver, username, password):
    driver.get(TARGET_LOGIN_URL)
    time.sleep(1)

    driver.find_element(By.NAME, "login_id").send_keys(username)
    driver.find_element(By.NAME, "login_pw").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)