import pytest
from assertpy import assert_that, soft_assertions
from constants.app_constants import FOOTER_SECTIONS, INFORMATION_SECTION_LINKS
from constants.test_data import SEARCH_TESTDATA

@pytest.mark.skip(reason="Skipping search result page tests temporarily")
@pytest.mark.usefixtures('setup_account_page')
class TestSearchResultsPage:

    def test_search_field_exists(self):
        assert_that(self.common_components.search.is_search_field_displayed()).is_true()

    @pytest.mark.parametrize('search_term, expected_count', SEARCH_TESTDATA['empty_results']+SEARCH_TESTDATA['product_results'])
    def test_search_functionality(self, search_term, expected_count):
        search_results = self.common_components.search.search_product(search_term)
        with soft_assertions():
            assert_that(search_results.get_search_result_count()).is_equal_to(expected_count)
            assert_that(search_results.get_search_result_header()).contains(search_term)

    def test_footer_section_exists(self):
        actual_footer_section = self.common_components.footer.get_all_footer_sections_text()
        assert_that(actual_footer_section).is_not_empty().is_equal_to(FOOTER_SECTIONS)

    def test_footer_links_for_section(self):
        footer_links = self.common_components.footer.get_specific_section_footer_links_text('Information')
        assert_that(footer_links).is_not_empty().contains(*INFORMATION_SECTION_LINKS)
