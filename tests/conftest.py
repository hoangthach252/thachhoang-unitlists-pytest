import allure
from allure import attachment_type
import pytest
from appium import webdriver as appium_webdriver
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from common.ui.config.desired_caps import SAUCE_LABS_RDC_CHROME_EMULATION_MAPPING
from common.ui.config.env_conf import EnvironmentConfig as EnvConf
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def create_local_driver(is_mobile, browser_name, device_name):
    if browser_name.lower() == 'chrome' or EnvConf.MOBILE_EMULATION:
        chrome_options = ChromeOptions()
        if is_mobile and EnvConf.MOBILE_EMULATION:
            # Device name should be "Pixel 2", "Nexus 5", "iPhoneX", "iPad Mini" ...
            device_name_emulation = SAUCE_LABS_RDC_CHROME_EMULATION_MAPPING[device_name]
            chrome_options.add_experimental_option("mobileEmulation", {"deviceName": device_name_emulation})
        if EnvConf.HEADLESS:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("user-agent=Zenfolio Automation Testing Head-less Chrome Instance")
            if not is_mobile:
                chrome_options.add_argument("--window-size=1920x1080")
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    elif browser_name.lower() == 'firefox':
        firefox_options = FirefoxOptions()
        if EnvConf.HEADLESS:
            firefox_options.headless = True
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)
    elif browser_name.lower() == 'edge':
        browser = webdriver.Edge()
    else:
        raise KeyError("The inputted browser is not supported")
    return browser


@pytest.fixture(scope='function')
def web_driver(request):
    driver_lst = []
    rdc_user = EnvConf.SAUCE_LABS_RDC_USER
    rdc_key = EnvConf.SAUCE_LABS_RDC_KEY

    def _web_driver(is_mobile=False, platform=EnvConf.PLATFORM, browser_name=EnvConf.BROWSER_NAME, device_name=None):
        test_name = request.node.name

        if EnvConf.GRID:
            if is_mobile and EnvConf.SAUCE_LABS:
                caps = {'browserName': browser_name, 'platformName': platform, 'deviceName': device_name,
                        'deviceOrientation': 'portrait', 'phoneOnly': False, 'tabletOnly': False,
                        'privateDevicesOnly': False, 'name': test_name, 'build': EnvConf.BUILD_TAG
                        }
                grid_url = \
                    "https://{}:{}@ondemand.us-west-1.saucelabs.com:443/wd/hub".format(rdc_user, rdc_key)
                browser = appium_webdriver.Remote(grid_url, desired_capabilities=caps)
            elif not is_mobile:
                browser = create_local_driver(is_mobile, browser_name, device_name)
            else:
                grid_url = 'http://{host}:{port}/wd/hub'.format(host=EnvConf.GRID_HOST, port=EnvConf.GRID_PORT)
                caps = {
                    'platform': platform,
                    'browserName': browser_name
                }
                browser = webdriver.Remote(grid_url, desired_capabilities=caps)

            # This is specifically for SauceLabs plugin. In case test fails after selenium session creation
            # having this here will help track it down. creates one file per test non ideal but xdist is awful
            if browser:
                print("SauceOnDemandSessionID={} job-name={}\n".format(browser.session_id, test_name))
            else:
                raise WebDriverException("Never created!")
            driver_lst.append(browser)
        else:
            browser = create_local_driver(is_mobile, browser_name, device_name)
            driver_lst.append(browser)

        browser.set_page_load_timeout(EnvConf.PAGE_LOAD_TIMEOUT_SECONDS)
        if not is_mobile:
            browser.maximize_window()

        return browser

    yield _web_driver
    # Teardown starts here
    if driver_lst:
        if getattr(driver_lst[0], "battery_info", None):
            # Only run these code if the test is run on Sauce Labs.
            # report results
            # use the test result to send the pass/fail status to Sauce Labs
            sauce_result = "failed" if request.node.rep_call.failed else "passed"
            driver_lst[0].execute_script("sauce:job-result={}".format(sauce_result))
        if request.node.rep_call.failed:
            allure.attach(driver_lst[0].get_screenshot_as_png(), 'fail_screenshot', attachment_type=attachment_type.PNG)
        driver_lst[0].quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for Sauce Labs reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
