from selenium import webdriver
from utils.config_reader import ConfigReader
from utils.driver_factory.browser_options_manager import OptionsManager
from utils.framework_exception import FrameworkException


def driver_manager(browser):
    """
    A simple driver manager that returns a driver instance based on the browser type.
    :param browser: The type of browser to use (e.g., "chrome", "firefox", "edge").
    :return: An instance of the WebDriver for the specified browser.
    :raises FrameworkException: If the browser type is not supported.
    """


    # If browser value is not provided, read from the config file
    if not browser:
        browser = ConfigReader.get_config('browser')

    print(f'Initializing WebDriver for browser: {browser}')

    match browser.strip().lower():
        case "chrome":
            options = OptionsManager().get_chrome_options
            driver = webdriver.Chrome(options=options)
        case "firefox":
            options = OptionsManager().get_firefox_options
            driver = webdriver.Firefox(options=options)
        case "edge":
            options = OptionsManager().get_edge_options
            driver = webdriver.Edge(options=options)
        case _:
            raise FrameworkException(f'Unsupported browser type: {browser}. Supported browsers are: Chrome, Firefox, Edge')

    driver.maximize_window()
    driver.delete_all_cookies()

    return driver
