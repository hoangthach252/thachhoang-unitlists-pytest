from common.ui.page_objects.base_page import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):

    COOKIES_ACCEPT_BTN = (By.CSS_SELECTOR, 'div[class^="cookieWarningstyles__Dialog"] button')
    NUMBER_OF_UNIT = (By.CSS_SELECTOR, 'p[class^="TertiarySmall"]')
    UNIT_ENTRY = (By.CSS_SELECTOR, 'li[class^="unitlistsstyles__UnitEntry"]')
    CREATED_LISTS = (By.CSS_SELECTOR, 'li[class^="Paper-sc"]  h2[class^="MainText"]')
    LIST_BY_TEXT = (By.XPATH, '//h2[contains(@class, "MainText")][text()="{list_name}"]')

    def accept_cookie_warning(self):
        self.click_element(HomePage.COOKIES_ACCEPT_BTN)
        return self

    def get_created_lists(self):
        return self.find_elements(HomePage.CREATED_LISTS)

    def click_list(self, list_name):
        list_selector = HomePage.LIST_BY_TEXT
        self.click_element((list_selector[0], list_selector[1].format(list_name=list_name)))
        return self

    def get_number_of_unit(self):
        return int(self.get_element_text(HomePage.NUMBER_OF_UNIT).split(": ")[1])

    def get_list_unit_entries(self):
        return self.find_elements(HomePage.UNIT_ENTRY)
