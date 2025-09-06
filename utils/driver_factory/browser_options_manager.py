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

    def __init__(self, remote, version, test_name):
        self.remote = remote
        self.version = version
        self.test_name = test_name

    @cached_property
    def get_chrome_options(self):
        return chrome_options(self.remote, self.version, self.test_name)

    @cached_property
    def get_firefox_options(self):
        return firefox_options(self.remote, self.version, self.test_name)

    @cached_property
    def get_edge_options(self):
        return edge_options(self.remote)

def chrome_options(remote, version, test_name):
    options = ChromeOptions()
    if ConfigReader.get_config('headless'):
        options.add_argument("--headless")
        print('Running in headless mode')
    if ConfigReader.get_config('incognito'):
        options.add_argument("--incognito")
        print('Running in incognito mode')

    if remote:
        options.set_capability('browserName', 'chrome')

        if version.lower() not in {"default", "latest", "auto", ""}:
            options.browser_version = version

        selenoid_options = {
            "enableVNC": True,
            "enableVideo": True,
            #"enableLog": False,
            "videoName": f"{test_name}_video.mp4",
            "videoScreenSize": "1920x1080",
            "videoFrameRate": 24,
            "screenResolution": "1920x1080x24",
            "name": f"{test_name}"
        }

        options.set_capability('selenoid:options', selenoid_options)

    return options

def firefox_options(remote, version, test_name):
    options = FirefoxOptions()
    if ConfigReader.get_config('headless'):
        options.add_argument("--headless")
        print('Running in headless mode')
    if ConfigReader.get_config('incognito'):
        options.add_argument("-private-window")
        print('Running in incognito mode')

    if remote:
        options.set_capability('browserName', 'firefox')
        if version.lower() not in {"default", "latest", "auto", ""}:
            options.browser_version = version

        selenoid_options = {
            "enableVNC": True,
            "enableVideo": True,
            # "enableLog": False,
            "videoName": f"{test_name}_video.mp4",
            "videoScreenSize": "1920x1080",
            "videoFrameRate": 24,
            "screenResolution": "1920x1080x24",
            "name": f"{test_name}"
        }

        options.set_capability('selenoid:options', selenoid_options)
    return options

def edge_options(remote):
    options = EdgeOptions()
    if ConfigReader.get_config('headless'):
        options.add_argument("--headless")
        print('Running in headless mode')
    if ConfigReader.get_config('incognito'):
        options.add_argument("-inprivate")
        print('Running in incognito mode')

    if remote:
        options.set_capability('browserName', 'edge')
    return options
