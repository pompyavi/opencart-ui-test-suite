"""
Product Page Module
===================

Page Object Model implementation for the OpenCart Product Detail page.
Provides methods for extracting product information including name,
price, metadata, and images.

Features:
    - Product information extraction (name, brand, price, availability)
    - Product image verification
    - Allure integration for test reporting

Example:
    >>> product_page = search_results.select_product("MacBook Pro")
    >>> info = product_page.get_product_complete_info()
    >>> assert info["Brand"] == "Apple"
"""

import logging
from typing import Dict

from selenium.webdriver.common.by import By

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
    
    If Allure is not installed, the decorator is a no-op and the
    function executes normally without any modifications.
    
    Args:
        step_text: Description of the step for Allure reports.
        
    Returns:
        Decorated function with Allure step, or original function.
        
    Example:
        >>> @allure_step("Clicking submit button")
        ... def click_submit(self):
        ...     self.driver.find_element(...).click()
    """
    def decorator(func):
        if _ALLURE:
            return allure.step(step_text)(func)
        return func
    return decorator


_logger = logging.getLogger(__name__)


class ProductPage:
    """
    Page Object for the OpenCart Product Detail page.
    
    Provides methods to extract and verify product information
    including headers, metadata, pricing, and images.
    
    Attributes:
        driver: Selenium WebDriver instance.
        
    Example:
        >>> product_page = ProductPage(driver)
        >>> info = product_page.get_product_complete_info()
        >>> print(f"Product: {info['productHeader']}, Price: {info['price']}")
    """
    
    # Locators
    __PRODUCT_HEADER = (By.CSS_SELECTOR, "#content h1")
    __PRODUCT_IMAGES = (By.CSS_SELECTOR, ".thumbnails a > img")
    __ADD_TO_CART_BTN = (By.ID, "button-cart")
    __WISHLIST_BTN = (By.XPATH, "//button[@data-original-title='Add to Wish List']")
    __PRODUCT_META_DATA = (By.CSS_SELECTOR, ".col-sm-4 > ul:nth-of-type(1) > li")
    __PRODUCT_PRICE = (By.CSS_SELECTOR, ".col-sm-4 > ul:nth-of-type(2) > li")

    def __init__(self, driver):
        """
        Initialize ProductPage with the current driver state.
        
        Args:
            driver: Selenium WebDriver instance (should already be on product page).
        """
        self.__driver = driver
        self.__util = ElementUtil(self.__driver)
        self.__product_info_map: Dict[str, str] = {}
        _logger.info(f"ProductPage: Initialized | URL: {self.__driver.current_url} | Title: {self.__driver.title}")

    def get_page_title(self) -> str:
        """
        Get the current page title.
        
        Returns:
            str: The browser's current page title (typically the product name).
            
        Example:
            >>> title = product_page.get_page_title()
            >>> assert "MacBook" in title
        """
        title = self.__driver.title
        _logger.debug(f"ProductPage: Retrieved page title: '{title}'")
        return title

    def get_product_images_count(self) -> int:
        """
        Count the number of product images displayed.
        
        Returns:
            int: Number of product thumbnail images.
            
        Example:
            >>> count = product_page.get_product_images_count()
            >>> assert count >= 1, "Product should have at least one image"
        """
        _logger.info("ProductPage: Counting product images")
        count = self.__util.get_elements_count(self.__PRODUCT_IMAGES)
        _logger.debug(f"ProductPage: Found {count} product images")
        return count

    def are_product_images_displayed(self) -> bool:
        """
        Verify all product images are visible on the page.
        
        Returns:
            bool: True if all images are displayed, False if any is hidden.
            
        Example:
            >>> assert product_page.are_product_images_displayed()
        """
        _logger.info("ProductPage: Checking if all product images are displayed")
        images = self.__util.get_elements(self.__PRODUCT_IMAGES)
        for idx, img in enumerate(images):
            if not self.__util.is_element_displayed(img):
                _logger.warning(f"ProductPage: Image at index {idx} is NOT displayed")
                return False
        _logger.debug(f"ProductPage: All {len(images)} images are displayed")
        return True

    @allure_step("Getting complete product info")
    def get_product_complete_info(self) -> Dict[str, str]:
        """
        Extract complete product information from the page.
        
        Gathers product header, metadata (brand, availability, product code,
        reward points), and pricing information.
        
        Returns:
            Dict[str, str]: Dictionary containing product information:
                - productHeader: Product name
                - Brand: Manufacturer (if available)
                - Product Code: SKU/code
                - Reward Points: Points earned on purchase
                - Availability: Stock status
                - price: Display price
                - Ex Tax: Price before tax
                
        Example:
            >>> info = product_page.get_product_complete_info()
            >>> print(info)
            {
                "productHeader": "MacBook Pro",
                "Brand": "Apple",
                "Product Code": "Product 18",
                "Availability": "In Stock",
                "price": "$2,000.00",
                "Ex Tax": "$2,000.00"
            }
        """
        _logger.info("ProductPage: Extracting complete product information")
        self.__product_info_map["productHeader"] = self.__util.get_element_text(self.__PRODUCT_HEADER)
        _logger.debug(f"ProductPage: Product Header: '{self.__product_info_map['productHeader']}'")

        self.__get_product_meta_data()
        self.__get_product_price_data()

        _logger.info(f"ProductPage: Product info extracted | Data: {self.__product_info_map}")
        return self.__product_info_map

    @allure_step("Getting product meta data")
    def __get_product_meta_data(self) -> None:
        """
        Extract product metadata (Brand, Code, Points, Availability).
        
        Parses the metadata list items and adds key-value pairs
        to the product info map.
        """
        _logger.debug("ProductPage: Extracting product metadata (Brand, Code, Points, Availability)")
        meta_list = self.__util.get_elements_text(self.__PRODUCT_META_DATA)
        for meta in meta_list:
            parts = meta.split(":")
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                self.__product_info_map[key] = value
                _logger.debug(f"ProductPage: Metadata | {key}: {value}")

    @allure_step("Getting product price data")
    def __get_product_price_data(self) -> None:
        """
        Extract product pricing information.
        
        Parses the price display and tax information,
        adding them to the product info map.
        """
        _logger.debug("ProductPage: Extracting product price data")
        price_list = self.__util.get_elements_text(self.__PRODUCT_PRICE)
        if not price_list:
            _logger.warning("ProductPage: No price data found")
            return

        self.__product_info_map["price"] = price_list[0].strip()
        _logger.debug(f"ProductPage: Price: {self.__product_info_map['price']}")

        if len(price_list) > 1:
            parts = price_list[1].split(":")
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                self.__product_info_map[key] = value
                _logger.debug(f"ProductPage: {key}: {value}")
