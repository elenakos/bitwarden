from time import sleep
from ObjectModel.Helpers.AppiumUtilities import AppiumUtil
from ObjectModel.HeaderBar import HeaderBar

class MyVault:
    # All elements from the sign-in page
    ADD_ITEM_BUTTOn = "AddItemButton"

    def __init__(self, driver):
        self.driver = driver
        self.utilities = AppiumUtil(driver)
        self.header_bar = HeaderBar(driver)

    def is_my_vault_page_displayed(self):
        my_vault_page = self.utilities.wait_for_element_by_text("My vault")
        self.utilities.print_page_source()
        return my_vault_page.is_displayed()
