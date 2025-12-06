import platform
import time

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


operating_system = platform.platform()

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--start-maximized')
if 'Windows' not in operating_system:
    chrome_options.add_argument('--headless')


class Browser:
    browser, service = None, None

    def __init__(self):
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def click_button(self, by: By, id: str):
        button = self.browser.find_element(by=by, value=id)
        if button is not None:
            try:
                button.click()
            except ElementNotInteractableException:
                print('This is not a clickable button')
                return
        else:
            print('Button not found')
        time.sleep(1)

    def delete_element(self, by: By, id: str):
        try:
            element = self.browser.find_element(by=by, value=id)
        except NoSuchElementException:
            return None
        else:
            self.browser.execute_script(
                """
                var element = arguments[0];
                element.remove();
                """,
                element,
            )
            return True

    def get_element(self, by: By, id: str):
        try:
            el = self.browser.find_element(by=by, value=id)
        except NoSuchElementException:
            return None
        else:
            return el

    def open_page(self, url: str):
        self.browser.get(url)

    def quit(self):
        self.browser.quit()

    def sleep(self, timeout: int):
        time.sleep(timeout)
