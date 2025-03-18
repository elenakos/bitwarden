
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class AppiumUtil:

    def __init__(self, driver):
        self.driver = driver

    def find_element_by_resource_id(self, test_tag: str) -> WebElement:
        return self.driver.find_element(by=AppiumBy.XPATH, value=f'//*[@resource-id="{test_tag}"]')

    def find_element_by_text(self, text: str) -> WebElement:
        return self.driver.find_element(by=AppiumBy.XPATH, value='//*[@resource-id="{text}"]')

    def wait_for_element_by_text(self, text: str, wait_timeout = 10) -> WebElement | None:
        locator = (AppiumBy.XPATH, f'//*[@text="{text}"]')
        try:
            element = WebDriverWait(self.driver, wait_timeout).until(
                EC.presence_of_element_located(locator=locator)
            )
            return element
        except TimeoutException:
            print("Timeout while waiting for element to be displayed")
        return None

    def wait_for_element_by_resource_id(self, text: str, wait_timeout = 10) -> WebElement | None:
        locator = (AppiumBy.XPATH, f'//*[@resource-id="{text}"]')
        try:
            element = WebDriverWait(self.driver, wait_timeout).until(
                EC.presence_of_element_located(locator=locator)
            )
            return element
        except TimeoutException:
            print("Timeout while waiting for element to be displayed")
        return None


    def print_page_source(self):
        page_source = self.driver.page_source
        print(page_source)
