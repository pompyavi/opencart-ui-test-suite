"""
Account Page Module
===================

Page Object Model implementation for the OpenCart Account page.
Represents the user's account dashboard after successful login.

Features:
    - Account section header verification
    - Logout link verification
    - Page title and URL retrieval

Example:
    >>> account_page = login_page.do_login("user@example.com", "password")
    >>> assert account_page.is_logout_link_exists()
    >>> headers = account_page.get_account_headers()
"""

import logging
from typing import List

from selenium.webdriver.common.by import By

from utils.element_util import ElementUtil

_logger = logging.getLogger(__name__)


class AccountPage:
    """
    Page Object for the OpenCart User Account page.
    
    This page is displayed after successful user login and provides
    access to account management features.
    
    Attributes:
        driver: Selenium WebDriver instance.
        
    Example:
        >>> account_page = AccountPage(driver)
        >>> headers = account_page.get_account_headers()
        >>> assert "My Account" in headers
    """
    
    # Private locators
    __account_header = (By.CSS_SELECTOR, '#content h2')
    __logout_link = (By.LINK_TEXT, 'Logout')

    def __init__(self, driver):
        """
        Initialize AccountPage with the current driver state.
        
        Args:
            driver: Selenium WebDriver instance (should already be on account page).
            
        Note:
            Unlike LoginPage, this does not navigate to a URL.
            It assumes the driver is already on the account page
            (typically after successful login).
        """
        self.__driver = driver
        self.__util = ElementUtil(self.__driver)
        _logger.info(f"AccountPage: Initialized | URL: {self.__driver.current_url} | Title: {self.__driver.title}")

    def get_page_title(self) -> str:
        """
        Get the current page title.
        
        Returns:
            str: The browser's current page title.
            
        Example:
            >>> title = account_page.get_page_title()
            >>> assert title == "My Account"
        """
        title = self.__driver.title
        _logger.debug(f"AccountPage: Retrieved page title: '{title}'")
        return title

    def get_page_url(self) -> str:
        """
        Get the current page URL.
        
        Returns:
            str: The browser's current URL.
            
        Example:
            >>> url = account_page.get_page_url()
            >>> assert "route=account/account" in url
        """
        url = self.__driver.current_url
        _logger.debug(f"AccountPage: Retrieved page URL: '{url}'")
        return url

    def get_account_headers(self) -> List[str]:
        """
        Get all section headers displayed on the account page.
        
        Returns:
            List[str]: List of header text (e.g., ["My Account", "My Orders", ...]).
            
        Example:
            >>> headers = account_page.get_account_headers()
            >>> assert len(headers) == 4
            >>> assert "My Account" in headers
        """
        _logger.info("AccountPage: Getting account section headers")
        headers = self.__util.get_elements_text(self.__account_header)
        _logger.debug(f"AccountPage: Found {len(headers)} headers: {headers}")
        return headers

    def is_logout_link_exists(self) -> bool:
        """
        Check if the 'Logout' link is displayed.
        
        This is commonly used to verify successful login.
        
        Returns:
            bool: True if logout link is visible, False otherwise.
            
        Example:
            >>> # After login
            >>> assert account_page.is_logout_link_exists(), "Login failed!"
        """
        _logger.info("AccountPage: Checking if 'Logout' link exists")
        exists = self.__util.is_element_displayed(self.__logout_link)
        _logger.debug(f"AccountPage: 'Logout' link exists: {exists}")
        return exists
