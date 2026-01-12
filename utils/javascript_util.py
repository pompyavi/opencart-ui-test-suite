"""
JavaScript Utility Module
=========================

Provides JavaScript execution capabilities for Selenium WebDriver.
Useful for actions that are difficult with standard Selenium methods.

Features:
    - Page scrolling (to top, bottom, specific position)
    - Element scrolling into view
    - JavaScript-based clicks (for hidden elements)
    - Direct value setting via JavaScript
    - Page navigation (back, forward, refresh)
    - Visual element highlighting (flash effect)

Example:
    >>> js = JSUtil(driver)
    >>> js.scroll_to_bottom()
    >>> js.click_element(hidden_button)
    >>> js.flash_element(target_element)  # Visual debugging
"""

import time
from selenium.webdriver.remote.webelement import WebElement


class JSUtil:
    """
    Utility class for JavaScript-based browser interactions.
    
    Executes JavaScript directly in the browser for operations
    that may be difficult or impossible with standard WebDriver methods.
    
    Attributes:
        driver: Selenium WebDriver instance.
        
    Example:
        >>> js = JSUtil(driver)
        >>> js.scroll_to_bottom()
        >>> js.click_element(element)
    """

    def __init__(self, driver):
        """
        Initialize JSUtil with a WebDriver instance.
        
        Args:
            driver: Selenium WebDriver instance.
        """
        self.__driver = driver

    # ================== Scrolling ==================

    def scroll_to_bottom(self) -> None:
        """
        Scroll to the bottom of the page.
        
        Useful for loading lazy-loaded content or reaching
        footer elements.
        
        Example:
            >>> js.scroll_to_bottom()
        """
        self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_top(self) -> None:
        """
        Scroll to the top of the page.
        
        Example:
            >>> js.scroll_to_top()
        """
        self.__driver.execute_script("window.scrollTo(0, 0);")

    def scroll_by(self, x: int, y: int) -> None:
        """
        Scroll by a relative amount from current position.
        
        Args:
            x: Pixels to scroll horizontally (positive = right).
            y: Pixels to scroll vertically (positive = down).
            
        Example:
            >>> js.scroll_by(0, 500)  # Scroll down 500px
            >>> js.scroll_by(100, 0)  # Scroll right 100px
        """
        self.__driver.execute_script(f"window.scrollBy({x}, {y});")

    def scroll_into_view(self, element: WebElement) -> None:
        """
        Scroll the page so the element is visible in the viewport.
        
        Args:
            element: WebElement to scroll into view.
            
        Example:
            >>> button = driver.find_element(By.ID, "submit")
            >>> js.scroll_into_view(button)
            >>> button.click()
        """
        self.__driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_to_position(self, x: int, y: int) -> None:
        """
        Scroll to an absolute position on the page.
        
        Args:
            x: Absolute horizontal position in pixels.
            y: Absolute vertical position in pixels.
            
        Example:
            >>> js.scroll_to_position(0, 1000)  # Scroll to y=1000
        """
        self.__driver.execute_script(f"window.scrollTo({x}, {y});")

    # ================== Element Interactions ==================

    def click_element(self, element: WebElement) -> None:
        """
        Click an element using JavaScript.
        
        Useful for clicking elements that are hidden, overlapped,
        or not clickable via standard WebDriver click.
        
        Args:
            element: WebElement to click.
            
        Example:
            >>> hidden_button = driver.find_element(By.ID, "hidden-submit")
            >>> js.click_element(hidden_button)
        """
        self.__driver.execute_script("arguments[0].click();", element)

    def send_keys(self, element: WebElement, value: str) -> None:
        """
        Set the value of an input element directly via JavaScript.
        
        Bypasses normal key events, directly setting the element's
        value property. May not trigger all event handlers.
        
        Args:
            element: Input WebElement.
            value: Value to set.
            
        Example:
            >>> input_field = driver.find_element(By.ID, "quantity")
            >>> js.send_keys(input_field, "100")
        """
        self.__driver.execute_script("arguments[0].value = arguments[1];", element, value)

    # ================== Page Information ==================

    def get_page_title(self) -> str:
        """
        Get the page title using JavaScript.
        
        Returns:
            str: The document title.
            
        Example:
            >>> title = js.get_page_title()
        """
        return self.__driver.execute_script("return document.title;")

    # ================== Navigation ==================

    def refresh_page(self) -> None:
        """
        Refresh the current page using JavaScript.
        
        Example:
            >>> js.refresh_page()
        """
        self.__driver.execute_script("location.reload();")

    def go_back(self) -> None:
        """
        Navigate back to the previous page in browser history.
        
        Example:
            >>> js.go_back()
        """
        self.__driver.execute_script("window.history.back();")

    def go_forward(self) -> None:
        """
        Navigate forward to the next page in browser history.
        
        Example:
            >>> js.go_forward()
        """
        self.__driver.execute_script("window.history.forward();")

    # ================== Visual Debugging ==================

    def get_bg_color(self, element: WebElement) -> str:
        """
        Get the background color of an element.
        
        Args:
            element: WebElement to inspect.
            
        Returns:
            str: CSS background color value (e.g., "rgb(255, 255, 255)").
            
        Example:
            >>> color = js.get_bg_color(button)
            >>> print(color)  # "rgb(0, 123, 255)"
        """
        return self.__driver.execute_script(
            "return window.getComputedStyle(arguments[0]).backgroundColor;", element
        )

    def change_bg_color(self, element: WebElement, color: str) -> None:
        """
        Change the background color of an element.
        
        Args:
            element: WebElement to modify.
            color: CSS color value (e.g., "red", "#ff0000", "rgb(255,0,0)").
            
        Example:
            >>> js.change_bg_color(button, "yellow")
        """
        self.__driver.execute_script(
            "arguments[0].style.backgroundColor = arguments[1];", element, color
        )

    def flash_element(self, element: WebElement) -> None:
        """
        Visually highlight an element by flashing its background color.
        
        Useful for debugging to visually identify which element
        the automation is interacting with.
        
        Args:
            element: WebElement to flash.
            
        Note:
            This method introduces a small delay (1 second total)
            as it flashes the element 20 times with 0.05s intervals.
            Use only for debugging, not in production tests.
            
        Example:
            >>> submit_button = driver.find_element(By.ID, "submit")
            >>> js.flash_element(submit_button)  # Flashes green
            >>> submit_button.click()
        """
        bg_color = self.get_bg_color(element)
        for i in range(20):
            self.change_bg_color(element, 'lightgreen')
            time.sleep(0.05)
            self.change_bg_color(element, bg_color)
