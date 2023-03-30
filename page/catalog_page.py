import allure
from random import choice
from utils.common import wait

from locators.catalog_locators import *
from page.base_page import BasePage


class CatalogPage(BasePage):
    """Класс для работы со страницей 'Каталог'"""

    name = 'catalog_page'

    def you_searched_text_is_visible(self):
        with allure.step('Определить виден ли текст "Вы искали <<...>>"'):
            return self.element_is_visible(you_searched_text)

    def wait_you_searched_text(self):
        with allure.step('Подождать отображение текста "Вы искали <<...>>"'):
            wait(lambda: self.you_searched_text_is_visible(), err_msg='"You searched" text isn`t visible')

    def open_random_card(self):
        with allure.step('Открыть рандомную карточку с продуктом'):
            cards = self.get_elements(product_cards)
            random_cards = choice(cards)
            self.move_mouse_to_element(random_cards)
            random_cards.click()
