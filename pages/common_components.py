from functools import cached_property
from typing import List

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from constants.app_constants import SHORT_WAIT
from pages.search_result_page import SearchResultPage
from utils.element_util import ElementUtil


class CommonComponents:
    def __init__(self, driver):
        self.__driver = driver
        self.__util = ElementUtil(self.__driver)

    # --- lazy components: instantiated on first access only ---
    @cached_property
    def footer(self) -> "Footer":
        return Footer(self.__driver, self.__util)

    @cached_property
    def right_column_links(self) -> 'RightColumnLinks':
        return RightColumnLinks(self.__driver, self.__util)

    @cached_property
    def search(self) -> 'Search':
        return Search(self.__driver, self.__util)

class Footer:
    __FOOTER_SECTION = By.XPATH, "//footer//h5"
    __FOOTER_LINKS = By.XPATH, "./following-sibling::ul//a"

    def __init__(self, driver, element_util):
        self.__driver = driver
        self.__util = element_util

    def get_all_footer_sections_text(self) -> List[str]:
        return self.__util.get_elements_text(self.__FOOTER_SECTION)

    def get_footer_links_text(self) -> List[str]:
        sections: List[WebElement] = self.__util.get_elements(self.__FOOTER_SECTION)
        texts: List[str] = []
        for section in sections:
            links = section.find_elements(*self.__FOOTER_LINKS)
            for link in links:
                texts.append(link.text)
        return texts

    def get_specific_section_footer_links_text(self, section: str) -> List[str]:
        section_links = (
            By.XPATH,
            f"//footer//h5[text()='{section}']/following-sibling::ul//a",
        )
        return self.__util.get_elements_text(section_links)

class RightColumnLinks:
    __RIGHT_COLUMN_LINKS = By.CSS_SELECTOR, '#column-right a'

    def __init__(self, driver, element_util):
        self.__driver = driver
        self.__util = element_util

    def get_right_column_links(self) -> List[str]:
        return self.__util.get_elements_text(self.__RIGHT_COLUMN_LINKS)

class Search:
    __SEARCH_FIELD  = (By.NAME, "search")
    __SEARCH_BUTTON = (By.CSS_SELECTOR, "input[name='search']+span>button")

    def __init__(self, driver: WebDriver, util: ElementUtil):
        self.__driver = driver
        self.__util = util

    def is_search_field_displayed(self) -> bool:
        return self.__util.is_element_displayed(self.__SEARCH_FIELD)

    @allure.step("Searching for product: {product_name}")
    def search_product(self, product_name: str):
        el = self.__util.wait_for_element_to_be_visible(self.__SEARCH_FIELD, SHORT_WAIT)
        self.__util.enter_text(el, product_name)
        self.__util.click_element(self.__SEARCH_BUTTON)
        return SearchResultPage(self.__driver)

