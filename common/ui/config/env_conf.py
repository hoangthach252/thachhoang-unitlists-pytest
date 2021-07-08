import os

from common.utils.data_helper import DataHelper


class EnvironmentConfig:
    ENVIRONMENT = os.getenv('ENV', 'TEST')
    BASE_URL = os.getenv('BASE_URL', 'https://vardenisiffror.se/unitlists')
    SAUCE_LABS = DataHelper.str_to_bool(os.getenv('SAUCE_LABS', 'False'))
    BUILD_TAG = os.getenv('BUILD_TAG', 'Default Sauce Labs Build')
    SAUCE_LABS_RDC_USER = ''
    SAUCE_LABS_RDC_KEY = ''

    # Browser configuration
    HEADLESS = DataHelper.str_to_bool(os.getenv('HEADLESS', 'False'))
    BROWSER_NAME = os.getenv('BROWSER', 'Chrome')
    PLATFORM = os.getenv('PLATFORM', 'WINDOWS')
    MOBILE_EMULATION = DataHelper.str_to_bool(os.getenv('MOBILE_EMULATION', 'True'))
    GRID = DataHelper.str_to_bool(os.getenv('GRID', 'False'))
    GRID_HOST = os.getenv('GRID_HOST', 'localhost')
    GRID_PORT = os.getenv('GRID_PORT', '4444')

    # Timeout for Selenium waits
    PAGE_LOAD_TIMEOUT_SECONDS = float(os.getenv('PAGE_LOAD_TIMEOUT_SECONDS', 90))
    SELENIUM_TIMEOUT_SECONDS = float(os.getenv('SELENIUM_TIMEOUT_SECONDS', 30))
    WAIT_TIMEOUT_SECONDS = float(os.getenv('SELENIUM_TIMEOUT_SECONDS', 30))
