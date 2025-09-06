import allure
import pytest
from assertpy import assert_that, soft_assertions

from constants import app_constants
from constants.app_constants import FOOTER_SECTIONS, INFORMATION_SECTION_LINKS
from constants.test_data import PRODUCT_TEST_DATA

@pytest.mark.product
@pytest.mark.usefixtures('setup_account_page')
class TestProductPage:

    @allure.title("Verify product info for various products")
    @allure.description("This test verifies that the product information displayed on the product page matches the expected details for various products.")
    @pytest.mark.parametrize('search_term, product_name', PRODUCT_TEST_DATA['macbook_products']+PRODUCT_TEST_DATA['samsung_products'])
    def test_product_info(self, search_term, product_name):
        search_results = self.common_components.search.search_product(search_term)
        product_page = search_results.select_product(product_name)
        actual_product_info = product_page.get_product_complete_info()
        assert_that(actual_product_info).is_equal_to(app_constants.PRODUCTS_INFO[product_name])

    @pytest.mark.parametrize('search_term, product_name', PRODUCT_TEST_DATA['macbook_products']+PRODUCT_TEST_DATA['samsung_products'])
    def test_product_images_displayed(self, search_term, product_name):
        search_results = self.common_components.search.search_product(search_term)
        product_page = search_results.select_product(product_name)
        assert_that(product_page.get_product_images_count()).is_greater_than(0)
        assert_that(product_page.are_product_images_displayed()).is_true()

    def test_footer_section_exists(self):
        actual_footer_section = self.common_components.footer.get_all_footer_sections_text()
        assert_that(actual_footer_section).is_not_empty().is_equal_to(FOOTER_SECTIONS)

    def test_footer_links_for_section(self):
        footer_links = self.common_components.footer.get_specific_section_footer_links_text('Information')
        assert_that(footer_links).is_not_empty().contains(*INFORMATION_SECTION_LINKS)