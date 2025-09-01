import allure
from selenium.webdriver.common.by import By
from utils.element_util import ElementUtil


class ProductPage:
    # Locators
    __PRODUCT_HEADER = (By.CSS_SELECTOR, "#content h1")
    __PRODUCT_IMAGES = (By.CSS_SELECTOR, ".thumbnails a > img")
    __ADD_TO_CART_BTN = (By.ID, "button-cart")
    __WISHLIST_BTN = (By.XPATH, "//button[@data-original-title='Add to Wish List']")
    __PRODUCT_META_DATA = (By.CSS_SELECTOR, ".col-sm-4 > ul:nth-of-type(1) > li")
    __PRODUCT_PRICE = (By.CSS_SELECTOR, ".col-sm-4 > ul:nth-of-type(2) > li")

    def __init__(self, driver):
        self.__driver = driver
        self.__util = ElementUtil(self.__driver)
        self.__product_info_map = {}

    def get_page_title(self) -> str:
        return self.__driver.title

    def get_product_images_count(self) -> int:
        return self.__util.get_elements_count(self.__PRODUCT_IMAGES)

    def are_product_images_displayed(self) -> bool:
        images = self.__util.get_elements(self.__PRODUCT_IMAGES)
        for img in images:
            if not self.__util.is_element_displayed(img):
                return False
        return True

    @allure.step("Getting complete product info")
    def get_product_complete_info(self):
        """
        Builds and returns a dict like:
        {
            "productHeader": "...",
            "Brand": "...",
            "Product Code": "...",
            "Reward Points": "...",
            "Availability": "...",
            "price": "£... ",
            "Ex Tax": "£..."
        }
        """
        self.__product_info_map["productHeader"] = self.__util.get_element_text(self.__PRODUCT_HEADER)
        self.__get_product_meta_data()
        self.__get_product_price_data()
        return self.__product_info_map

# ---------- Private helpers ----------

    @allure.step("Getting product meta data")
    def __get_product_meta_data(self) -> None:
        meta_list = self.__util.get_elements_text(self.__PRODUCT_META_DATA)
        for meta in meta_list:
            parts = meta.split(":")
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                self.__product_info_map[key] = value

    @allure.step("Getting product price data")
    def __get_product_price_data(self) -> None:
        price_list = self.__util.get_elements_text(self.__PRODUCT_PRICE)
        if not price_list:
            return
        # First item: price
        self.__product_info_map["price"] = price_list[0].strip()
        # Second item: e.g., "Ex Tax: £368.73"
        if len(price_list) > 1:
            parts = price_list[1].split(":")
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                self.__product_info_map[key] = value
