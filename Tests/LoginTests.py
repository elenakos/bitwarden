import unittest
from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions
from ObjectModel.SignInPage import SignIn
from ObjectModel.MyVaultPage import MyVault
from ObjectModel.Helpers.AppiumUtilities import AppiumUtil
from Utilities.Properties import Properties
from TestSetup import BitwardenTestSetup

class LoginPageTests(unittest.TestCase):

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
        self.capabilities_options = AppiumOptions().load_capabilities(self.capabilities)
        self.driver = webdriver.Remote(command_executor=self.host, options=self.capabilities_options)
        self.utilities = AppiumUtil(self.driver)
        self.properties = Properties()
        self.signin_page = SignIn(self.driver, self, self.properties.get_properties())
        self.my_vault_page = MyVault(self.driver)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_verify_login_page(self):
        print("*** TC: Verify a login page appears")
        self.assertTrue(self.signin_page.is_login_page_displayed())
        # Printing page source for debugging
        self.utilities.print_page_source()

    @unittest.skip("Skipping this test - no hosted environment")
    def test_login_to_hosted_environment(self):
        print("*** TC: Login to a hosted environment")
        self.assertTrue(self.signin_page.is_login_page_displayed())
        self.signin_page.configure_self_hosted()
        user = self.properties.get_properties()["login_id"]
        password = self.properties.get_properties()["password"]
        self.signin_page.submit_email_and_password(user, password)
        self.assertTrue(self.my_vault_page.is_my_vault_page_displayed())

    @unittest.skip("Skipping this test - set valid ID/password in config.properties")
    def test_login_to_usa_environment(self):
        print("*** TC: Login to US environment with the correct ID/password")
        self.assertTrue(self.signin_page.is_login_page_displayed())
        self.signin_page.select_region("USA")
        self.signin_page.set_remember_email_option(True)
        user = self.properties.get_properties()["login_id"]
        password = self.properties.get_properties()["password"]
        self.signin_page.submit_email_and_password(user, password)
        self.assertTrue(self.my_vault_page.is_my_vault_page_displayed())

    def test_login_to_usa_environment_wrong_id_password(self):
        print("*** TC: Login to US environment with the wrong ID/password")
        self.assertTrue(self.signin_page.is_login_page_displayed())
        self.signin_page.select_region("USA")
        self.signin_page.set_remember_email_option(False)
        user = "somebody@domain.com"
        password = "wrongPassword123"
        self.signin_page.submit_email_and_password(user, password)
        self.assertTrue(self.signin_page.is_alert_displayed())
        self.signin_page.accept_alert()
        self.signin_page.close_password_page()
        self.assertTrue(self.signin_page.is_login_page_displayed())

if __name__ == '__main__':
    unittest.main()
