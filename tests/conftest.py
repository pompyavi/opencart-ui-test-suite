import base64
import copy
import shutil
from datetime import datetime
from pathlib import Path
import pytest
from pytest_html import extras as html_extras
from yaml import safe_load
import logging
import logging.config
from pages.common_components import CommonComponents
from pages.login_page import LoginPage
from utils.config_reader import ConfigReader
from utils.driver_factory.driver_manager import driver_manager

# --- optional Allure (won't break if missing) ---
try:
    import os
    import allure
    from allure_commons.types import AttachmentType
    _ALLURE = True
except Exception:
    allure = None
    AttachmentType = None
    _ALLURE = False
# -----------------------------------------------


_logger = None

def pytest_addoption(parser):
    parser.addoption("--browser", action="store")
    parser.addoption("--browser_version", action="store", default="latest", type=str)
    parser.addoption("--remote", action="store_true",  # means it’s a boolean toggle
        default=False,
        help="Enable remote execution via Selenium Grid or Selenoid"
    )


@pytest.fixture(scope='class')
def setup_teardown(request):
    browser = request.config.getoption("browser")
    version = request.config.getoption("browser_version")
    test_name = request.node.name
    remote = request.config.getoption("remote")
    driver = driver_manager(browser, remote, version, test_name)

    # Attaches the driver to the test class (request.cls.driver), so in tests you can just do
    # self.driver instead of passing it as a method arg.
    request.cls.driver = driver

    # setup common components
    request.cls.common_components = CommonComponents(driver)
    yield
    driver.quit()

#------------- fixtures --------------------

# This fixture depends on setup_teardown (because it’s passed as a parameter).
# That ensures setup_teardown runs before this fixture.
# It takes the driver created by setup_teardown (request.cls.driver) and instantiates LoginPage Object
@pytest.fixture(scope='class')
def setup_login_page(request, setup_teardown):
    # Now, all test methods in the class can directly use self.login_page without creating it themselves.
    request.cls.login_page = LoginPage(request.cls.driver)

@pytest.fixture(scope='class')
def setup_account_page(request, setup_login_page):
    _logger.info("Logging in to setup AccountPage")
    creds = ConfigReader.get_config('credentials')
    request.cls.account_page = request.cls.login_page.do_login(creds.get('email'), creds.get('password'))
    _logger.info("AccountPage setup completed")

@pytest.fixture(scope='class')
def setup_registration_page(request, setup_login_page):
    request.cls.registration_page = request.cls.login_page.click_registration_link()

@pytest.fixture(autouse=True)
def log_test_start_and_end(request):
    _logger.info(f"--- STARTING {request.node.name} ---")
    yield
    _logger.info(f"--- ENDING {request.node.name} ---")

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
    global _logger
    _logger = logging.getLogger(__name__)



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

    # 5) Insert the timestamp before the .html extension
    stamped = base.with_name(f"{base.stem}_{ts}{base.suffix}")

    # 6) Make sure the folder exists
    stamped.parent.mkdir(parents=True, exist_ok=True)

    # 7) Tell pytest-html to write to the timestamped path
    config.option.htmlpath = str(stamped)

    # 9) (Optional) remember where to copy a "latest.html"
    config._latest_html_target = base.with_name("latest.html")


def _b64(data: bytes) -> str:
    """bytes -> base64 ascii string"""
    return base64.b64encode(data).decode("ascii")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when not in ("setup", "call") or rep.outcome != "failed" or getattr(rep, "wasxfail", ""):
        return

    # Resolve driver once (function fixture or class attribute)
    drv = None
    if hasattr(item, "funcargs"):
        drv = item.funcargs.get("driver")
    if drv is None and getattr(item, "instance", None) is not None:
        drv = getattr(item.instance, "driver", None)
    if not drv:
        return

    # One timestamp/worker id for both reporters
    ts = int(datetime.now().timestamp())
    worker = os.getenv("PYTEST_XDIST_WORKER", "sequential")

    # Take one screenshot; reuse for html + Allure
    png = None
    try:
        png = drv.get_screenshot_as_png()
    except Exception:
        pass

    # pytest-html (embed as base64 so it's self-contained)
    if item.config.pluginmanager.hasplugin("html") and png:
        try:
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
            _logger and _logger.info(f"Copied final HTML to: {latest}")
        except Exception as e:
            _logger and _logger.warning(f"Failed to copy HTML to latest: {e}")


def pytest_html_report_title(report):
    report.title = "Test Execution Report"