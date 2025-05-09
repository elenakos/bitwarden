
from time import sleep
from ObjectModel.Helpers.AppiumUtilities import AppiumUtil
from ObjectModel.HeaderBar import HeaderBar

class SignIn:
    # All variables
    SELF_HOSTED_URL = "https://ptah.local"
    WAIT_TIME_LONG = 5
    WAIT_TIME_SHORT = 3

    # All elements from the sign-in page
    LOGIN_TEXT = "Log in to Bitwarden"
    EMAIL_ADDRESS_EDIT_TEXT = "EmailAddressEntry"
    REGION_SELECTION_DROPDOWN = "RegionSelectorDropdown"
    REMEMBER_EMAIL_TOGGLE_TEXT = "RememberMeSwitch"
    REMEMBER_EMAIL_TOGGLE = "SwitchToggle"
    CONTINUE_BUTTON = "ContinueButton"

    # Elements from the alert popup
    ALERT_POPUP = "AlertPopup"
    ALERT_TEXT = "AlertTitleText"
    ALERT_CONTENT_TEXT = "AlertContentText"
    DOT_COM_OPTION_TEXT = "bitwarden.com"
    DOT_EU_OPTION_TEXT = "bitwarden.eu"
    SELF_HOSTED_OPTION_TEXT = "SelfHosted"
    CANCEL_BUTTON = "DismissAlertButton"
    OK_BUTTON = "AcceptAlertButton"

    # Elements from Self-host configuration
    CLOSE_BUTTON = "CloseButton"
    HOSTED_SERVER_FIELD = "ServerUrlEntry"
    SAVE_BUTTON = "SaveButton"

    # Password page
    CLOSE_BUTTON_PASSWORD = "CloseButton"
    PASSWORD_FIELD = "MasterPasswordEntry"
    PASSWORD_VISIBILITY_TOGGLE = "PasswordVisibleToggle"
    LOGIN_BUTTON = "LogInWithMasterPasswordButton"
    VERIFY_PASSWORD_TEXT = "Verify master password"

    # Logout Popup
    CANCEL_BUTTON = "DismissAlertButton"
    ACCEPT_BUTTON = "AcceptAlertButton"



    def __init__(self, driver, test, properties):
        self.driver = driver
        self.utilities = AppiumUtil(driver)
        self.test = test
        self.properties = properties
        self.header_bar = HeaderBar(driver)

    def is_login_page_displayed(self):
        # Check if a user if already logged-in, then log-out
        if self.is_verify_master_password_page_is_displayed():
            print("Looks like a user is already logged in. Let's logout")
            self.user_logout()
        login_message = self.utilities.wait_for_element_by_text(self.LOGIN_TEXT)
        return login_message.is_displayed()

    def is_verify_master_password_page_is_displayed(self):
        # Check if a header bar is present
        if not self.header_bar.is_header_visible():
            return False
        page_title = self.header_bar.get_page_name()
        if page_title == self.VERIFY_PASSWORD_TEXT:
            return True
        else:
            return False

    def user_logout(self):
        print("User logout by clicking on More -> Logout")
        self.header_bar.click_on_more_button()
        self.header_bar.click_on_logout_button()
        if self.is_alert_displayed():
            yes_button = self.utilities.wait_for_element_by_resource_id(self.ACCEPT_BUTTON)
            yes_button.click()

    def open_host_region_selection_popup(self):
        print("Open a host region selection popup")
        retry = 3
        dialog = None
        while dialog is None and retry > 0:
            sleep(self.WAIT_TIME_LONG)
            region = self.utilities.find_element_by_resource_id(self.REGION_SELECTION_DROPDOWN)
            region.click()
            dialog = self.utilities.wait_for_element_by_resource_id(self.ALERT_POPUP)
            retry = retry - 1


    def configure_self_hosted(self):
        print("Configure a self hosted option")
        self.open_host_region_selection_popup()
        self_hosted_radio_button = self.utilities.wait_for_element_by_text(self.SELF_HOSTED_OPTION_TEXT)
        self.test.assertIsNotNone(self_hosted_radio_button)
        self_hosted_radio_button.click()
        server_url_entry = self.utilities.find_element_by_resource_id(self.HOSTED_SERVER_FIELD)
        server_url_entry.send_keys(self.SELF_HOSTED_URL)
        save_button = self.utilities.find_element_by_resource_id(self.SAVE_BUTTON)
        save_button.click()
        sleep(self.WAIT_TIME_LONG)

    def select_region(self, region="EU"):
        print("Select {} region".format(region))
        self.open_host_region_selection_popup()
        if region == "USA":
            radio_button = self.utilities.wait_for_element_by_text(self.DOT_COM_OPTION_TEXT)
        else:
            radio_button = self.utilities.find_element_by_text(self.DOT_EU_OPTION_TEXT)
        radio_button.click()

    def cancel_region_selector_dialog(self):
        print("Close a region selection dialog")
        cancel_dialog_button = self.utilities.find_element_by_resource_id(self.CANCEL_BUTTON)
        cancel_dialog_button.click()

    def set_remember_email_option(self, option = True):
        print("Set remember email as {}".format(option))
        remember_email_button = self.utilities.find_element_by_resource_id(self.REMEMBER_EMAIL_TOGGLE_TEXT)
        toggle_status = remember_email_button.get_attribute("checked")
        print("*** Toggle status: {}".format(toggle_status))
        if option:
            if toggle_status == "true":
                return
            else:
                remember_email_button.click()
        if not option:
            if toggle_status == "false":
                return
            else:
                remember_email_button.click()

    def submit_email_and_password(self, user, password):
        print("Enter email and password")
        email_address_field = self.utilities.wait_for_element_by_resource_id(self.EMAIL_ADDRESS_EDIT_TEXT)
        self.test.assertTrue(email_address_field.is_displayed())
        email_address_field.clear()
        email_address_field.send_keys(user)
        sleep(self.WAIT_TIME_SHORT)
        continue_button = self.utilities.wait_for_element_by_resource_id(self.CONTINUE_BUTTON)
        continue_button.click()
        master_password_entry = self.utilities.wait_for_element_by_resource_id(self.PASSWORD_FIELD)
        master_password_entry.send_keys(password)
        sleep(self.WAIT_TIME_SHORT)
        login_button = self.utilities.wait_for_element_by_resource_id(self.LOGIN_BUTTON)
        login_button.click()
        sleep(self.WAIT_TIME_LONG * 3)

    def accept_alert(self):
        print("Accept alert")
        ok_button = self.utilities.wait_for_element_by_resource_id(self.OK_BUTTON)
        ok_button.click()

    def close_password_page(self):
        print("Close password page")
        close_button = self.utilities.wait_for_element_by_resource_id(self.CLOSE_BUTTON_PASSWORD)
        close_button.click()

    def is_alert_displayed(self):
        print("Check if an alert popup is displayed")
        alert = self.utilities.wait_for_element_by_resource_id(self.ALERT_POPUP)
        return (alert.is_displayed())