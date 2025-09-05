import time

from selenium.webdriver.common.by import By
from pages.account_page import AccountPage
from pages.user_registration_page import UserRegistrationPage
from utils.config_reader import ConfigReader
from utils.element_util import ElementUtil
import logging

class LoginPage:
    __email_field = By.ID, 'input-email'
    __password_field = By.ID, 'input-password'
    __login_button = By.CSS_SELECTOR, 'input[value="Login"]'
    __forgot_password_link = By.LINK_TEXT, 'Forgotten Password'
    __registration_link = By.LINK_TEXT, 'Register'


    def __init__(self, driver):
        self.__driver = driver
        self.__util = ElementUtil(self.__driver)
        self.__util.launch_url(ConfigReader.get_config('login_url'))
        #time.sleep(150)
        self.__logger = logging.getLogger(__name__)

    def get_page_title(self):
        return self.__driver.title

    def get_page_url(self):
        return self.__driver.current_url

    def does_forgot_password_link_exists(self):
        return self.__util.is_element_displayed(self.__forgot_password_link)

    def do_login(self, email, password):
        self.__logger.debug(f'Logging in with email: {email} and password: {"*" * len(password)}')

        self.__logger.debug(f'Entered email: {email}')
        self.__util.enter_text(self.__email_field, email)

        self.__logger.debug(f'Entered password: {"*" * len(password)}')
        self.__util.enter_text(self.__password_field, password)

        self.__logger.debug(f'Clicked on Login button')
        self.__util.click_element(self.__login_button)
        return AccountPage(self.__driver)

    def click_registration_link(self):
        self.__util.click_element(self.__registration_link)
        return UserRegistrationPage(self.__driver)

    

