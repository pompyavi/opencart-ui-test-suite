from selenium.webdriver.common.by import By

from constants import app_constants
from constants.app_constants import SHORT_WAIT
from utils.element_util import ElementUtil


class UserRegistrationPage:
    def __init__(self, driver):
        self.__driver = driver
        self.__util = ElementUtil(driver)

        # Locators
        self.__header = (By.CSS_SELECTOR, "#content h1")
        self.__first_name = (By.ID, "input-firstname")
        self.__last_name = (By.ID, "input-lastname")
        self.__email = (By.ID, "input-email")
        self.__telephone = (By.ID, "input-telephone")
        self.__password = (By.ID, "input-password")
        self.__confirm_password = (By.ID, "input-confirm")
        self.__agree_checkbox = (By.NAME, "agree")
        self.__continue_button = (By.XPATH, "//input[@type='submit' and @value='Continue']")
        self.__success_message = (By.CSS_SELECTOR, "div#content h1")
        self.__logout_link = (By.LINK_TEXT, "Logout")
        self.__register_link = (By.LINK_TEXT, "Register")

    def get_user_registration_page_title(self) -> str:
        return self.__driver.title

    def get_user_registration_page_header(self) -> str:
        return self.__util.get_element_text(self.__header)

    def register_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        telephone: str,
        password: str,
        subscribe: str,
    ) -> bool:
        eu = self.__util
        do_subscribe = [By.XPATH, "(//label[@class='radio-inline'])[position()={}]/input[@type='radio']"]

        if subscribe.strip().lower() == "yes":
            do_subscribe[1] = do_subscribe[1].format('1')  # Subscribe Yes
        else:
            do_subscribe[1] = do_subscribe[1].format('2')

        eu.wait_for_element_to_be_visible(self.__first_name, 5).send_keys(first_name)
        eu.enter_text(self.__last_name, last_name)
        eu.enter_text(self.__email, email)
        eu.enter_text(self.__telephone, telephone)
        eu.enter_text(self.__password, password)
        eu.enter_text(self.__confirm_password, password)
        eu.click_element(do_subscribe)
        eu.click_element(self.__agree_checkbox)
        eu.click_element(self.__continue_button)

        # Validate success and reset to registration page
        success_text = eu.wait_for_element_to_be_visible(self.__success_message, SHORT_WAIT).text.strip()
        if success_text == app_constants.USER_REGISTER_SUCCESS_MESG:
            eu.click_element(self.__logout_link)
            eu.click_element(self.__register_link)
            return True
        return False