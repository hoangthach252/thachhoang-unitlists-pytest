from common.ui.page_objects.base_page import BasePage
from selenium.webdriver.common.by import By


class UnitSearchPage(BasePage):

    UNIT_SEARCH_INPUT = (By.ID, 'select-organizations-input')
    UNIT_SELECT_CHECKBOX = (By.XPATH, '//label[contains(@for, "select-organizations-checkbox")]'
                                      '[text()="{unit_name}"]//preceding-sibling::input')
    ADDED_SEARCH_LIST_ITEMS = (By.CSS_SELECTOR, 'table td p[class^="MainText"]')

    def enter_unit_search(self, search_text):
        self.type_text(UnitSearchPage.UNIT_SEARCH_INPUT, search_text)
        return self

    def clear_unit_search_text(self):
        self.click_element(UnitSearchPage.UNIT_SEARCH_INPUT)
        current_search_txt = self.get_attribute_of_element(UnitSearchPage.UNIT_SEARCH_INPUT, 'value')
        self.delete_or_clear_text(UnitSearchPage.UNIT_SEARCH_INPUT, len(current_search_txt), clear=False)
        return self

    def select_search_unit(self, unit_name):
        select_unit_selector = UnitSearchPage.UNIT_SELECT_CHECKBOX
        self.click_element((select_unit_selector[0], select_unit_selector[1].format(unit_name=unit_name)))
        return self

    def get_added_search_lists(self):
        added_lists = []
        list_items = self.find_elements(UnitSearchPage.ADDED_SEARCH_LIST_ITEMS)
        for list_item in list_items:
            added_lists.append(list_item.text.split(". ")[1])
        return added_lists
