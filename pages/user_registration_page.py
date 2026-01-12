"""
User Registration Page Module
=============================

Page Object Model implementation for the OpenCart User Registration page.
Handles new user account creation with form filling and validation.

Features:
    - Complete user registration with all required fields
    - Newsletter subscription selection
    - Terms and conditions acceptance
    - Registration success verification

Example:
    >>> reg_page = login_page.click_registration_link()
    >>> success = reg_page.register_user(
    ...     first_name="John",
    ...     last_name="Doe",
    ...     email="john@example.com",
    ...     telephone="1234567890",
    ...     password="SecurePass123",
    ...     subscribe="yes"
    ... )
"""

import logging

from selenium.webdriver.common.by import By

from constants import app_constants
from constants.app_constants import SHORT_WAIT
from utils.element_util import ElementUtil

_logger = logging.getLogger(__name__)


class UserRegistrationPage:
    """
    Page Object for the OpenCart User Registration page.
    
    Provides methods to fill out the registration form and
    verify successful account creation.
    
    Attributes:
        driver: Selenium WebDriver instance.
        
    Example:
        >>> reg_page = UserRegistrationPage(driver)
        >>> success = reg_page.register_user(
        ...     "Jane", "Smith", "jane@test.com", "555-1234", "pass123", "no"
        ... )
        >>> assert success, "Registration failed"
    """

    def __init__(self, driver):
        """
        Initialize UserRegistrationPage with the current driver state.
        
        Args:
            driver: Selenium WebDriver instance (should be on registration page).
        """
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

        _logger.info(f"UserRegistrationPage: Initialized | URL: {self.__driver.current_url} | Title: {self.__driver.title}")

    def get_user_registration_page_title(self) -> str:
        """
        Get the current page title.
        
        Returns:
            str: The browser's current page title.
            
        Example:
            >>> title = reg_page.get_user_registration_page_title()
            >>> assert "Register" in title
        """
        title = self.__driver.title
        _logger.debug(f"UserRegistrationPage: Retrieved page title: '{title}'")
        return title

    def get_user_registration_page_header(self) -> str:
        """
        Get the page header text.
        
        Returns:
            str: The main header text on the registration page.
            
        Example:
            >>> header = reg_page.get_user_registration_page_header()
            >>> assert header == "Register Account"
        """
        _logger.info("UserRegistrationPage: Getting page header")
        header = self.__util.get_element_text(self.__header)
        _logger.debug(f"UserRegistrationPage: Header text: '{header}'")
        return header

    def register_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        telephone: str,
        password: str,
        subscribe: str,
    ) -> bool:
        """
        Complete the user registration process.
        
        Fills out all registration form fields, accepts terms,
        and submits the form. After successful registration,
        logs out and returns to the registration page for the
        next test iteration.
        
        Args:
            first_name: User's first name.
            last_name: User's last name.
            email: User's email address (must be unique).
            telephone: User's phone number.
            password: Account password.
            subscribe: Newsletter subscription - "yes" or "no".
            
        Returns:
            bool: True if registration was successful, False otherwise.
            
        Note:
            After successful registration, this method automatically:
            1. Logs out the newly created user
            2. Navigates back to the registration page
            3. Waits for the page to be ready for the next registration
            
        Example:
            >>> success = reg_page.register_user(
            ...     first_name="Test",
            ...     last_name="User",
            ...     email="testuser123@example.com",
            ...     telephone="9876543210",
            ...     password="Password123!",
            ...     subscribe="yes"
            ... )
            >>> assert success, "Registration should succeed"
        """
        _logger.info(f"UserRegistrationPage: Starting user registration | "
                     f"Name: {first_name} {last_name} | Email: {email} | Phone: {telephone} | Subscribe: {subscribe}")

        eu = self.__util
        do_subscribe = [By.XPATH, "(//label[@class='radio-inline'])[position()={}]/input[@type='radio']"]

        if subscribe.strip().lower() == "yes":
            do_subscribe[1] = do_subscribe[1].format('1')  # Subscribe Yes
            _logger.debug("UserRegistrationPage: Newsletter subscription: YES")
        else:
            do_subscribe[1] = do_subscribe[1].format('2')
            _logger.debug("UserRegistrationPage: Newsletter subscription: NO")

        _logger.debug(f"UserRegistrationPage: Entering first name: '{first_name}'")
        eu.wait_for_element_to_be_visible(self.__first_name, 5).send_keys(first_name)

        _logger.debug(f"UserRegistrationPage: Entering last name: '{last_name}'")
        eu.enter_text(self.__last_name, last_name)

        _logger.debug(f"UserRegistrationPage: Entering email: '{email}'")
        eu.enter_text(self.__email, email)

        _logger.debug(f"UserRegistrationPage: Entering telephone: '{telephone}'")
        eu.enter_text(self.__telephone, telephone)

        _logger.debug(f"UserRegistrationPage: Entering password: {'*' * len(password)}")
        eu.enter_text(self.__password, password)

        _logger.debug(f"UserRegistrationPage: Confirming password: {'*' * len(password)}")
        eu.enter_text(self.__confirm_password, password)

        _logger.debug("UserRegistrationPage: Selecting newsletter subscription option")
        eu.click_element(do_subscribe)

        _logger.debug("UserRegistrationPage: Accepting terms and conditions")
        eu.click_element(self.__agree_checkbox)

        _logger.info("UserRegistrationPage: Submitting registration form")
        eu.click_element(self.__continue_button)

        # Validate success and reset to registration page
        _logger.info("UserRegistrationPage: Waiting for success message")
        success_text = eu.wait_for_element_to_be_visible(self.__success_message, SHORT_WAIT).text.strip()
        _logger.debug(f"UserRegistrationPage: Success message: '{success_text}'")

        if success_text == app_constants.USER_REGISTER_SUCCESS_MESG:
            _logger.info(f"UserRegistrationPage: Registration SUCCESSFUL for: {email}")

            _logger.debug("UserRegistrationPage: Clicking logout link")
            eu.click_element(self.__logout_link)

            _logger.debug("UserRegistrationPage: Clicking register link to reset for next iteration")
            eu.click_element(self.__register_link)

            # Wait for registration page to be ready for next iteration
            eu.wait_for_element_to_be_visible(self.__first_name, SHORT_WAIT)
            _logger.info("UserRegistrationPage: Ready for next registration")
            return True

        _logger.warning(f"UserRegistrationPage: Registration FAILED for: {email} | Message: '{success_text}'")
        return False
