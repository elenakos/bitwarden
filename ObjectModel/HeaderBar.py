from ObjectModel.Helpers.AppiumUtilities import AppiumUtil

class HeaderBar:
    # All elements from the header bar
    HEADER_BAR = "HeaderBarComponent"
    PAGE_TITLE_LABEL = "PageTitleLabel"
    ACCOUNT_BUTTON = "CurrentActiveAccount"
    SEARCH_VAULT_BUTTON = "SearchButton"
    HEADER_BAR_OPTIONS_BUTTON = "HeaderBarOptionsButton"
    MORE_FLOATING_MENU = "FloatingOptionsContent"
    LOG_OUT_BUTTON = "FloatingOptionsItemName"

    def __init__(self, driver):
        self.driver = driver
        self.utilities = AppiumUtil(driver)

    def is_header_visible(self):
        try:
            header = self.utilities.wait_for_element_by_resource_id(self.HEADER_BAR)
            return header.is_displayed()
        except:
            return False

    def get_page_name(self):
        print("Return a page title")
        page_title_element = self.utilities.wait_for_element_by_resource_id(self.PAGE_TITLE_LABEL)
        page_name = page_title_element.text
        print("*** Current page: " + page_name)
        return page_name

    def click_on_more_button(self):
        print("Click on More button")
        more_button = self.utilities.wait_for_element_by_resource_id(self.HEADER_BAR_OPTIONS_BUTTON)
        more_button.click()

    def is_logout_option_visible(self):
        logout_button = self.utilities.wait_for_element_by_resource_id(self.LOG_OUT_BUTTON)
        return logout_button.is_displayed()

    def click_on_logout_button(self):
        if self.is_logout_option_visible():
            logout_button = self.utilities.wait_for_element_by_resource_id(self.LOG_OUT_BUTTON)
            logout_button.click()
