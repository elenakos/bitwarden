from ObjectModel.Helpers.AppiumUtilities import AppiumUtil

class NavigationBar:
    # Navigation Bar
    VAULT_TAB = "VaultTab"
    SEND_TAB = "SendTab"
    GENERATOR_TAB = "GeneratorTab"
    SETTINGS_TAB = "SettingsTab"

    def __init__(self, driver):
        self.driver = driver
        self.utilities = AppiumUtil(driver)