import pytest
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
create account page

@Author: Efrat Cohen
@Date: 06.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(@class, 'chakra-text css-x4xr8c')]")
ENTER_ACCOUNT_NAME_INPUT = (By.XPATH, "//*[contains(@class, 'chakra-input css-dc6ofi')]")
ENTER_PASSWORD_INPUT = (By.XPATH, "//*[contains(@class, 'chakra-input css-hc5dva')]")
CREATE_BTN = (By.XPATH, "//*[contains(@class, 'chakra-button css-1xo7i53')]")


class CreateAccountPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def insert_account_name(self):
        """
        insert account name
        """
        self.enter_text("ENTER_ACCOUNT_NAME_INPUT", ENTER_ACCOUNT_NAME_INPUT, pytest.wallets_data.get("cardano").get("account_name"))

    def insert_password(self):
        """
        insert password
        """
        self.enter_text_on_specific_list_item("ENTER_PASSWORD_INPUT", ENTER_PASSWORD_INPUT, 0, pytest.wallets_data.get("cardano").get("account_password"))

    def insert_confirm_password(self):
        """
        insert confirm password
        """
        self.enter_text_on_specific_list_item("ENTER_CONFIRM_PASSWORD_INPUT", ENTER_PASSWORD_INPUT, 1, pytest.wallets_data.get("cardano").get("account_password"))

    def click_on_create_button(self):
        """
        click on create button
        """
        self.click("CREATE_BTN", CREATE_BTN)