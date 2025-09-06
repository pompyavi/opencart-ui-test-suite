import pytest
from constants import app_constants
from assertpy import assert_that
from utils.config_reader import ConfigReader

@pytest.mark.login
@pytest.mark.usefixtures('setup_login_page')
class TestLoginPage:

    # Pytest instantiates the class before fixtures run. In your __init__,
    # you call LoginPage(self.driver) but self.driver is set by the fixture after
    # instantiation (request.cls.driver), so collection breaks and you end up with
    # “no tests found/collected”.

    # def __init__(self):
    #     self.login_page = LoginPage(self.driver)

    def test_login_page_title(self):
        actual_title = self.login_page.get_page_title()
        assert_that(actual_title).is_not_empty().is_equal_to(app_constants.LOGIN_PAGE_TITLE)

    def test_login_page_url(self):
        actual_url = self.login_page.get_page_url()
        assert_that(actual_url).is_not_empty().is_equal_to(app_constants.LOGIN_PAGE_URL)

    def test_forgot_password_link_exists(self):
        assert_that(self.login_page.does_forgot_password_link_exists()).is_true()

    def test_right_column_links(self):
        right_col_links = self.common_components.right_column_links.get_right_column_links()
        assert_that(right_col_links).is_length(13).is_equal_to(app_constants.RIGHT_COLUMN_LINKS_BEFORE_LOGIN)

    def test_footer_section_exists(self):
        actual_footer_section = self.common_components.footer.get_all_footer_sections_text()
        assert_that(actual_footer_section).is_not_empty().is_equal_to(app_constants.FOOTER_SECTIONS)

    def test_login(self):
        creds = ConfigReader.get_config('credentials')
        account_page = self.login_page.do_login(creds.get('email'), creds.get('password'))
        assert_that(account_page.is_logout_link_exists()).is_true()


