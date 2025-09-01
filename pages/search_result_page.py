import allure
from selenium.webdriver.common.by import By
from constants.app_constants import SHORT_WAIT
from pages.product_page import ProductPage
from utils.element_util import ElementUtil


class SearchResultPage:
    """
        Represents the Search Result page of the application.
        Provides functionality to retrieve search results information
        and to select a product from the results.
    """

    # Locators
    __SEARCH_RESULT_HEADER = By.CSS_SELECTOR, "#content h1"
    __SEARCH_RESULT_COUNT = By.CSS_SELECTOR, "div[class='row'] div[class='product-thumb']"

    def __init__(self, driver):
        self.__driver = driver
        self.__util = ElementUtil(self.__driver)

    def get_search_result_header(self) -> str:
        """
        Retrieves the text of the search result header.
        Example: "Search - macbook"
        """
        return self.__util.get_element_text(self.__SEARCH_RESULT_HEADER)

    def get_search_result_count(self) -> int:
        """
        Counts the number of product thumbnails displayed in the search results.
        """
        return self.__util.get_elements_count(self.__SEARCH_RESULT_COUNT)

    @allure.step("Selecting product '{product_name}' from search results")
    def select_product(self, product_name: str):
        """
        Selects a product from the search results by clicking its visible link text.
        Returns:
            ProductPage instance representing the selected product's detail page.
        """
        product_link = By.LINK_TEXT, product_name
        element = self.__util.wait_for_element_to_be_visible(product_link, SHORT_WAIT)
        element.click()
        return ProductPage(self.__driver)

