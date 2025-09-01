import pytest
from assertpy import assert_that
from constants.app_constants import ACCOUNT_PAGE_URL, ACCOUNT_PAGE_TITLE, ACCOUNT_HEADERS, \
    RIGHT_COLUMN_LINKS_AFTER_LOGIN, FOOTER_SECTIONS, INFORMATION_SECTION_LINKS


@pytest.mark.usefixtures('setup_account_page')
class TestAccountPage:

    def test_account_page_title(self):
        page_title = self.account_page.get_page_title()
        assert_that(page_title).is_equal_to(ACCOUNT_PAGE_TITLE)

    def test_account_page_url(self):
        page_url = self.account_page.get_page_url()
        assert_that(page_url).is_equal_to(ACCOUNT_PAGE_URL)

    def test_logout_link_exists(self):
        assert_that(self.account_page.is_logout_link_exists()).is_true()

    def test_account_headers(self):
        act_account_headers = self.account_page.get_account_headers()
        assert_that(act_account_headers).is_length(4).is_equal_to(ACCOUNT_HEADERS)

    def test_right_column_links(self):
        right_col_links = self.common_components.right_column_links.get_right_column_links()
        assert_that(right_col_links).is_length(13).is_equal_to(RIGHT_COLUMN_LINKS_AFTER_LOGIN)

    def test_footer_section_exists(self):
        actual_footer_section = self.common_components.footer.get_all_footer_sections_text()
        assert_that(actual_footer_section).is_not_empty().is_equal_to(FOOTER_SECTIONS)

    def test_footer_links_for_section(self):
        footer_links = self.common_components.footer.get_specific_section_footer_links_text('Information')
        assert_that(footer_links).is_not_empty().contains(*INFORMATION_SECTION_LINKS)


