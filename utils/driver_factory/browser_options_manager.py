"""
Browser Options Manager Module
==============================

Provides configuration and options management for different browser types.
Handles headless mode, incognito/private browsing, and Selenoid-specific
capabilities for remote execution.

Supported Browsers:
    - Chrome (with Selenoid VNC/video support)
    - Firefox (with Selenoid VNC/video support)
    - Edge (with Selenoid VNC/video support)

Features:
    - Lazy loading of options via cached_property
    - Automatic headless/incognito configuration from config.yaml
    - Selenoid capabilities for VNC viewing and video recording
    - Configurable browser versions

Example:
    >>> manager = OptionsManager(remote=True, version="120.0", test_name="test_login")
    >>> chrome_opts = manager.get_chrome_options
    >>> driver = webdriver.Chrome(options=chrome_opts)
"""

import logging
from functools import cached_property

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from utils.config_reader import ConfigReader

_logger = logging.getLogger(__name__)


class OptionsManager:
    """
    Manager class for browser options with lazy loading support.
    
    Uses @cached_property to ensure options are only created once per instance,
    even if accessed multiple times.
    
    Attributes:
        remote (bool): Whether to configure for remote execution.
        version (str): Browser version to use.
        test_name (str): Test name for Selenoid video/session naming.
        
    Example:
        >>> opts = OptionsManager(remote=True, version="latest", test_name="test_checkout")
        >>> driver = webdriver.Chrome(options=opts.get_chrome_options)
    """

    def __init__(self, remote: bool, version: str, test_name: str):
        """
        Initialize the OptionsManager.
        
        Args:
            remote: True for Selenoid/Grid execution, False for local.
            version: Browser version ("latest", "default", or specific like "120.0").
            test_name: Name of the test for session identification.
        """
        self.remote = remote
        self.version = version
        self.test_name = test_name
        _logger.debug(f"OptionsManager initialized | Remote: {remote} | Version: {version} | Test: {test_name}")

    @cached_property
    def get_chrome_options(self) -> ChromeOptions:
        """
        Get configured Chrome options (cached after first access).
        
        Returns:
            ChromeOptions: Configured Chrome browser options.
        """
        return chrome_options(self.remote, self.version, self.test_name)

    @cached_property
    def get_firefox_options(self) -> FirefoxOptions:
        """
        Get configured Firefox options (cached after first access).
        
        Returns:
            FirefoxOptions: Configured Firefox browser options.
        """
        return firefox_options(self.remote, self.version, self.test_name)

    @cached_property
    def get_edge_options(self) -> EdgeOptions:
        """
        Get configured Edge options (cached after first access).
        
        Returns:
            EdgeOptions: Configured Edge browser options.
        """
        return edge_options(self.remote, self.version, self.test_name)


def chrome_options(remote: bool, version: str, test_name: str) -> ChromeOptions:
    """
    Configure and return Chrome browser options.
    
    Args:
        remote: True to add Selenoid capabilities.
        version: Browser version (ignored if "latest", "default", "auto", or empty).
        test_name: Test name for Selenoid session/video naming.
        
    Returns:
        ChromeOptions: Configured options object.
        
    Configuration (from config.yaml):
        - headless: Run browser without GUI
        - incognito: Run in incognito/private mode
        
    Selenoid Capabilities (when remote=True):
        - enableVNC: Allow VNC viewing of session
        - enableVideo: Record video of session
        - videoName: Name of the recorded video file
        - screenResolution: Browser window resolution
        - sessionTimeout: Maximum session duration
        
    Example:
        >>> opts = chrome_options(remote=True, version="120.0", test_name="test_login")
        >>> driver = webdriver.Remote(command_executor=url, options=opts)
    """
    _logger.info(f"Configuring Chrome options | Remote: {remote} | Version: {version}")
    options = ChromeOptions()

    if ConfigReader.get_config('headless'):
        options.add_argument("--headless")
        _logger.info("Chrome: Headless mode enabled")

    if ConfigReader.get_config('incognito'):
        options.add_argument("--incognito")
        _logger.info("Chrome: Incognito mode enabled")

    if remote:
        options.set_capability('browserName', 'chrome')
        _logger.debug("Chrome: Set browserName capability")

        if version.lower() not in {"default", "latest", "auto", ""}:
            options.browser_version = version
            _logger.info(f"Chrome: Explicit version set to {version}")
        else:
            _logger.info(f"Chrome: Using default/latest version (requested: {version})")

        selenoid_options = {
            "enableVNC": True,
            "enableVideo": True,
            "videoName": f"{test_name}_video.mp4",
            "videoScreenSize": "1920x1080",
            "videoFrameRate": 24,
            "screenResolution": "1920x1080x24",
            "name": f"{test_name}",
            "sessionTimeout": "60m"
        }
        options.set_capability('selenoid:options', selenoid_options)
        _logger.debug(f"Chrome: Selenoid options configured | VNC: True | Video: {test_name}_video.mp4")

    _logger.info("Chrome options configuration complete")
    return options


def firefox_options(remote: bool, version: str, test_name: str) -> FirefoxOptions:
    """
    Configure and return Firefox browser options.
    
    Args:
        remote: True to add Selenoid capabilities.
        version: Browser version (ignored if "latest", "default", "auto", or empty).
        test_name: Test name for Selenoid session/video naming.
        
    Returns:
        FirefoxOptions: Configured options object.
        
    Configuration (from config.yaml):
        - headless: Run browser without GUI
        - incognito: Run in private browsing mode (uses -private-window flag)
        
    Example:
        >>> opts = firefox_options(remote=False, version="latest", test_name="test_search")
        >>> driver = webdriver.Firefox(options=opts)
    """
    _logger.info(f"Configuring Firefox options | Remote: {remote} | Version: {version}")
    options = FirefoxOptions()

    if ConfigReader.get_config('headless'):
        options.add_argument("--headless")
        _logger.info("Firefox: Headless mode enabled")

    if ConfigReader.get_config('incognito'):
        options.add_argument("-private-window")
        _logger.info("Firefox: Private browsing mode enabled")

    if remote:
        options.set_capability('browserName', 'firefox')
        _logger.debug("Firefox: Set browserName capability")

        if version.lower() not in {"default", "latest", "auto", ""}:
            options.browser_version = version
            _logger.info(f"Firefox: Explicit version set to {version}")
        else:
            _logger.info(f"Firefox: Using default/latest version (requested: {version})")

        selenoid_options = {
            "enableVNC": True,
            "enableVideo": True,
            "videoName": f"{test_name}_video.mp4",
            "videoScreenSize": "1920x1080",
            "videoFrameRate": 24,
            "screenResolution": "1920x1080x24",
            "name": f"{test_name}",
            "sessionTimeout": "60m"
        }
        options.set_capability('selenoid:options', selenoid_options)
        _logger.debug(f"Firefox: Selenoid options configured | VNC: True | Video: {test_name}_video.mp4")

    _logger.info("Firefox options configuration complete")
    return options


def edge_options(remote: bool, version: str, test_name: str) -> EdgeOptions:
    """
    Configure and return Edge browser options.
    
    Args:
        remote: True to add Selenoid capabilities.
        version: Browser version (ignored if "latest", "default", "auto", or empty).
        test_name: Test name for Selenoid session/video naming.
        
    Returns:
        EdgeOptions: Configured options object.
        
    Configuration (from config.yaml):
        - headless: Run browser without GUI
        - incognito: Run in InPrivate mode (uses -inprivate flag)
        
    Example:
        >>> opts = edge_options(remote=True, version="120.0", test_name="test_payment")
        >>> driver = webdriver.Remote(command_executor=url, options=opts)
    """
    _logger.info(f"Configuring Edge options | Remote: {remote} | Version: {version}")
    options = EdgeOptions()

    if ConfigReader.get_config('headless'):
        options.add_argument("--headless")
        _logger.info("Edge: Headless mode enabled")

    if ConfigReader.get_config('incognito'):
        options.add_argument("-inprivate")
        _logger.info("Edge: InPrivate mode enabled")

    if remote:
        options.set_capability('browserName', 'edge')
        _logger.debug("Edge: Set browserName capability")

        if version.lower() not in {"default", "latest", "auto", ""}:
            options.browser_version = version
            _logger.info(f"Edge: Explicit version set to {version}")
        else:
            _logger.info(f"Edge: Using default/latest version (requested: {version})")

        selenoid_options = {
            "enableVNC": True,
            "enableVideo": True,
            "videoName": f"{test_name}_video.mp4",
            "videoScreenSize": "1920x1080",
            "videoFrameRate": 24,
            "screenResolution": "1920x1080x24",
            "name": f"{test_name}",
            "sessionTimeout": "60m"
        }
        options.set_capability('selenoid:options', selenoid_options)
        _logger.debug(f"Edge: Selenoid options configured | VNC: True | Video: {test_name}_video.mp4")

    _logger.info("Edge options configuration complete")
    return options
