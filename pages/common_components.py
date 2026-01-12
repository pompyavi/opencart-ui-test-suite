"""
Common Components Module
========================

Provides reusable page components that appear across multiple pages.
Uses lazy loading via @cached_property for efficient instantiation.

Components:
    - Footer: Footer sections and links
    - RightColumnLinks: Right sidebar navigation links
    - Search: Global search functionality

Features:
    - Lazy loading of components (only instantiated when accessed)
    - Shared ElementUtil instance for efficiency
    - Allure integration for test reporting

Example:
    >>> common = CommonComponents(driver)
    >>> footer_sections = common.footer.get_all_footer_sections_text()
    >>> results = common.search.search_product("macbook")
"""

import logging
from functools import cached_property
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from constants.app_constants import SHORT_WAIT
from pages.search_result_page import SearchResultPage
from utils.element_util import ElementUtil

# --- optional Allure (won't break if missing) ---
try:
    import allure
    _ALLURE = True
except ImportError:
    allure = None
    _ALLURE = False


def allure_step(step_text: str):
    """
    Decorator that adds Allure step reporting if Allure is available.
    
    Args:
        step_text: Description of the step for Allure reports.
        
    Returns:
        Decorated function with Allure step, or original function.
    """
    def decorator(func):
        if _ALLURE:
            return allure.step(step_text)(func)
        return func
    return decorator


_logger = logging.getLogger(__name__)


class CommonComponents:
    """
    Container for common page components accessible across all pages.
    
    Uses lazy loading to instantiate components only when first accessed,
    improving performance when not all components are needed.
    
    Attributes:
        footer: Footer component for footer-related operations.
        right_column_links: Right column navigation links.
        search: Global search functionality.
        
    Example:
        >>> common = CommonComponents(driver)
        >>> # Footer is only instantiated when accessed
        >>> sections = common.footer.get_all_footer_sections_text()
    """

    def __init__(self, driver):
        """
        Initialize CommonComponents with a WebDriver instance.
        
        Args:
            driver: Selenium WebDriver instance.
        """
        self.__driver = driver
        self.__util = ElementUtil(self.__driver)
        _logger.debug("CommonComponents initialized")

    @cached_property
    def footer(self) -> "Footer":
        """
        Get the Footer component (lazy loaded).
        
        Returns:
            Footer: Footer component instance.
        """
        _logger.debug("Lazy loading Footer component")
        return Footer(self.__driver, self.__util)

    @cached_property
    def right_column_links(self) -> 'RightColumnLinks':
        """
        Get the RightColumnLinks component (lazy loaded).
        
        Returns:
            RightColumnLinks: Right column links component instance.
        """
        _logger.debug("Lazy loading RightColumnLinks component")
        return RightColumnLinks(self.__driver, self.__util)

    @cached_property
    def search(self) -> 'Search':
        """
        Get the Search component (lazy loaded).
        
        Returns:
            Search: Search component instance.
        """
        _logger.debug("Lazy loading Search component")
        return Search(self.__driver, self.__util)


class Footer:
    """
    Component for interacting with the page footer.
    
    Provides methods to retrieve footer section titles and links.
    
    Example:
        >>> footer = Footer(driver, util)
        >>> sections = footer.get_all_footer_sections_text()
        >>> assert "Information" in sections
    """
    
    __FOOTER_SECTION = (By.XPATH, "//footer//h5")
    __FOOTER_LINKS = (By.XPATH, "./following-sibling::ul//a")

    def __init__(self, driver, element_util: ElementUtil):
        """
        Initialize Footer component.
        
        Args:
            driver: Selenium WebDriver instance.
            element_util: Shared ElementUtil instance.
        """
        self.__driver = driver
        self.__util = element_util
        _logger.debug("Footer component initialized")

    def get_all_footer_sections_text(self) -> List[str]:
        """
        Get all footer section titles.
        
        Returns:
            List[str]: List of section titles (e.g., ["Information", "Customer Service"]).
            
        Example:
            >>> sections = footer.get_all_footer_sections_text()
            >>> assert len(sections) == 4
        """
        _logger.info("Getting all footer section titles")
        sections = self.__util.get_elements_text(self.__FOOTER_SECTION)
        _logger.debug(f"Found {len(sections)} footer sections: {sections}")
        return sections

    def get_footer_links_text(self) -> List[str]:
        """
        Get the text of all links in all footer sections.
        
        Returns:
            List[str]: List of all link texts across all sections.
            
        Example:
            >>> links = footer.get_footer_links_text()
            >>> assert "About Us" in links
        """
        _logger.info("Getting all footer links text")
        sections: List[WebElement] = self.__util.get_elements(self.__FOOTER_SECTION)
        texts: List[str] = []
        for section in sections:
            links = section.find_elements(*self.__FOOTER_LINKS)
            for link in links:
                texts.append(link.text)
        _logger.debug(f"Found {len(texts)} footer links: {texts}")
        return texts

    def get_specific_section_footer_links_text(self, section: str) -> List[str]:
        """
        Get links from a specific footer section.
        
        Args:
            section: Exact section title (e.g., "Information").
            
        Returns:
            List[str]: List of link texts in that section.
            
        Example:
            >>> links = footer.get_specific_section_footer_links_text("Information")
            >>> assert "About Us" in links
        """
        _logger.info(f"Getting footer links for section: '{section}'")
        section_links = (
            By.XPATH,
            f"//footer//h5[text()='{section}']/following-sibling::ul//a",
        )
        links = self.__util.get_elements_text(section_links)
        _logger.debug(f"Found {len(links)} links in '{section}': {links}")
        return links


class RightColumnLinks:
    """
    Component for the right sidebar navigation links.
    
    These links typically include account-related navigation options
    like "Login", "Register", "My Account", etc.
    
    Example:
        >>> right_col = RightColumnLinks(driver, util)
        >>> links = right_col.get_right_column_links()
        >>> assert "Login" in links or "Logout" in links
    """
    
    __RIGHT_COLUMN_LINKS = (By.CSS_SELECTOR, '#column-right a')

    def __init__(self, driver, element_util: ElementUtil):
        """
        Initialize RightColumnLinks component.
        
        Args:
            driver: Selenium WebDriver instance.
            element_util: Shared ElementUtil instance.
        """
        self.__driver = driver
        self.__util = element_util
        _logger.debug("RightColumnLinks component initialized")

    def get_right_column_links(self) -> List[str]:
        """
        Get all link texts from the right column.
        
        Returns:
            List[str]: List of link texts.
            
        Example:
            >>> links = right_col.get_right_column_links()
            >>> assert len(links) == 13
        """
        _logger.info("Getting all right column links")
        links = self.__util.get_elements_text(self.__RIGHT_COLUMN_LINKS)
        _logger.debug(f"Found {len(links)} right column links: {links}")
        return links


class Search:
    """
    Component for the global search functionality.
    
    Provides methods to search for products and navigate to results.
    
    Example:
        >>> search = Search(driver, util)
        >>> results = search.search_product("laptop")
        >>> count = results.get_search_result_count()
    """
    
    __SEARCH_FIELD = (By.NAME, "search")
    __SEARCH_BUTTON = (By.CSS_SELECTOR, "input[name='search']+span>button")

    def __init__(self, driver: WebDriver, util: ElementUtil):
        """
        Initialize Search component.
        
        Args:
            driver: Selenium WebDriver instance.
            util: Shared ElementUtil instance.
        """
        self.__driver = driver
        self.__util = util
        _logger.debug("Search component initialized")

    def is_search_field_displayed(self) -> bool:
        """
        Check if the search input field is visible.
        
        Returns:
            bool: True if search field is displayed.
            
        Example:
            >>> assert search.is_search_field_displayed()
        """
        _logger.info("Checking if search field is displayed")
        is_displayed = self.__util.is_element_displayed(self.__SEARCH_FIELD)
        _logger.debug(f"Search field displayed: {is_displayed}")
        return is_displayed

    @allure_step("Searching for product: {product_name}")
    def search_product(self, product_name: str) -> SearchResultPage:
        """
        Search for a product by name.
        
        Enters the search term and clicks the search button,
        returning the search results page.
        
        Args:
            product_name: Product name or search term.
            
        Returns:
            SearchResultPage: Page object for the search results.
            
        Example:
            >>> results = search.search_product("macbook")
            >>> count = results.get_search_result_count()
            >>> assert count > 0
        """
        _logger.info(f"Searching for product: '{product_name}'")
        el = self.__util.wait_for_element_to_be_visible(self.__SEARCH_FIELD, SHORT_WAIT)
        self.__util.enter_text(el, product_name)
        _logger.debug(f"Entered search term: '{product_name}'")
        self.__util.click_element(self.__SEARCH_BUTTON)
        _logger.debug("Clicked search button")
        _logger.info(f"Search completed for: '{product_name}' | Navigating to SearchResultPage")
        return SearchResultPage(self.__driver)
