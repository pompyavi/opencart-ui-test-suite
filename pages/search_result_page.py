"""
Search Result Page Module
=========================

Page Object Model implementation for the OpenCart Search Results page.
Displays products matching a search query and allows navigation to
individual product pages.

Features:
    - Search result count retrieval
    - Search header verification
    - Product selection from results

Example:
    >>> results = common_components.search.search_product("macbook")
    >>> count = results.get_search_result_count()
    >>> product_page = results.select_product("MacBook Pro")
"""

import logging

from selenium.webdriver.common.by import By

from constants.app_constants import SHORT_WAIT
from pages.product_page import ProductPage
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


class SearchResultPage:
    """
    Page Object for the OpenCart Search Results page.
    
    Displays products matching a search query and provides methods
    to verify results and navigate to product detail pages.
    
    Attributes:
        driver: Selenium WebDriver instance.
        
    Example:
        >>> results = SearchResultPage(driver)
        >>> print(f"Found {results.get_search_result_count()} products")
        >>> product = results.select_product("MacBook Air")
    """

    # Locators
    __SEARCH_RESULT_HEADER = (By.CSS_SELECTOR, "#content h1")
    __SEARCH_RESULT_COUNT = (By.CSS_SELECTOR, "div[class='row'] div[class='product-thumb']")

    def __init__(self, driver):
        """
        Initialize SearchResultPage with the current driver state.
        
        Args:
            driver: Selenium WebDriver instance (should already be on search results).
        """
        self.__driver = driver
        self.__util = ElementUtil(self.__driver)
        _logger.info(f"SearchResultPage: Initialized | URL: {self.__driver.current_url} | Title: {self.__driver.title}")

    def get_search_result_header(self) -> str:
        """
        Get the search result page header text.
        
        Returns:
            str: Header text (e.g., "Search - macbook").
            
        Example:
            >>> header = results.get_search_result_header()
            >>> assert "macbook" in header.lower()
        """
        _logger.info("SearchResultPage: Getting search result header")
        header = self.__util.get_element_text(self.__SEARCH_RESULT_HEADER)
        _logger.debug(f"SearchResultPage: Header text: '{header}'")
        return header

    def get_search_result_count(self) -> int:
        """
        Count the number of products in the search results.
        
        Returns:
            int: Number of product thumbnails displayed.
            
        Example:
            >>> count = results.get_search_result_count()
            >>> assert count > 0, "No products found"
        """
        _logger.info("SearchResultPage: Counting search results")
        count = self.__util.get_elements_count(self.__SEARCH_RESULT_COUNT)
        _logger.debug(f"SearchResultPage: Found {count} product results")
        return count

    @allure_step("Selecting product '{product_name}' from search results")
    def select_product(self, product_name: str) -> ProductPage:
        """
        Select a product from search results by clicking its link.
        
        Args:
            product_name: Exact name of the product to select.
            
        Returns:
            ProductPage: Page object for the selected product's detail page.
            
        Example:
            >>> product_page = results.select_product("MacBook Pro")
            >>> info = product_page.get_product_complete_info()
        """
        _logger.info(f"SearchResultPage: Selecting product: '{product_name}'")
        product_link = (By.LINK_TEXT, product_name)
        element = self.__util.wait_for_element_to_be_visible(product_link, SHORT_WAIT)
        _logger.debug(f"SearchResultPage: Product link found, clicking: '{product_name}'")
        element.click()
        _logger.info(f"SearchResultPage: Product selected | Navigating to ProductPage for: '{product_name}'")
        return ProductPage(self.__driver)
