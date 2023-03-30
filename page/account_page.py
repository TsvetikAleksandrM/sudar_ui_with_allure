import allure

from locators.account_locators import *
from page.base_page import BasePage


class AccountPage(BasePage):
    """Класс для работы со страницей 'Аккаунт'"""

    name = 'account_page'

    def data_updated_message_is_visible(self):
        with allure.step('Определить видно ли всплывающее сообщение "Данные обновлены"'):
            return self.element_is_visible(data_updated_message)

    def enter_to_phone(self, phone):
        with allure.step(f'Ввести текст: "{phone}" в поле "Телефон"'):
            self.enter_text_in_field(phone, phone_field)

    def scroll_to_save_button(self):
        with allure.step(f'Проскроллить до кнопки "Сохранить"'):
            self.scroll_to_locator(save_button, y_offset=-200)

    def click_save_button(self):
        with allure.step(f'Кликнуть по кнопке "Сохранить"'):
            self.click_element(save_button)
