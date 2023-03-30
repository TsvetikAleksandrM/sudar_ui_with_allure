import allure
from utils.common import wait

from locators.basket_locators import *
from page.base_page import BasePage


class BasketPage(BasePage):
    """Класс для работы со страницей 'Корзина'"""

    name = 'basket_page'

    def ordering_text_is_visible(self):
        with allure.step('Определить виден ли текст "Оформление заказа"'):
            return self.element_is_visible(ordering_text)

    def wait_ordering_text(self):
        with allure.step('Подождать отображения текста "Оформление заказа"'):
            wait(lambda: self.ordering_text_is_visible(), err_msg='Text "Ordering" isn`t visible')

    def click_delete_product_card_button(self, product):
        with allure.step(f'Кликнуть по кнопке "Удалить" в карточке продукта: "{product}"'):
            self.click_element(delete_product_card_button.format(product=product))

    def your_basket_is_empty_text_is_visible(self):
        with allure.step('Определить виден ли текст "Ваша корзина пуста"'):
            return self.element_is_visible(your_basket_is_empty_text)
