import allure
import pytest
from hamcrest import assert_that, equal_to

from common.ui.config.desired_caps import CHROME_ANDROID_GALAXY_S9, CHROME_LINUX
from common.ui.config.env_conf import EnvironmentConfig as EnvConf
from common.ui.page_objects.home_page import HomePage

pytestmark = [pytest.mark.full_regression, pytest.mark.frontend_regression,
              allure.parent_suite('UI Suite'), allure.suite('UnitLists'), allure.sub_suite('Default List')]


@pytest.mark.frontend_smoke
@pytest.mark.parametrize('designed_caps', [
    pytest.param(CHROME_LINUX, marks=pytest.mark.desktop),
    # pytest.param(SAFARI_IPHONE_X, marks=pytest.mark.mobile)
])
@allure.title('Verify that 1 existing list added by default')
def test_existing_list_added_default(web_driver, designed_caps):
    # ARRANGE
    is_mobile_view = designed_caps['isMobile']
    driver = web_driver(is_mobile_view, designed_caps['platformName'], designed_caps['browserName'],
                        designed_caps['deviceName'])

    # ACT #
    driver.get(EnvConf.BASE_URL)
    home_page = HomePage(driver)
    home_page.accept_cookie_warning()
    actual_created_lists = home_page.get_created_lists()
    actual_number_of_unit = home_page.get_number_of_unit()
    list_unit_entries = home_page.get_list_unit_entries()

    # ASSERT #
    assert_that(len(actual_created_lists), equal_to(1), 'Verify number of created lists by default')
    assert_that(actual_number_of_unit, equal_to(1), 'Verify number of unit count by default')
    assert_that(len(list_unit_entries), equal_to(1), 'Verify number of unit entry by default')
