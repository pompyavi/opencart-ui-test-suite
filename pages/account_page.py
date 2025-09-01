import logging
from selenium.webdriver.common.by import By
from utils.element_util import ElementUtil


class AccountPage:
    __account_header = By.CSS_SELECTOR, '#content h2'
    __logout_link = By.LINK_TEXT, 'Logout'

    def __init__(self, driver):
        self.__driver = driver
        self.__util = ElementUtil(self.__driver)
        self.__logger = logging.getLogger(__name__)

    def get_page_title(self):
        return self.__driver.title

    def get_page_url(self):
        return self.__driver.current_url

    def get_account_headers(self):
        self.__logger.debug('Getting account page headers')
        return self.__util.get_elements_text(self.__account_header)

    def is_logout_link_exists(self):
        return self.__util.is_element_displayed(self.__logout_link)
