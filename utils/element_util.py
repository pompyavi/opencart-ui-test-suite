"""
ElementUtil Module
==================

Provides a wrapper around Selenium WebDriver for common element interactions.
Includes methods for finding elements, entering text, clicking, selecting dropdowns,
handling frames, and waiting for conditions.

Features:
    - Automatic element flashing for visual debugging (configurable)
    - Comprehensive logging for all actions
    - Custom exception handling via FrameworkException
    - Support for both locator tuples and WebElement objects

Example:
    >>> util = ElementUtil(driver)
    >>> util.launch_url("https://example.com")
    >>> util.enter_text((By.ID, "username"), "testuser")
    >>> util.click_element((By.ID, "submit"))
"""

import logging
from typing import List, Optional, Union

from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from utils.config_reader import ConfigReader
from utils.framework_exception import FrameworkException
from utils.javascript_util import JSUtil

_logger = logging.getLogger(__name__)


def _format_locator(locator) -> str:
    """
    Format a locator tuple for logging output.
    
    Args:
        locator: A tuple of (By strategy, locator string) or any other object.
        
    Returns:
        str: Formatted string representation of the locator.
        
    Example:
        >>> _format_locator((By.ID, "submit-btn"))
        "(By.ID, 'submit-btn')"
    """
    if isinstance(locator, tuple) and len(locator) == 2:
        return f"({locator[0]}, '{locator[1]}')"
    return str(locator)


class ElementUtil:
    """
    Utility class for Selenium WebDriver element interactions.
    
    Provides a high-level API for common web automation tasks including:
    - Element finding and interaction
    - Text input and retrieval
    - Dropdown selection
    - Frame handling
    - Explicit waits
    
    Attributes:
        driver: The Selenium WebDriver instance.
        
    Example:
        >>> from selenium.webdriver.common.by import By
        >>> util = ElementUtil(driver)
        >>> util.enter_text((By.ID, "email"), "test@example.com")
        >>> util.click_element((By.CSS_SELECTOR, "button[type='submit']"))
    """

    def __init__(self, driver):
        """
        Initialize ElementUtil with a WebDriver instance.
        
        Args:
            driver: Selenium WebDriver instance (Chrome, Firefox, etc.).
            
        Note:
            If 'flash' is enabled in config, elements will be visually
            highlighted when interacted with (useful for debugging).
        """
        self.__driver = driver
        self.__do_flash = ConfigReader.get_config('flash')
        if self.__do_flash:
            self.__js = JSUtil(self.__driver)
        _logger.debug(f"ElementUtil initialized | Flash enabled: {self.__do_flash}")

    # ================== Navigation ==================

    def launch_url(self, url: str) -> None:
        """
        Navigate the browser to the specified URL.
        
        Args:
            url: The URL to navigate to (must include protocol, e.g., https://).
            
        Raises:
            FrameworkException: If URL is empty or None.
            
        Example:
            >>> util.launch_url("https://example.com/login")
        """
        if not url:
            _logger.error("launch_url: URL cannot be empty or null")
            raise FrameworkException('URL cannot be empty or null.')
        _logger.info(f"Navigating to URL: {url}")
        self.__driver.get(url)
        _logger.debug(f"Navigation complete | Current URL: {self.__driver.current_url}")

    # ================== Element Finding ==================

    def get_element(self, locator: tuple) -> WebElement:
        """
        Find a single element using the provided locator.
        
        Args:
            locator: Tuple of (By strategy, locator string).
                     Example: (By.ID, "submit-button")
                     
        Returns:
            WebElement: The found element.
            
        Raises:
            NoSuchElementException: If element is not found.
            
        Example:
            >>> element = util.get_element((By.ID, "username"))
            >>> element.send_keys("testuser")
        """
        _logger.debug(f"Finding element | Locator: {_format_locator(locator)}")
        element = self.__driver.find_element(*locator)
        _logger.debug(f"Element found | Tag: <{element.tag_name}> | Text: '{element.text[:50] if element.text else ''}...'")
        if self.__do_flash:
            self.__js.flash_element(element)
        return element

    def get_elements(self, locator: tuple) -> List[WebElement]:
        """
        Find all elements matching the provided locator.
        
        Args:
            locator: Tuple of (By strategy, locator string).
            
        Returns:
            List[WebElement]: List of matching elements (empty if none found).
            
        Example:
            >>> items = util.get_elements((By.CSS_SELECTOR, ".product-item"))
            >>> print(f"Found {len(items)} products")
        """
        _logger.debug(f"Finding elements | Locator: {_format_locator(locator)}")
        elements = self.__driver.find_elements(*locator)
        _logger.debug(f"Found {len(elements)} elements | Locator: {_format_locator(locator)}")
        return elements

    def get_elements_count(self, locator: tuple) -> int:
        """
        Get the count of elements matching the locator.
        
        Args:
            locator: Tuple of (By strategy, locator string).
            
        Returns:
            int: Number of matching elements.
            
        Example:
            >>> count = util.get_elements_count((By.CSS_SELECTOR, ".cart-item"))
            >>> assert count == 3, "Expected 3 items in cart"
        """
        count = len(self.get_elements(locator))
        _logger.debug(f"Element count: {count} | Locator: {_format_locator(locator)}")
        return count

    # ================== Element Text & Attributes ==================

    def get_element_text(self, locator: tuple) -> str:
        """
        Get the visible text content of an element.
        
        Args:
            locator: Tuple of (By strategy, locator string).
            
        Returns:
            str: The visible text of the element.
            
        Example:
            >>> header = util.get_element_text((By.TAG_NAME, "h1"))
            >>> assert header == "Welcome"
        """
        _logger.debug(f"Getting element text | Locator: {_format_locator(locator)}")
        element = self.get_element(locator)
        text = element.text
        _logger.debug(f"Element text: '{text}'")
        return text

    def get_elements_text(self, locator: tuple) -> List[str]:
        """
        Get the visible text of all elements matching the locator.
        
        Args:
            locator: Tuple of (By strategy, locator string).
            
        Returns:
            List[str]: List of text content from each matching element.
            
        Example:
            >>> menu_items = util.get_elements_text((By.CSS_SELECTOR, ".nav-link"))
            >>> assert "Home" in menu_items
        """
        _logger.debug(f"Getting text from multiple elements | Locator: {_format_locator(locator)}")
        elements = self.get_elements(locator)
        texts = [element.text for element in elements]
        _logger.debug(f"Extracted {len(texts)} text values: {texts[:5]}{'...' if len(texts) > 5 else ''}")
        return texts

    def get_element_attribute(self, locator: tuple, attribute: str) -> Optional[str]:
        """
        Get the value of a DOM attribute from an element.
        
        Args:
            locator: Tuple of (By strategy, locator string).
            attribute: Name of the DOM attribute (e.g., "href", "class", "data-id").
            
        Returns:
            Optional[str]: The attribute value, or None if not present.
            
        Example:
            >>> href = util.get_element_attribute((By.LINK_TEXT, "Click here"), "href")
            >>> print(f"Link points to: {href}")
        """
        _logger.debug(f"Getting attribute '{attribute}' | Locator: {_format_locator(locator)}")
        element = self.get_element(locator)
        value = element.get_dom_attribute(attribute)
        _logger.debug(f"Attribute '{attribute}' = '{value}'")
        return value

    def get_element_property(self, locator: tuple, property_name: str):
        """
        Get the value of a JavaScript property from an element.
        
        Args:
            locator: Tuple of (By strategy, locator string).
            property_name: Name of the JS property (e.g., "value", "checked").
            
        Returns:
            The property value (type depends on property).
            
        Note:
            Properties differ from attributes. For input fields, use "value"
            property instead of "value" attribute to get current value.
            
        Example:
            >>> is_checked = util.get_element_property((By.ID, "agree"), "checked")
        """
        _logger.debug(f"Getting property '{property_name}' | Locator: {_format_locator(locator)}")
        element = self.get_element(locator)
        value = element.get_property(property_name)
        _logger.debug(f"Property '{property_name}' = '{value}'")
        return value

    # ================== Element Interactions ==================

    def enter_text(self, locator: Union[tuple, WebElement], value: str) -> None:
        """
        Clear an input field and enter new text.
        
        Args:
            locator: Either a locator tuple or an existing WebElement.
            value: The text to enter into the field.
            
        Raises:
            FrameworkException: If value is empty or None.
            
        Example:
            >>> util.enter_text((By.ID, "email"), "user@example.com")
            >>> util.enter_text((By.NAME, "password"), "secret123")
        """
        if not value:
            _logger.error("enter_text: Value cannot be empty or null")
            raise FrameworkException('Value cannot be empty or null for entering text.')

        if isinstance(locator, tuple):
            _logger.debug(f"Entering text | Locator: {_format_locator(locator)} | Value: '{value[:20]}{'...' if len(value) > 20 else ''}'")
            element = self.get_element(locator)
        else:
            element = locator
            _logger.debug(f"Entering text into WebElement | Value: '{value[:20]}{'...' if len(value) > 20 else ''}'")

        element.clear()
        _logger.debug("Field cleared")
        element.send_keys(value)
        _logger.debug(f"Text entered successfully | Length: {len(value)} chars")

    def click_element(self, locator: tuple = None, elements: List[WebElement] = None, value: str = None) -> None:
        """
        Click on an element using a locator or by finding text in a list.
        
        Args:
            locator: Optional tuple of (By strategy, locator string).
            elements: Optional list of WebElements to search through.
            value: Text to match when searching through elements list.
            
        Raises:
            FrameworkException: If using elements/value and text is not found.
            
        Example:
            >>> # Click by locator
            >>> util.click_element((By.ID, "submit-btn"))
            >>> 
            >>> # Click by text in list
            >>> buttons = util.get_elements((By.TAG_NAME, "button"))
            >>> util.click_element(elements=buttons, value="Save")
        """
        if locator:
            _logger.info(f"Clicking element | Locator: {_format_locator(locator)}")
            element = self.get_element(locator)
            element.click()
            _logger.debug("Element clicked successfully")
        elif elements and value:
            _logger.info(f"Clicking element with text '{value}' from {len(elements)} elements")
            for element in elements:
                if element.text == value:
                    element.click()
                    _logger.debug(f"Element with text '{value}' clicked successfully")
                    break
            else:
                _logger.error(f"Element with text '{value}' not found in provided elements")
                raise FrameworkException(f"Element with text '{value}' not found in the provided elements.")

    # ================== Element Visibility Checks ==================

    def is_element_displayed(self, element_reference: Union[tuple, WebElement]) -> bool:
        """
        Check if an element is currently visible on the page.
        
        Args:
            element_reference: Either a locator tuple or WebElement.
            
        Returns:
            bool: True if element exists and is visible, False otherwise.
            
        Note:
            This method catches NoSuchElementException and StaleElementReferenceException,
            returning False instead of raising an error.
            
        Example:
            >>> if util.is_element_displayed((By.ID, "error-message")):
            ...     print("Error is shown!")
        """
        try:
            if isinstance(element_reference, tuple):
                _logger.debug(f"Checking visibility | Locator: {_format_locator(element_reference)}")
                el = self.get_element(element_reference)
            else:
                _logger.debug("Checking visibility of WebElement")
                el = element_reference
            is_displayed = el.is_displayed()
            _logger.debug(f"Element displayed: {is_displayed}")
            return is_displayed
        except (NoSuchElementException, StaleElementReferenceException) as e:
            _logger.debug(f"Element not displayed | Exception: {type(e).__name__}")
            return False

    def check_element_displayed(self, locator: tuple) -> bool:
        """
        Check if exactly one element matching the locator exists.
        
        Args:
            locator: Tuple of (By strategy, locator string).
            
        Returns:
            bool: True if exactly one element is found.
            
        Example:
            >>> assert util.check_element_displayed((By.ID, "unique-element"))
        """
        count = len(self.get_elements(locator))
        result = count == 1
        _logger.debug(f"Check element displayed | Found: {count} | Result: {result}")
        return result

    def check_elements_displayed(self, locator: tuple, count: int) -> bool:
        """
        Check if the expected number of elements exist on the page.
        
        Args:
            locator: Tuple of (By strategy, locator string).
            count: Expected number of elements.
            
        Returns:
            bool: True if actual count matches expected count.
            
        Example:
            >>> assert util.check_elements_displayed((By.CSS_SELECTOR, ".tab"), 5)
        """
        elements = self.get_elements(locator)
        result = len(elements) == count
        _logger.debug(f"Check elements count | Expected: {count} | Actual: {len(elements)} | Match: {result}")
        return result

    # ================== Select Dropdown (with Select class) ==================

    def select_option_by_visible_text(self, locator: tuple, text: str) -> None:
        """
        Select a dropdown option by its visible text.
        
        Args:
            locator: Locator for the <select> element.
            text: The visible text of the option to select.
            
        Note:
            Only works with native HTML <select> elements.
            
        Example:
            >>> util.select_option_by_visible_text((By.ID, "country"), "United States")
        """
        _logger.info(f"Selecting option by visible text: '{text}' | Locator: {_format_locator(locator)}")
        element = self.get_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)
        _logger.debug(f"Option '{text}' selected successfully")

    def select_option_by_index(self, locator: tuple, index: int) -> None:
        """
        Select a dropdown option by its index (0-based).
        
        Args:
            locator: Locator for the <select> element.
            index: Zero-based index of the option to select.
            
        Example:
            >>> util.select_option_by_index((By.ID, "month"), 0)  # Select first option
        """
        _logger.info(f"Selecting option by index: {index} | Locator: {_format_locator(locator)}")
        element = self.get_element(locator)
        select = Select(element)
        select.select_by_index(index)
        _logger.debug(f"Option at index {index} selected successfully")

    def select_option_by_value(self, locator: tuple, value: str) -> None:
        """
        Select a dropdown option by its value attribute.
        
        Args:
            locator: Locator for the <select> element.
            value: The value attribute of the option to select.
            
        Example:
            >>> # For <option value="us">United States</option>
            >>> util.select_option_by_value((By.ID, "country"), "us")
        """
        _logger.info(f"Selecting option by value: '{value}' | Locator: {_format_locator(locator)}")
        element = self.get_element(locator)
        select = Select(element)
        select.select_by_value(value)
        _logger.debug(f"Option with value '{value}' selected successfully")

    def get_all_options(self, locator: tuple) -> List[str]:
        """
        Get the text of all options in a dropdown.
        
        Args:
            locator: Locator for the <select> element.
            
        Returns:
            List[str]: Text content of all options.
            
        Example:
            >>> options = util.get_all_options((By.ID, "size"))
            >>> print(options)  # ['Small', 'Medium', 'Large']
        """
        _logger.debug(f"Getting all options | Locator: {_format_locator(locator)}")
        select = Select(self.get_element(locator))
        options = [option.text for option in select.options]
        _logger.debug(f"Found {len(options)} options: {options}")
        return options

    # ================== Select Option (without Select class) ==================

    def select_option(self, locator: tuple, value: str) -> None:
        """
        Select an option by clicking on it (alternative to Select class).
        
        Args:
            locator: Locator for the <select> element.
            value: The visible text of the option to select.
            
        Raises:
            FrameworkException: If option with specified text is not found.
            
        Example:
            >>> util.select_option((By.ID, "priority"), "High")
        """
        _logger.info(f"Selecting option '{value}' | Locator: {_format_locator(locator)}")
        select = Select(self.get_element(locator))
        all_options = select.options
        for option in all_options:
            if option.text == value:
                option.click()
                _logger.debug(f"Option '{value}' clicked successfully")
                break
        else:
            _logger.error(f"Option '{value}' not found in dropdown")
            raise FrameworkException(f"Option with text '{value}' not found in the dropdown.")

    def select_options(self, dropdown_locator: tuple, choices_locator: tuple, *values: str) -> None:
        """
        Select multiple options from a custom (non-native) dropdown.
        
        Args:
            dropdown_locator: Locator for the dropdown trigger element.
            choices_locator: Locator for the option elements within dropdown.
            *values: Variable number of option texts to select.
            
        Raises:
            FrameworkException: If not all specified options are found.
            
        Example:
            >>> util.select_options(
            ...     (By.ID, "multi-select"),
            ...     (By.CSS_SELECTOR, ".dropdown-item"),
            ...     "Option 1", "Option 3"
            ... )
        """
        _logger.info(f"Selecting multiple options: {values} | Dropdown: {_format_locator(dropdown_locator)}")
        self.get_element(dropdown_locator).click()
        _logger.debug("Dropdown opened")

        choices = self.get_elements(choices_locator)
        _logger.debug(f"Found {len(choices)} choices")

        selected_count = 0
        for choice in choices:
            if choice.text in values:
                choice.click()
                selected_count += 1
                _logger.debug(f"Selected: '{choice.text}'")

        if selected_count != len(values):
            _logger.error(f"Not all options selected | Expected: {len(values)} | Selected: {selected_count}")
            raise FrameworkException(f"Not all options were selected. Expected: {len(values)}, Selected: {selected_count}.")

        _logger.info(f"Successfully selected {selected_count} options")

    def select_all_options(self, dropdown_locator: tuple, choices_locator: tuple) -> None:
        """
        Select all available options from a custom dropdown.
        
        Args:
            dropdown_locator: Locator for the dropdown trigger element.
            choices_locator: Locator for the option elements within dropdown.
            
        Example:
            >>> util.select_all_options(
            ...     (By.ID, "multi-select"),
            ...     (By.CSS_SELECTOR, ".dropdown-item")
            ... )
        """
        _logger.info(f"Selecting all options | Dropdown: {_format_locator(dropdown_locator)}")
        self.get_element(dropdown_locator).click()
        _logger.debug("Dropdown opened")

        choices = self.get_elements(choices_locator)
        selected = 0
        for choice in choices:
            if not choice.is_selected():
                choice.click()
                selected += 1
        _logger.info(f"Selected {selected} options (out of {len(choices)} total)")

    # ================== Frame Handling ==================

    def switch_to_frame(self, frame: Union[tuple, WebElement, str, int]) -> None:
        """
        Switch WebDriver context to an iframe.
        
        Args:
            frame: Frame identifier - can be:
                   - tuple: Locator for the iframe element
                   - WebElement: The iframe element itself
                   - str: Frame name or ID
                   - int: Frame index (0-based)
                   
        Raises:
            FrameworkException: If unable to switch to the frame.
            
        Example:
            >>> util.switch_to_frame((By.ID, "content-frame"))
            >>> # or
            >>> util.switch_to_frame("frame-name")
            >>> # or
            >>> util.switch_to_frame(0)  # First frame
        """
        _logger.info(f"Switching to frame: {frame}")
        try:
            if isinstance(frame, tuple):
                frame = self.get_element(frame)
            self.__driver.switch_to.frame(frame)
            _logger.debug("Successfully switched to frame")
        except Exception as e:
            _logger.error(f"Failed to switch to frame: {frame} | Error: {str(e)}")
            raise FrameworkException(f"Failed to switch to frame with: {frame}. Error: {str(e)}")

    def switch_to_default_content(self) -> None:
        """
        Switch back to the main document from any iframe.
        
        Use this after finishing work inside an iframe to return
        to the main page context.
        
        Example:
            >>> util.switch_to_frame((By.ID, "modal-frame"))
            >>> # ... do work in frame ...
            >>> util.switch_to_default_content()
        """
        _logger.info("Switching to default content (main document)")
        self.__driver.switch_to.default_content()
        _logger.debug("Successfully switched to default content")

    def switch_to_parent_frame(self) -> None:
        """
        Switch to the parent frame of the current frame.
        
        Use this when working with nested iframes to go up one level.
        
        Example:
            >>> util.switch_to_frame("outer-frame")
            >>> util.switch_to_frame("inner-frame")
            >>> # ... do work ...
            >>> util.switch_to_parent_frame()  # Back to outer-frame
        """
        _logger.info("Switching to parent frame")
        self.__driver.switch_to.parent_frame()
        _logger.debug("Successfully switched to parent frame")

    # ================== Waits ==================

    def wait_for_element_to_be_visible(self, locator: tuple, timeout: int = 10) -> WebElement:
        """
        Wait for an element to be visible on the page.
        
        Args:
            locator: Tuple of (By strategy, locator string).
            timeout: Maximum seconds to wait (default: 10).
            
        Returns:
            WebElement: The visible element.
            
        Raises:
            FrameworkException: If element is not visible within timeout.
            
        Example:
            >>> element = util.wait_for_element_to_be_visible(
            ...     (By.ID, "loading-complete"),
            ...     timeout=30
            ... )
        """
        _logger.info(f"Waiting for element visibility | Locator: {_format_locator(locator)} | Timeout: {timeout}s")
        wait = WebDriverWait(self.__driver, timeout)
        try:
            element = wait.until(expected_conditions.visibility_of_element_located(locator))
            _logger.debug(f"Element visible | Tag: <{element.tag_name}> | Text: '{element.text[:30] if element.text else ''}...'")
            if self.__do_flash:
                self.__js.flash_element(element)
            return element
        except TimeoutException as e:
            _logger.error(f"Element not visible after {timeout}s | Locator: {_format_locator(locator)}")
            raise FrameworkException(f"Element not visible after {timeout} seconds: {locator}. Error: {str(e)}")

    def wait_for_title_contains(self, fractional_title: str, timeout: int = 10) -> Optional[str]:
        """
        Wait for the page title to contain specific text.
        
        Args:
            fractional_title: Text that should be in the page title.
            timeout: Maximum seconds to wait (default: 10).
            
        Returns:
            Optional[str]: The full page title if matched, None if timeout.
            
        Note:
            This method returns None instead of raising an exception on timeout.
            
        Example:
            >>> title = util.wait_for_title_contains("Dashboard", timeout=15)
            >>> if title:
            ...     print(f"Page loaded: {title}")
        """
        _logger.info(f"Waiting for title to contain: '{fractional_title}' | Timeout: {timeout}s")
        wait = WebDriverWait(self.__driver, timeout)
        try:
            wait.until(expected_conditions.title_contains(fractional_title))
            title = self.__driver.title
            _logger.debug(f"Title matched | Current title: '{title}'")
            return title
        except TimeoutException as e:
            _logger.warning(f"Title does not contain '{fractional_title}' after {timeout}s | Error: {str(e)}")
            return None
