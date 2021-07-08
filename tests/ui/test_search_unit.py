import allure
import pytest
from hamcrest import assert_that, equal_to

from common.ui.config.desired_caps import CHROME_ANDROID_GALAXY_S9, CHROME_LINUX
from common.ui.config.env_conf import EnvironmentConfig as EnvConf
from common.ui.page_objects.home_page import HomePage
from common.ui.page_objects.unit_search_page import UnitSearchPage

pytestmark = [pytest.mark.full_regression, pytest.mark.frontend_regression,
              allure.parent_suite('UI Suite'), allure.suite('UnitLists'), allure.sub_suite('Search Unit')]


@pytest.mark.frontend_smoke
@pytest.mark.parametrize('designed_caps', [
    pytest.param(CHROME_LINUX, marks=pytest.mark.desktop),
    # pytest.param(CHROME_ANDROID_GALAXY_S9, marks=pytest.mark.mobile)
])
@pytest.mark.parametrize('unit_name', ['Gotland'])
@allure.title('Verify that search units')
def test_search_unit(web_driver, designed_caps, unit_name):
    # ARRANGE
    # Get driver
    is_mobile_view = designed_caps['isMobile']
    driver = web_driver(is_mobile_view, designed_caps['platformName'], designed_caps['browserName'],
                        designed_caps['deviceName'])
    # Create a new nz photographer

    # ACT #
    driver.get(EnvConf.BASE_URL)
    home_page = HomePage(driver)
    unit_search_page = UnitSearchPage(driver)

    home_page.accept_cookie_warning()

    # click default created list
    default_lists = home_page.get_created_lists()
    default_list_name = default_lists[0].text
    home_page.click_list(default_list_name)

    unit_search_page.enter_unit_search(unit_name)\
        .select_search_unit(unit_name)\
        .clear_unit_search_text()

    actual_added_lists = unit_search_page.get_added_search_lists()

    # ASSERT #
    assert_that(unit_name in actual_added_lists, equal_to(True), 'Verify list is added successfully')
