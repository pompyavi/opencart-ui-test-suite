from functools import cached_property
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from utils.config_reader import ConfigReader


class OptionsManager:
    """
    A function to manage and return Browser options for the Selenium WebDriver.
    This function sets various options for the browser to enhance performance and user experience.
    :return: An instance of Options with the specified configurations.
    """
    @cached_property
    def get_chrome_options(self):
        return chrome_options()

    @cached_property
    def get_firefox_options(self):
        return firefox_options()

    @cached_property
    def get_edge_options(self):
        return edge_options()

def chrome_options():
    options = ChromeOptions()
    if ConfigReader.get_config('headless'):
        options.add_argument("--headless")
        print('Running in headless mode')
    if ConfigReader.get_config('incognito'):
        options.add_argument("--incognito")
        print('Running in incognito mode')
    return options

def firefox_options():
    options = FirefoxOptions()
    if ConfigReader.get_config('headless'):
        options.add_argument("--headless")
        print('Running in headless mode')
    if ConfigReader.get_config('incognito'):
        options.add_argument("-private-window")
        print('Running in incognito mode')
    return options

def edge_options():
    options = EdgeOptions()
    if ConfigReader.get_config('headless'):
        options.add_argument("--headless")
        print('Running in headless mode')
    if ConfigReader.get_config('incognito'):
        options.add_argument("-inprivate")
        print('Running in incognito mode')
    return options
