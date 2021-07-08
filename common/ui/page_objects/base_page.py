import time
from urllib.parse import urlparse
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import By
from selenium.webdriver.support.wait import WebDriverWait
from common.ui.config.env_conf import EnvironmentConfig as EnvConf


class BasePage:

    def __init__(self, selenium_webdriver):
        self.driver = selenium_webdriver

    def quit(self):
        self.driver.quit()

    def maximize_window(self):
        self.driver.maximize_window()

    def visit(self, location='', timeout=EnvConf.PAGE_LOAD_TIMEOUT_SECONDS):
        self.driver.get(EnvConf.BASE_URL + location)
        self.driver.set_page_load_timeout(timeout)

    def navigate(self, url):
        self.driver.get(url)

    def refresh_page(self):
        self.driver.refresh()

    def click_back_button(self):
        self.driver.execute_script('window.history.back()')

    def delete_all_cookies(self, url):
        """
        Delete all cookies of the given domain
        :param url: Domain that cookies have been deleted
        :return:
        """
        self.navigate(url)
        self.driver.delete_all_cookies()

    def get_cookie(self, cookie_name):
        return self.driver.get_cookie(cookie_name)

    def find_elements(self, tuple_selector):
        element_list = self.driver.find_elements(*tuple_selector)
        return element_list

    # =========================Handle URL=======================
    def get_current_url_path(self):
        current_url = urlparse(self.driver.current_url)
        current_path = current_url.path
        return current_path

    def get_current_url_fragment(self):
        current_url = urlparse(self.driver.current_url)
        current_fragment = current_url.fragment
        return current_fragment

    def get_current_url(self):
        """
        Get the current url complete path by concatenating both path and fragment
        """
        current_url = urlparse(self.driver.current_url)
        whole_path = current_url.path + "#" + current_url.fragment
        return whole_path

    def get_element_of_current_url(self, part=None):
        """
        Get a part of the current url complete
        :param self:
        :param part: hostname, path, query or all by geturl
        :return:
        """
        current_url = urlparse(self.driver.current_url)
        element_of_url = None
        if part is None:  # Get whole URL
            element_of_url = current_url.geturl()
        elif part == 'protocol':
            element_of_url = current_url.scheme  # E.g. http, https ...
        elif part == 'hostname':
            element_of_url = current_url.hostname  # E.g. dev.unifiedsocial.com ...
        elif part == 'port':
            element_of_url = current_url.port  # E.g. 8080, 9000 ...
        elif part == 'path':
            element_of_url = current_url.path  # E.g. /app/onboarding
        elif part == 'query':
            element_of_url = current_url.query  # E.g.
        elif part == 'fragment':
            element_of_url = current_url.fragment  # E.g. /facebook/
        return element_of_url

    # ==========================wait elements===============================================
    def wait_for_page_ready(self, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: self.driver.execute_script("return document.readyState == 'complete'"))

    def wait_for_visibility_of_element(self, by, selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((by, selector)))

    def wait_for_visibility_of_element_by_id(self, selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        return self.wait_for_visibility_of_element(By.ID, selector, timeout)

    def wait_for_visibility_of_element_by_css(self, selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        return self.wait_for_visibility_of_element(By.CSS_SELECTOR, selector, timeout)

    def wait_for_visibility_of_element_by_xpath(self, selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        return self.wait_for_visibility_of_element(By.XPATH, selector, timeout)

    def wait_for_text_to_be_present(self, by, selector, text, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.text_to_be_present_in_element((by, selector), text))

    def wait_for_element_to_click(self, by, selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, selector)))

    def click_and_type(self, selector_tuple, text=None):
        elm = self.wait_for_element_to_be_clickable(selector_tuple)
        actions = ActionChains(self.driver)
        actions.click(elm)
        if text is not None:
            actions.send_keys(text)
        actions.perform()

    def double_click(self, selector_tuple):
        elm = self.wait_for_element_to_be_clickable(selector_tuple)
        actions = ActionChains(self.driver)
        actions.double_click(elm)
        actions.perform()

    def clear_and_type(self, by, selector, value=None):
        element = self.wait_for_visibility_of_element(by, selector)
        element.click()
        element.clear()
        if value is not None:
            element.send_keys(value)

    def send_key_and_press_tab(self, selector_tuple, value):
        element = self.wait_for_visibility_of_element_located(selector_tuple)
        element.send_keys(value)
        element.send_keys(Keys.TAB)

    def check_displayed(self, by, selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        try:
            self.wait_for_visibility_of_element(by, selector, timeout)
        except TimeoutException:
            return False
        return True

    def check_element_exist(self, selector):
        try:
            self.driver.find_element(selector[0], selector[1])
        except NoSuchElementException:
            return False
        return True

    def is_attribute_present(self, selector, attribute_name):
        """
        Check if attribute of a element present
        :param selector:
        :param self:
        :param attribute_name: name of attribute to get
        :return:
        """
        element = self.wait_for_visibility_of_element_located(selector)
        result = False
        attribute_value = element.get_attribute(attribute_name)
        if attribute_value is not None:
            result = True
        return result

    def get_text(self, by, selector):
        """
        Return text of a element
        :param self:
        :param by:
        :param selector:
        :return:
        """
        element = self.wait_for_visibility_of_element(by, selector)
        return element.text

    def move_to_element(self, tuple_selector, by_script=False):
        element = self.wait_element_exist(tuple_selector)
        if by_script:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        else:
            actions = ActionChains(self.driver)
            actions.move_to_element(element)
            actions.perform()

        # ---- wait method ------------

    def wait_element_exist(self, tuple_selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(tuple_selector))

    def wait_for_visibility_of_element_located(self, tuple_selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(tuple_selector))

    def wait_for_invisibility_of_element_located(self, tuple_selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(tuple_selector))

    def wait_for_text_to_be_present_in_element(self, tuple_selector, text, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.text_to_be_present_in_element(tuple_selector, text))

    def wait_for_element_to_be_clickable(self, tuple_selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(tuple_selector))

    def wait_for_text_to_be_present_in_value_of_element(self, tuple_selector, text,
                                                        timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        """
        An expectation for checking if the given text is present in the element's
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.text_to_be_present_in_element_value(tuple_selector, text))

    def is_text_present_in_element(self, tuple_selector, text, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        try:
            self.wait_for_text_to_be_present_in_element(tuple_selector, text, timeout)
            return True
        except TimeoutException:
            return False

    def is_text_present_in_value_of_element(self, tuple_selector, text):
        """
        Return result for checking if the given text is present in the element's
        """
        try:
            self.wait_for_text_to_be_present_in_value_of_element(tuple_selector, text)
            return True
        except TimeoutException:
            return False

    # ---- check method ------------
    def is_element_selected(self, tuple_selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        element = self.wait_for_visibility_of_element_located(tuple_selector, timeout)
        return element.is_selected()

    def is_element_visible(self, tuple_selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        try:
            self.wait_for_visibility_of_element_located(tuple_selector, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_invisible(self, tuple_selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        try:
            self.wait_for_invisibility_of_element_located(tuple_selector, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_exist(self, tuple_selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        try:
            self.wait_element_exist(tuple_selector, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_enabled(self, tuple_selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        element = self.wait_for_visibility_of_element_located(tuple_selector, timeout)
        return element.is_enabled()

    def is_element_disable(self, tuple_selector):
        """
        Check whether or not element is disable
        :param tuple_selector:
        :return:True (disable)/False(enable)
        """
        is_disabled = self.get_attribute_of_element(tuple_selector, 'disabled')
        return False if is_disabled is None else True

    # ---- action method ------------

    def click_and_select_link_text_from_menu_options(self, dropdown_locator, link_text,
                                                     timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS, move_to_element=False,
                                                     move_to_element_by_script=False):
        self.click_element(dropdown_locator, timeout)
        self.click_element((By.LINK_TEXT, link_text), move_to_element=move_to_element,
                           move_to_element_by_script=move_to_element_by_script)

    @classmethod
    def click_element_directly(cls, element):
        element.click()

    def click_element(self, tuple_selector, move_to_element=False, move_to_element_by_script=False,
                      timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS, by_script=False):
        if move_to_element:
            self.move_to_element(tuple_selector)
        if move_to_element_by_script:
            self.move_to_element(tuple_selector, by_script=True)
        element = self.wait_for_element_to_be_clickable(tuple_selector, timeout)
        if by_script:
            self.driver.execute_script("arguments[0].click();", element)
            self.driver.execute_script("return arguments[0].style", element)
        else:
            element.click()

    def type_text(self, tuple_selector, value=None, tab=None, enter=None):
        element = self.wait_for_visibility_of_element_located(tuple_selector)
        if value:
            element.send_keys(value)
        if tab:
            element.send_keys(Keys.TAB)
        if enter:
            element.send_keys(Keys.ENTER)

    def clear_and_type_text(self, tuple_selector, value=None, tab=None, enter=None):
        element = self.wait_for_visibility_of_element_located(tuple_selector)
        self.click_element(tuple_selector, move_to_element=True)
        element.clear()
        self.wait_for_text_to_be_present(tuple_selector[0], tuple_selector[1], '')
        if value and value != 'None':
            element.send_keys(value)
        if tab:
            element.send_keys(Keys.TAB)
        if enter:
            element.send_keys(Keys.ENTER)

    def delete_or_clear_text(self, tuple_selector, num, clear=False):
        element = self.wait_for_visibility_of_element_located(tuple_selector)
        if clear:
            element.clear()
            time.sleep(2)
        else:
            for n in range(0, num):
                element.send_keys(Keys.BACKSPACE)
                time.sleep(0.1)

    def drag_and_drop_between_two_elements(self, tuple_selector_source, tuple_selector_target):
        element_source = self.wait_for_visibility_of_element_located(tuple_selector_source)
        element_target = self.wait_for_visibility_of_element_located(tuple_selector_target)

        actions = ActionChains(self.driver)
        actions.drag_and_drop(element_source, element_target).perform()

    def drag_and_drop_offset_element(self, tuple_selector, xoffset, yoffset):
        element = self.wait_for_visibility_of_element_located(tuple_selector)

        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.drag_and_drop_by_offset(element, xoffset, yoffset).perform()

    # ---- get information method ------------
    def get_element_text(self, tuple_selector, move_to_element=False, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        if move_to_element:
            self.move_to_element(tuple_selector)
        element = self.wait_for_visibility_of_element_located(tuple_selector, timeout)

        return element.text

    def get_moved_elements_text(self, tuple_selector, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        wait = WebDriverWait(self.driver, timeout)
        elements = wait.until(EC.presence_of_all_elements_located(tuple_selector))
        result = []
        for e in elements:
            actions = ActionChains(self.driver)
            actions.move_to_element(e)
            actions.perform()
            result.append(e.text)
        return result

    def get_text_of_elements(self, tuple_selector, move_to_element=False, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        wait = WebDriverWait(self.driver, timeout)
        elements = wait.until(EC.presence_of_all_elements_located(tuple_selector))
        if not move_to_element:
            return self.get_text_list(elements)
        text_list = []
        for e in elements:
            ActionChains(self.driver).move_to_element(e).perform()
            text_list.append(str(e.text))
        return text_list

    @staticmethod
    def get_text_list(list_data):
        """
        Get names of a list
        :param list_data:
        :return:
        """
        name_list = []
        for item in list_data:
            name_list.append(item.text)
        return name_list

    def get_attribute_of_element(self, tuple_selector, attribute, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS,
                                 move_to_element=False):
        """
        Get attribute of element
        :param move_to_element:
        :param self:
        :param tuple_selector: tuple selector (By.locator, locator_value)
        :param attribute:
        :param timeout:
        :return:
        """
        if move_to_element:
            self.move_to_element(tuple_selector)
        element = self.wait_element_exist(tuple_selector, timeout)
        return element.get_attribute(attribute)

    def get_value_of_css_property(self, tuple_selector, attribute_name, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS,
                                  move_to_element=False):
        """
        Get the value of an attribute of selector
        :param move_to_element:
        :param tuple_selector:
        :param timeout:
        :param self:
        :param attribute_name: name of attribute to get
        :return:
        """
        if move_to_element:
            self.move_to_element(tuple_selector)
        element = self.wait_for_visibility_of_element_located(tuple_selector, timeout)
        return element.value_of_css_property(attribute_name)

    def set_attribute_of_element(self, tuple_selector, value_input,
                                 timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS,
                                 move_to_element=False):
        if move_to_element:
            self.move_to_element(tuple_selector)
        element = self.wait_element_exist(tuple_selector, timeout)
        return self.driver.execute_script("arguments[0].setAttribute('value',arguments[1])", element, value_input)

    # --------------------------------------------------------

    def is_link_name_visible(self, link_name):
        return self.is_element_visible((By.LINK_TEXT, link_name))

    def is_link_name_invisible(self, link_name):
        return self.is_element_invisible((By.LINK_TEXT, link_name))

    def click_on_link_name(self, link_name):
        self.move_to_element((By.LINK_TEXT, link_name), True)
        self.click_element((By.LINK_TEXT, link_name))

    def get_pseudo_selector(self, locator, style, prop):
        element = self.wait_element_exist(locator)
        script = "return window.getComputedStyle(arguments[0],'{style}').getPropertyValue('{property}')".format(
            style=style, property=prop)
        return self.driver.execute_script(script, element)

    def click_element_at_point(self, pixel_x, pixel_y):
        """
        Click element at point(x,y)
        :param pixel_x:
        :param pixel_y:
        :return:
        """
        script = 'el = document.elementFromPoint({pixel_x}, {pixel_y}); el.click();'.format(pixel_x=pixel_x,
                                                                                            pixel_y=pixel_y)
        self.driver.execute_script(script)

    def execute_javascript(self, script=''):
        return self.driver.execute_script(script)

    def switch_to_frame(self, tuple_locator, timeout=EnvConf.SELENIUM_TIMEOUT_SECONDS):
        iframe = self.wait_element_exist(tuple_locator, timeout)
        self.driver.switch_to.frame(iframe)

    def switch_to_default_frame(self):
        self.driver.switch_to.default_content()
