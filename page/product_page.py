import allure

from locators.product_locators import *
from page.base_page import BasePage


class ProductPage(BasePage):
    """Класс для работы со страницей 'Продукт'"""

    name = 'product_page'

    def click_add_in_basket_button(self):
        with allure.step('Кликнуть по кнопке "Добавить в корзину"'):
            self.click_element(add_in_basket_button)

    def added_in_basket_button_is_visible(self):
        with allure.step('Определить видна ли кнопка "Добавлено"'):
            return self.element_is_visible(added_in_basket_button)
