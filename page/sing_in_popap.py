import allure

from locators.sing_in_locators import *
from page.base_page import BasePage
from utils.common import wait


class SignInPopap(BasePage):
    """Класс для работы с попапом 'Войти'"""

    name = 'sign_in_popap'

    def email_field_is_visible(self):
        with allure.step('Определить видно ли поле "Электронная почта"'):
            return self.element_is_visible(email_field)

    def wait_email_field(self):
        with allure.step('Подождать отображение поля "Электронная почта"'):
            wait(lambda: self.email_field_is_visible(), err_msg='"Email" field isn`t visible')

    def enter_to_email(self, email):
        with allure.step(f'Ввести текст: "{email}" в поле "Электронная почта"'):
            self.enter_text_in_field(email, email_field)

    def enter_to_password(self, password):
        with allure.step(f'Ввести текст: "{password}" в поле "Введите пароль"'):
            self.enter_text_in_field(password, password_field)

    def click_come_button_in_auth_popup(self):
        with allure.step('Кликнуть по кнопке "Войти"'):
            self.click_element(come_button_in_auth_popup)

    def sign_in(self, email, password):
        with allure.step(f'Авторизовать пользователя c кредами:\n'
                         f'email: "{email}", password: "{password}"'):
            self.click_come_in_button()
            self.wait_email_field()
            self.enter_to_email(email)
            self.enter_to_password(password)
            self.click_come_button_in_auth_popup()
