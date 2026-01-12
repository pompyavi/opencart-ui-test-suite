"""
Driver Manager Module
======================

Factory module for creating and configuring Selenium WebDriver instances.
Supports local and remote (Selenoid/Selenium Grid) execution for Chrome,
Firefox, and Edge browsers.

Features:
    - Automatic browser detection and configuration
    - Remote execution via Selenoid with VNC and video recording
    - Configurable browser versions
    - Window maximization and cookie cleanup

Example:
    >>> driver = driver_manager("chrome", remote=True, version="latest", test_name="test_login")
    >>> driver.get("https://example.com")
    >>> driver.quit()
"""

import logging

from selenium import webdriver
from utils.config_reader import ConfigReader
from utils.driver_factory.browser_options_manager import OptionsManager
from utils.framework_exception import FrameworkException

_logger = logging.getLogger(__name__)


def _init_remote_webdriver(remote_url: str, options, browser: str):
    """
    Initialize a remote WebDriver connection to Selenium Grid or Selenoid.
    
    Args:
        remote_url: URL of the Selenium Grid hub (e.g., "http://localhost:4444/wd/hub").
        options: Browser-specific options object (ChromeOptions, FirefoxOptions, etc.).
        browser: Browser name for logging purposes.
        
    Returns:
        WebDriver: Remote WebDriver instance connected to the grid.
        
    Example:
        >>> driver = _init_remote_webdriver(
        ...     "http://localhost:4444/wd/hub",
        ...     chrome_options,
        ...     "Chrome"
        ... )
    """
    _logger.info(f"Connecting to remote WebDriver at: {remote_url}")
    driver = webdriver.Remote(
        command_executor=remote_url,
        options=options
    )
    _logger.info(f"Remote {browser} session established | Session ID: {driver.session_id}")
    return driver


def driver_manager(browser: str, remote: bool, version: str, test_name: str):
    """
    Create and configure a WebDriver instance based on specified parameters.
    
    This is the main entry point for obtaining a WebDriver. It handles both
    local and remote browser execution, configures browser options, and
    performs initial setup (maximize, clear cookies).
    
    Args:
        browser: Browser type - "chrome", "firefox", or "edge" (case-insensitive).
        remote: If True, connect to Selenoid/Selenium Grid; if False, run locally.
        version: Browser version - "latest", "default", or specific version (e.g., "120.0").
        test_name: Name of the test (used for video naming in remote execution).
        
    Returns:
        WebDriver: Configured WebDriver instance ready for use.
        
    Raises:
        FrameworkException: If browser type is not supported.
        
    Configuration:
        Remote URL is read from config.yaml under 'remote.remote_url'.
        Browser options (headless, incognito) are read from config.yaml.
        
    Example:
        >>> # Local Chrome
        >>> driver = driver_manager("chrome", False, "latest", "test_login")
        >>> 
        >>> # Remote Firefox on Selenoid
        >>> driver = driver_manager("firefox", True, "125.0", "test_checkout")
        >>> 
        >>> # Edge with latest version
        >>> driver = driver_manager("edge", False, "default", "test_search")
    
    Note:
        The driver is automatically maximized and all cookies are cleared
        before returning. Remember to call driver.quit() when done.
    """
    remote_url = None
    if remote:
        remote_url = ConfigReader.get_config('remote').get('remote_url')

    _logger.info(f"Initializing WebDriver | Browser: {browser} | Version: {version} | Remote: {remote} | Test: {test_name}")

    match browser.strip().lower():
        case "chrome":
            options = OptionsManager(remote=remote, version=version, test_name=test_name).get_chrome_options
            if remote:
                driver = _init_remote_webdriver(remote_url, options, "Chrome")
            else:
                _logger.debug("Starting local Chrome browser")
                driver = webdriver.Chrome(options=options)
        case "firefox":
            options = OptionsManager(remote=remote, version=version, test_name=test_name).get_firefox_options
            if remote:
                driver = _init_remote_webdriver(remote_url, options, "Firefox")
            else:
                _logger.debug("Starting local Firefox browser")
                driver = webdriver.Firefox(options=options)
        case "edge":
            options = OptionsManager(remote=remote, version=version, test_name=test_name).get_edge_options
            if remote:
                driver = _init_remote_webdriver(remote_url, options, "Edge")
            else:
                _logger.debug("Starting local Edge browser")
                driver = webdriver.Edge(options=options)
        case _:
            _logger.error(f"Unsupported browser type: {browser}")
            raise FrameworkException(f'Unsupported browser type: {browser}. Supported browsers are: Chrome, Firefox, Edge')

    driver.maximize_window()
    _logger.debug("Browser window maximized")
    driver.delete_all_cookies()
    _logger.debug("All cookies deleted")

    _logger.info(f"WebDriver ready | Browser: {browser} | Session ID: {driver.session_id}")
    return driver
