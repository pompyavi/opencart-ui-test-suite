import logging

from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from utils.config_reader import ConfigReader
from utils.framework_exception import FrameworkException
from utils.javascript_util import JSUtil


class ElementUtil:

    def __init__(self, driver):
        self.__driver = driver
        self.__do_flash = ConfigReader.get_config('flash')
        self.__logger = logging.getLogger(__name__)
        if self.__do_flash:
            self.__js = JSUtil(self.__driver)

    def launch_url(self, url):
        if not url:
            raise FrameworkException('URL cannot be empty or null.')
        self.__driver.get(url)

    def get_element(self, locator):
        element = self.__driver.find_element(*locator)
        if self.__do_flash:
            self.__js.flash_element(element)
        return element

    def enter_text(self, locator, value):
        if not value:
            raise FrameworkException('Value cannot be empty or null for entering text.')

        if isinstance(locator, tuple):
            locator = self.get_element(locator)
        locator.clear()
        locator.send_keys(value)

    def click_element(self, locator=None, elements=None, value=None):
        if locator:
            element = self.get_element(locator)
            element.click()
        elif elements and value:
            for element in elements:
                if element.text == value:
                    element.click()
                    break
            else:
                raise FrameworkException(f"Element with text '{value}' not found in the provided elements.")


    def get_element_text(self, locator):
        element = self.get_element(locator)
        return element.text

    def get_element_attribute(self, locator, attribute):
        element = self.get_element(locator)
        return element.get_dom_attribute(attribute)

    def get_element_property(self, locator, property_name):
        element = self.get_element(locator)
        return element.get_property(property_name)

    def is_element_displayed(self, element_reference):
        try:
            el = self.get_element(element_reference) if isinstance(element_reference, tuple) else element_reference
            return el.is_displayed()
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def check_element_displayed(self, locator):
        return len(self.get_elements(locator)) == 1

    def check_elements_displayed(self, locator, count):
        elements = self.get_elements(locator)
        if len(elements) == count:
            return True
        return False

    def get_elements(self, locator):
        self.__logger.debug(f"Getting elements with locator: {locator}")
        return self.__driver.find_elements(*locator)

    def get_elements_count(self, locator):
        return len(self.get_elements(locator))

    def get_elements_text(self, locator):
        elements = self.get_elements(locator)
        return [element.text for element in elements]

# ==============select based dropdown===========================

    def select_option_by_visible_text(self, locator, text):
        element = self.get_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)

    def select_option_by_index(self, locator, index):
        element = self.get_element(locator)
        select = Select(element)
        select.select_by_index(index)

    def select_option_by_value(self, locator, value):
        element = self.get_element(locator)
        select = Select(element)
        select.select_by_value(value)

    def get_all_options(self, locator):
        select = Select(self.get_element(locator))
        return [option.text for option in select.options]

#============== select option without select class =========================
    def select_option(self, locator, value):
        select = Select(self.get_element(locator))
        all_options = select.options
        for option in all_options:
            if option.text == value:
                option.click()
                break
        else:
            raise FrameworkException(f"Option with text '{value}' not found in the dropdown.")

    def select_options(self, dropdown_locator, choices_locator, *values):
        self.get_element(dropdown_locator).click()  # Ensure the dropdown is open
        choices = self.get_elements(choices_locator)
        selected_count = 0
        for choice in choices:
            if choice.text in values:
                choice.click()
                selected_count += 1

        if selected_count != len(values):
            raise FrameworkException(f"Not all options were selected. Expected: {len(values)}, Selected: {selected_count}.")

    def select_all_options(self, dropdown_locator, choices_locator):
        self.get_element(dropdown_locator).click()
        choices = self.get_elements(choices_locator)
        for choice in choices:
            if not choice.is_selected():
                choice.click()

#================Frame Handling========================

    def switch_to_frame(self, frame):
        try:
            if isinstance(frame, tuple):
                frame = self.get_element(frame)
            self.__driver.switch_to.frame(frame)
        except Exception as e:
            raise FrameworkException(f"Failed to switch to frame with: {frame}. Error: {str(e)}")

    def switch_to_default_content(self):
        self.__driver.switch_to.default_content()

    def switch_to_parent_frame(self):
        self.__driver.switch_to.parent_frame()

#================Waits========================

    def wait_for_element_to_be_visible(self, locator, timeout=10):
        wait = WebDriverWait(self.__driver, timeout)
        try:
            element = wait.until(expected_conditions.visibility_of_element_located(locator))
            if self.__do_flash:
                self.__js.flash_element(element)
            return element
        except TimeoutException as e:
            raise FrameworkException(f"Element not visible after {timeout} seconds: {locator}. Error: {str(e)}")

    def wait_for_title_contains(self, fractional_title, timeout=10):
        wait = WebDriverWait(self.__driver, timeout)
        try:
            wait.until(expected_conditions.title_contains(fractional_title))
            return self.__driver.title
        except TimeoutException as e:
            print(f"Title does not contain '{fractional_title}' after {timeout} seconds. Error: {str(e)}")
            return None



