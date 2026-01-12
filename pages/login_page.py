"""
Login Page Module
=================

Page Object Model implementation for the OpenCart Login page.
Provides methods for user authentication and navigation to related pages.

Features:
    - User login with email and password
    - Navigation to registration page
    - Password recovery link verification

Example:
    >>> login_page = LoginPage(driver)
    >>> account_page = login_page.do_login("user@example.com", "password123")
"""

import logging

from selenium.webdriver.common.by import By

from pages.account_page import AccountPage
from pages.user_registration_page import UserRegistrationPage
from utils.config_reader import ConfigReader
from utils.element_util import ElementUtil

_logger = logging.getLogger(__name__)


class LoginPage:
    """
    Page Object for the OpenCart Login page.
    
    Encapsulates all interactions with the login page including
    authentication, navigation, and element verification.
    
    Attributes:
        driver: Selenium WebDriver instance.
        
    Example:
        >>> login_page = LoginPage(driver)
        >>> assert login_page.get_page_title() == "Account Login"
        >>> account_page = login_page.do_login("test@example.com", "pass123")
    """
    
    # Private locators - prefixed with __ to indicate they should not be accessed outside the class
    __email_field = (By.ID, 'input-email')
    __password_field = (By.ID, 'input-password')
    __login_button = (By.CSS_SELECTOR, 'input[value="Login"]')
    __forgot_password_link = (By.LINK_TEXT, 'Forgotten Password')
    __registration_link = (By.LINK_TEXT, 'Register')

    def __init__(self, driver):
        """
        Initialize LoginPage and navigate to the login URL.
        
        Args:
            driver: Selenium WebDriver instance.
            
        Note:
            The login URL is automatically retrieved from config.yaml
            and the page is navigated to upon initialization.
        """
        self.__driver = driver
        self.__util = ElementUtil(self.__driver)
        login_url = ConfigReader.get_config('login_url')
        _logger.info(f"LoginPage: Initializing | Navigating to: {login_url}")
        self.__util.launch_url(login_url)
        _logger.info(f"LoginPage: Ready | Current URL: {self.__driver.current_url} | Title: {self.__driver.title}")

    def get_page_title(self) -> str:
        """
        Get the current page title.
        
        Returns:
            str: The browser's current page title.
            
        Example:
            >>> title = login_page.get_page_title()
            >>> assert title == "Account Login"
        """
        title = self.__driver.title
        _logger.debug(f"LoginPage: Retrieved page title: '{title}'")
        return title

    def get_page_url(self) -> str:
        """
        Get the current page URL.
        
        Returns:
            str: The browser's current URL.
            
        Example:
            >>> url = login_page.get_page_url()
            >>> assert "route=account/login" in url
        """
        url = self.__driver.current_url
        _logger.debug(f"LoginPage: Retrieved page URL: '{url}'")
        return url

    def does_forgot_password_link_exists(self) -> bool:
        """
        Check if the 'Forgotten Password' link is displayed.
        
        Returns:
            bool: True if the link is visible, False otherwise.
            
        Example:
            >>> assert login_page.does_forgot_password_link_exists()
        """
        _logger.info("LoginPage: Checking if 'Forgot Password' link exists")
        exists = self.__util.is_element_displayed(self.__forgot_password_link)
        _logger.debug(f"LoginPage: 'Forgot Password' link exists: {exists}")
        return exists

    def do_login(self, email: str, password: str) -> AccountPage:
        """
        Perform user login with provided credentials.
        
        Enters email and password, clicks the login button,
        and returns the AccountPage object for the logged-in user.
        
        Args:
            email: User's email address.
            password: User's password.
            
        Returns:
            AccountPage: Page object for the user account page.
            
        Example:
            >>> account_page = login_page.do_login("user@test.com", "secret123")
            >>> assert account_page.is_logout_link_exists()
        """
        _logger.info(f"LoginPage: Attempting login | Email: {email} | Password: {'*' * len(password)}")

        _logger.debug(f"LoginPage: Entering email: {email}")
        self.__util.enter_text(self.__email_field, email)

        _logger.debug(f"LoginPage: Entering password: {'*' * len(password)}")
        self.__util.enter_text(self.__password_field, password)

        _logger.debug("LoginPage: Clicking Login button")
        self.__util.click_element(self.__login_button)

        _logger.info(f"LoginPage: Login submitted | Navigating to AccountPage")
        return AccountPage(self.__driver)

    def click_registration_link(self) -> UserRegistrationPage:
        """
        Click the 'Register' link to navigate to user registration.
        
        Returns:
            UserRegistrationPage: Page object for the registration page.
            
        Example:
            >>> reg_page = login_page.click_registration_link()
            >>> assert "Register" in reg_page.get_user_registration_page_title()
        """
        _logger.info("LoginPage: Clicking 'Register' link")
        self.__util.click_element(self.__registration_link)
        _logger.info("LoginPage: Navigating to UserRegistrationPage")
        return UserRegistrationPage(self.__driver)
