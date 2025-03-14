import unittest
from asyncio import timeout
from time import sleep

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

from appium.webdriver.webelement import WebElement
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import Appium UiAutomator2 driver for Android platforms (AppiumOptions)
from appium.options.android import UiAutomator2Options

from ObjectModel.signin import SignIn
from ObjectModel.Helpers.appium_util import AppiumUtil
from Utilities.properties import Properties
from TestSetup import BitwardenTestSetup

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.test_config = BitwardenTestSetup()
        self.host = self.test_config.HOST
        self.capabilities = {}
        self.capabilities['platformName'] =  self.test_config.PLATFORM_NAME
        self.capabilities['automationName'] = self.test_config.AUTOMATION_NAME
        self.capabilities['deviceName'] = self.test_config.DEVICE_NAME
        self.capabilities['appPackage'] = self.test_config.APP_PACKAGE
        self.capabilities['appActivity'] = self.test_config.APP_ACTIVITY
        self.capabilities['language'] =  self.test_config.LANGUAGE
        self.capabilities['locale'] = self.test_config.LOCALE
        self.capabilities['noReset'] = self.test_config.NoRESET

        # Converts capabilities to AppiumOptions instance
        self.capabilities_options = UiAutomator2Options().load_capabilities(self.capabilities)
        self.driver = webdriver.Remote(command_executor=self.host, options=self.capabilities_options)
        self.utilities = AppiumUtil(self.driver)
        self.properties = Properties()
        self.signin_page = SignIn(self.driver, self, self.properties.get_properties())

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_verify_login_page(self):
        self.assertTrue(self.signin_page.is_login_page_displayed())
        # Printing page source for debugging
        self.utilities.print_page_source()

    @unittest.skip("kipping this test - no hosted environment")
    def test_login_hosted(self):
        print("*** TC: Login to a hosted environment")
        self.assertTrue(self.signin_page.is_login_page_displayed())
        self.signin_page.configure_self_hosted()
        self.signin_page.submit_email_and_password()
        my_vault_page = self.utilities.wait_for_element_by_text("My vault")
        self.assertTrue(my_vault_page.is_displayed())

    @unittest.skip("Skipping this test - use correct ID/password")
    def test_login_usa(self):
        print("*** TC: Login to US environment")
        self.assertTrue(self.signin_page.is_login_page_displayed())
        self.signin_page.select_region("USA")
        self.signin_page.set_remember_password(True)
        self.signin_page.submit_email_and_password()
        my_vault_page = self.utilities.wait_for_element_by_text("My vault")
        self.assertTrue(my_vault_page.is_displayed())

    def test_login_usa_wrong_id_password(self):
        print("*** TC: Login to US environment")
        self.assertTrue(self.signin_page.is_login_page_displayed())
        self.signin_page.select_region("USA")
        self.signin_page.set_remember_password(False)
        self.signin_page.submit_email_and_password()
        self.assertTrue(self.signin_page.is_alert_displayed())
        self.signin_page.accept_alert()
        self.signin_page.close_password_page()
        self.assertTrue(self.signin_page.is_login_page_displayed())

if __name__ == '__main__':
    unittest.main()
