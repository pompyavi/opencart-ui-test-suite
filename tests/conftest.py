"""
Pytest Configuration Module (conftest.py)
==========================================

Central configuration file for pytest test execution.
Provides fixtures, hooks, and configuration for the test framework.

Features:
    - Browser setup/teardown fixtures
    - Page object initialization fixtures
    - Logging configuration with parallel execution support
    - pytest-html report customization with screenshots
    - Allure integration (optional)
    - Test start/end logging with visual separators

Command Line Options:
    --browser: Browser type (chrome, firefox, edge)
    --browser_version: Browser version (default: latest)
    --remote: Enable Selenoid/Grid execution

Example:
    pytest tests/ --browser chrome --remote -n auto
"""

import base64
import copy
import logging
import logging.config
import os
import shutil
from datetime import datetime
from pathlib import Path

import pytest
from pytest_html import extras as html_extras
from yaml import safe_load

from pages.common_components import CommonComponents
from pages.login_page import LoginPage
from utils.config_reader import ConfigReader
from utils.driver_factory.driver_manager import driver_manager

# --- optional Allure (won't break if missing) ---
try:
    import allure
    from allure_commons.types import AttachmentType
    _ALLURE = True
except ImportError:
    allure = None
    AttachmentType = None
    _ALLURE = False
# -----------------------------------------------

# Module-level logger - initialized in configure_logging fixture
_logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """
    Register custom command-line options for pytest.
    
    Options:
        --browser: Browser type to use (chrome, firefox, edge).
                   If not provided, reads from config.yaml.
        --browser_version: Browser version (default: 'latest').
                          Use specific versions like '120.0' for Selenoid.
        --remote: Enable remote execution via Selenoid/Selenium Grid.
        
    Example:
        pytest tests/ --browser chrome --browser_version 120.0 --remote
    """
    parser.addoption("--browser", action="store",
        help="Browser type: chrome, firefox, or edge"
    )
    parser.addoption("--browser_version", action="store", default="latest", type=str,
        help="Browser version (default: latest)"
    )
    parser.addoption("--remote", action="store_true",
        default=False,
        help="Enable remote execution via Selenium Grid or Selenoid"
    )


@pytest.fixture(scope='class')
def setup_teardown(request):
    """
    Main browser setup and teardown fixture.
    
    Creates a WebDriver instance and attaches it to the test class
    along with CommonComponents for shared functionality.
    
    Scope: class - One browser instance per test class.
    
    Provides:
        - request.cls.driver: WebDriver instance
        - request.cls.common_components: CommonComponents instance
        
    Teardown:
        Automatically quits the browser after all tests in the class.
        
    Example:
        @pytest.mark.usefixtures('setup_teardown')
        class TestExample:
            def test_something(self):
                self.driver.get("https://example.com")
    """
    browser = request.config.getoption("browser") or ConfigReader.get_config('browser')
    version = request.config.getoption("browser_version")
    test_name = request.node.name
    remote = request.config.getoption("remote")
    driver = driver_manager(browser, remote, version, test_name)

    # Attaches the driver to the test class
    request.cls.driver = driver
    request.cls.common_components = CommonComponents(driver)
    
    yield
    
    driver.quit()


# ============== Page Object Fixtures ==============

@pytest.fixture(scope='class')
def setup_login_page(request, setup_teardown):
    """
    Initialize LoginPage and attach to test class.
    
    Depends on: setup_teardown
    
    Provides:
        - request.cls.login_page: LoginPage instance
        
    Note:
        Automatically navigates to the login URL during initialization.
        
    Example:
        @pytest.mark.usefixtures('setup_login_page')
        class TestLogin:
            def test_title(self):
                assert self.login_page.get_page_title() == "Account Login"
    """
    request.cls.login_page = LoginPage(request.cls.driver)


@pytest.fixture(scope='class')
def setup_account_page(request, setup_login_page):
    """
    Login and initialize AccountPage for tests requiring authentication.
    
    Depends on: setup_login_page
    
    Provides:
        - request.cls.account_page: AccountPage instance (logged in)
        
    Credentials:
        Retrieved from config.yaml under 'credentials' section.
        
    Example:
        @pytest.mark.usefixtures('setup_account_page')
        class TestAccount:
            def test_logout_visible(self):
                assert self.account_page.is_logout_link_exists()
    """
    _logger.info("Logging in to setup AccountPage")
    creds = ConfigReader.get_config('credentials')
    request.cls.account_page = request.cls.login_page.do_login(
        creds.get('email'), creds.get('password')
    )
    _logger.info("AccountPage setup completed")


@pytest.fixture(scope='class')
def setup_registration_page(request, setup_login_page):
    """
    Navigate to registration page and initialize UserRegistrationPage.
    
    Depends on: setup_login_page
    
    Provides:
        - request.cls.registration_page: UserRegistrationPage instance
        
    Example:
        @pytest.mark.usefixtures('setup_registration_page')
        class TestRegistration:
            def test_register_user(self):
                result = self.registration_page.register_user(...)
    """
    request.cls.registration_page = request.cls.login_page.click_registration_link()

@pytest.fixture(autouse=True)
def log_test_start_and_end(request):
    """Log clear separators between tests with metadata."""
    test_name = request.node.name
    test_class = request.node.parent.name if request.node.parent else "Unknown"
    test_file = request.node.fspath.basename if hasattr(request.node, 'fspath') else "Unknown"
    
    separator = "=" * 80
    _logger.info("")
    _logger.info(separator)
    _logger.info(f"  TEST START: {test_name}")
    _logger.info(f"  Class: {test_class} | File: {test_file}")
    _logger.info(separator)
    
    yield
    
    # Get test outcome
    outcome = "PASSED" if not hasattr(request.node, '_fail_text') or request.node._fail_text is None else "FAILED"
    
    _logger.info(separator)
    _logger.info(f"  TEST END: {test_name} | Result: {outcome}")
    _logger.info(separator)
    _logger.info("")

@pytest.fixture(scope="session", autouse=True)
def configure_logging(request):

    project_root = Path(request.config.rootpath).resolve()
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    workerinput = getattr(request.config, "workerinput", None)  # present only on xdist workers
    numproc = int(getattr(request.config.option, "numprocesses", 0) or 0)  # >0 when -n is used

    if workerinput:
        # Parallel: this is a WORKER (gw0/gw1/...)
        workerid = workerinput.get("workerid", "gw?")
        filename = f"test_{workerid}_{ts}.log"
    elif numproc > 0:
        # Parallel: this is the CONTROLLER; skip making a controller log file (simple setup)
        return
    else:
        # Sequential run: ONE file
        filename = f"test_{ts}.log"

    log_file_path = log_dir / filename

    log_config_path = project_root / 'configs' / 'logger_config.yaml'

    with open(log_config_path) as f:
        config = safe_load(f)

    # Work on a copy (each process mutates its own)
    cfg = copy.deepcopy(config)

    # Ensure the handler exists and patch its filename
    handlers = cfg.get("handlers", {})
    if "file" not in handlers:
        raise KeyError("Logging YAML must define a 'file' handler")
    handlers["file"]["filename"] = str(log_file_path)

    logging.config.dictConfig(config=cfg)
    _logger.info(f"Logging configured | File: {log_file_path}")



# ------------- pytest-html configuration --------------------

def _is_controller(config):
    # In xdist, workers have 'workerinput'; controller doesn't.
    return getattr(config, "workerinput", None) is None

def pytest_configure(config):
    # 1) Only run if pytest-html is installed
    if not config.pluginmanager.hasplugin("html"):
        return
    # 2) Only the controller (not workers) should set the output path
    if not _is_controller(config):
        return

    # 3) Get the base path from CLI/ini, or use a default
    base = Path(__file__).parent.parent / "reports" / "report.html"

    # 4) Build a timestamp like 2025-08-15_21-17-33
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # 5) Insert the timestamp into the filename before the .html extension
    stamped = base.with_name(f"{base.stem}_{ts}{base.suffix}")

    # 6) Make sure the folder exists
    # parents=True creates intermediate directories;
    # exist_ok=True avoids raising if it already exists.
    stamped.parent.mkdir(parents=True, exist_ok=True)

    # 7) Tell pytest-html to write to the timestamped path
    # config.option holds CLI options — --html maps to htmlpath.
    # This effectively overrides CLI default if no CLI path was given or augments it.
    config.option.htmlpath = str(stamped)

    # 9) (Optional) remember where to copy a "latest.html"
    # This is an ad-hoc attribute (leading underscore to hint private). It’s used in pytest_unconfigure.
    config._latest_html_target = base.with_name("latest.html")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when not in ("setup", "call") or rep.outcome != "failed" or getattr(rep, "wasxfail", ""):
        return

    # Resolve driver once (function fixture or class attribute)
    drv = None
    # If the test uses a driver fixture, it will be in item.funcargs. Grab it.
    if hasattr(item, "funcargs"):
        drv = item.funcargs.get("driver")
    # If the test is a method on a class instance and that instance has a driver attribute, use that.
    if drv is None and getattr(item, "instance", None) is not None:
        drv = getattr(item.instance, "driver", None)
    if not drv:
        return

    # One timestamp/worker id for both reporters
    ts = int(datetime.now().timestamp())
    # get the xdist worker id from environment if present.
    worker = os.getenv("PYTEST_XDIST_WORKER", "sequential")

    # Take one screenshot; reuse for html + Allure
    png = None
    try:
        png = drv.get_screenshot_as_png()
    except Exception:
        pass

    if item.config.pluginmanager.hasplugin("html") and png:
        try:
            # pytest-html (embed as base64 so it's self-contained)
            b64 = base64.b64encode(png).decode("ascii")
            extras_list = getattr(rep, "extras", None) or getattr(rep, "extra", [])
            extras_list.append(
                html_extras.image(b64, mime_type="image/png", extension="png", name=f"{item.name}-{ts}")
            )
            if hasattr(rep, "extras"):
                rep.extras = extras_list
            else:
                rep.extra = extras_list
        except Exception:
            pass  # keep tests going even if report attach fails

    # Allure
    if _ALLURE and png:
        try:
            allure.attach(png, name=f"{item.name}_{worker}_{ts}", attachment_type=AttachmentType.PNG)
        except Exception as e:
            try:
                allure.attach(str(e), name="allure-screenshot-error", attachment_type=AttachmentType.TEXT)
            except Exception:
                pass

    # Stash failure text for your logger
    try:
        item._fail_text = str(rep.longrepr)
    except Exception:
        item._fail_text = None

@pytest.hookimpl(trylast=True)
def pytest_unconfigure(config):
    # only controller should copy
    if getattr(config, "workerinput", None) is not None:
        return

    html = getattr(config.option, "htmlpath", None)
    latest = getattr(config, "_latest_html_target", None)
    if html and latest and Path(html).exists():
        try:
            shutil.copyfile(html, latest)
            _logger.info(f"Copied final HTML to: {latest}")
        except Exception as e:
            _logger.warning(f"Failed to copy HTML to latest: {e}")


def pytest_html_report_title(report):
    report.title = "Test Execution Report"