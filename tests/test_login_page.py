"""
Login Page Tests
================

Test suite for the OpenCart login page functionality.
Validates page elements, navigation links, and user authentication.

Test Coverage:
    - Page title and URL verification
    - Forgot password link visibility
    - Right column navigation links
    - Footer sections
    - User login functionality

Fixtures Used:
    - setup_login_page: Initializes LoginPage and navigates to login URL

Markers:
    - @pytest.mark.login: Category marker for login-related tests
"""

import pytest
from assertpy import assert_that

from constants import app_constants
from utils.config_reader import ConfigReader


@pytest.mark.login
@pytest.mark.usefixtures('setup_login_page')
class TestLoginPage:
    """
    Test class for Login Page functionality.
    
    Uses the setup_login_page fixture which provides:
        - self.login_page: LoginPage instance
        - self.common_components: CommonComponents instance
        - self.driver: WebDriver instance
        
    Example:
        pytest tests/test_login_page.py -v --browser chrome
    """

    def test_login_page_title(self):
        """Verify the login page displays the correct title."""
        actual_title = self.login_page.get_page_title()
        assert_that(actual_title).is_not_empty().is_equal_to(app_constants.LOGIN_PAGE_TITLE)

    def test_login_page_url(self):
        """Verify the login page URL matches expected URL."""
        actual_url = self.login_page.get_page_url()
        assert_that(actual_url).is_not_empty().is_equal_to(app_constants.LOGIN_PAGE_URL)

    def test_forgot_password_link_exists(self):
        """Verify the 'Forgotten Password' link is visible on the page."""
        assert_that(self.login_page.does_forgot_password_link_exists()).is_true()

    def test_right_column_links(self):
        """Verify all expected right column navigation links are present."""
        right_col_links = self.common_components.right_column_links.get_right_column_links()
        assert_that(right_col_links).is_length(13).is_equal_to(
            app_constants.RIGHT_COLUMN_LINKS_BEFORE_LOGIN
        )

    def test_footer_section_exists(self):
        """Verify all footer sections are displayed correctly."""
        actual_footer_section = self.common_components.footer.get_all_footer_sections_text()
        assert_that(actual_footer_section).is_not_empty().is_equal_to(
            app_constants.FOOTER_SECTIONS
        )

    def test_login(self):
        """
        Verify successful user login with valid credentials.
        
        Steps:
            1. Get credentials from config
            2. Perform login
            3. Verify logout link is visible (indicates successful login)
        """
        creds = ConfigReader.get_config('credentials')
        account_page = self.login_page.do_login(
            creds.get('email'), creds.get('password')
        )
        assert_that(account_page.is_logout_link_exists()).is_true()
