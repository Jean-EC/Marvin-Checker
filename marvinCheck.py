from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as GeckoDriverService
from selenium.common.exceptions import NoSuchElementException
import os

url = "https://my.epitech.eu/"

filename = "website_content.txt"

driver_path = "/usr/bin/geckodriver"

options = Options()
options.profile = "/home/khara/.mozilla/firefox/aqoh1xti.default-release"
service_args = ["--marionette-port", "2828"]
service = GeckoDriverService(executable_path=driver_path, log_path=os.path.devnull, service_args=service_args)
driver = webdriver.Firefox(options=options, service=service)

driver.get(url)
driver.implicitly_wait(10)



try:
    login_button = driver.find_element(By.CLASS_NAME, "mdl-button__ripple-container")
    login_url = login_button.get_attribute("href")
except NoSuchElementException:
    login_button = None
    login_url = None

if login_url is not None:
    print("Navigating to", login_url)
    driver.get(login_url)

    driver.implicitly_wait(10)

    if url in driver.current_url:
        print("Already logged in.")
else:
    print("No login button found. Proceeding to get website content.")

main_element = driver.find_element(By.TAG_NAME, "main")
content = main_element.get_attribute("innerHTML")

if os.path.exists(filename):
    with open(filename, "r") as f:
        old_content = f.read()

    if old_content == content:
        print("Website content has not changed.")
    else:
        print("Website content has changed.")
        with open(filename, "w") as f:
            f.write(content)
else:
    print("Website content not found. Creating file.")
    with open(filename, "w") as f:
        f.write(content)

driver.quit()
