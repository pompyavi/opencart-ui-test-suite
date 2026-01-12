"""
Application Constants Module
============================

Centralized constants for the OpenCart test automation framework.
Contains expected values for assertions, URLs, timeouts, and test data.

Categories:
    - Page Titles: Expected page titles for validation
    - URLs: Application URLs for navigation and verification
    - UI Elements: Expected link texts, headers, and section names
    - Product Data: Expected product information for assertions
    - Timeouts: Standard wait durations for explicit waits

Usage:
    from constants.app_constants import LOGIN_PAGE_TITLE, SHORT_WAIT
    
    assert page.get_title() == LOGIN_PAGE_TITLE
    element = util.wait_for_element_to_be_visible(locator, SHORT_WAIT)
"""

# ============== Page Titles ==============

LOGIN_PAGE_TITLE = 'Account Login'
"""Expected title of the login page."""

ACCOUNT_PAGE_TITLE = 'My Account'
"""Expected title of the account dashboard page."""

# ============== Page URLs ==============

LOGIN_PAGE_URL = 'https://naveenautomationlabs.com/opencart/index.php?route=account/login'
"""Full URL of the login page."""

ACCOUNT_PAGE_URL = 'https://naveenautomationlabs.com/opencart/index.php?route=account/account'
"""Full URL of the account dashboard page."""

# ============== Right Column Links ==============

RIGHT_COLUMN_LINKS_BEFORE_LOGIN = [
    'Login', 'Register', 'Forgotten Password', 'My Account', 'Address Book',
    'Wish List', 'Order History', 'Downloads', 'Recurring payments',
    'Reward Points', 'Returns', 'Transactions', 'Newsletter'
]
"""Expected right column links when user is not logged in."""

RIGHT_COLUMN_LINKS_AFTER_LOGIN = [
    "My Account", "Edit Account", "Password", "Address Book", "Wish List",
    "Order History", "Downloads", "Recurring payments", "Reward Points",
    "Returns", "Transactions", "Newsletter", "Logout"
]
"""Expected right column links when user is logged in."""

# ============== Account Page Headers ==============

ACCOUNT_HEADERS = ['My Account', 'My Orders', 'My Affiliate Account', 'Newsletter']
"""Expected section headers on the account dashboard page."""

# ============== Footer Sections ==============

FOOTER_SECTIONS = ["Information", "Customer Service", "Extras", "My Account"]
"""Expected footer section titles."""

FOOTER_LINKS = [
    "About Us", "Delivery Information", "Privacy Policy", "Terms & Conditions",
    "Contact Us", "Returns", "Site Map", "Brands", "Gift Certificates",
    "Affiliate", "Specials", "My Account", "Order History", "Wish List", "Newsletter"
]
"""All expected footer links across all sections."""

INFORMATION_SECTION_LINKS = [
    "About Us", "Delivery Information", "Privacy Policy", "Terms & Conditions"
]
"""Expected links in the 'Information' footer section."""

# ============== Success Messages ==============

USER_REGISTER_SUCCESS_MESG = "Your Account Has Been Created!"
"""Success message displayed after successful user registration."""

# ============== Product Information ==============

PRODUCTS_INFO = {
    "MacBook Pro": {
        "Brand": "Apple",
        "Availability": "Out Of Stock",
        "productHeader": "MacBook Pro",
        "price": "$2,000.00",
        "Ex Tax": "$2,000.00",
        "Product Code": "Product 18",
        "Reward Points": "800"
    },
    "Samsung Galaxy Tab 10.1": {
        "Availability": "Pre-Order",
        "productHeader": "Samsung Galaxy Tab 10.1",
        "price": "$241.99",
        "Ex Tax": "$199.99",
        "Product Code": "SAM1",
        "Reward Points": "1000"
    },
    "MacBook Air": {
        "Brand": "Apple",
        "Availability": "Out Of Stock",
        "productHeader": "MacBook Air",
        "price": "$1,202.00",
        "Ex Tax": "$1,000.00",
        "Product Code": "Product 17",
        "Reward Points": "800"
    }
}
"""
Expected product information for validation.

Structure:
    {
        "Product Name": {
            "Brand": str,
            "Availability": str,
            "productHeader": str,
            "price": str,
            "Ex Tax": str,
            "Product Code": str,
            "Reward Points": str
        }
    }
"""

# ============== Wait Timeouts ==============

SHORT_WAIT = 5
"""Short timeout in seconds (5s) - for quick element waits."""

MEDIUM_WAIT = 10
"""Medium timeout in seconds (10s) - for standard page loads."""

LONG_WAIT = 20
"""Long timeout in seconds (20s) - for slow operations."""
