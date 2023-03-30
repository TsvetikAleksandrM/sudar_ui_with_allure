import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as WDWait
from time import time, sleep

from locators.base_page_locators import *
from settings.manager import manager
from utils.common import wait
from urllib.parse import urljoin


class BasePage:
    """Базовый класс"""

    waiting_timeout = 10
    locator_type = 'xpath'
    name = 'base_page'

    def __init__(self, driver):
        self.driver = driver
        self.url = urljoin(manager.env['base_url'], manager.pages[self.name]['uri'])

    """Методы для драйвера"""

    def go(self):
        with allure.step('Перейти на главную страницу'):
            self.driver.get(self.url)

    def go_url(self, url):
        with allure.step(f'Перейти на страницу: "{url}"'):
            self.driver.get(url)

    def get_current_url(self):
        with allure.step('Получить текущий url'):
            return self.driver.current_url

    def wait_for_url_changes(self, url, err_msg=''):
        with allure.step('Ждать смены url'):
            return WDWait(self.driver, 10).until(ec.url_changes(url), err_msg)

    def wait_for_url_change_to_expected(self, expect_url=None):
        with allure.step('Ждать смены url на ожидаемый'):
            if expect_url is None:
                expect_url = self.url
            wait(lambda: expect_url == self.get_current_url(),
                 err_msg=f'The URL hasn`t changed.'
                         f'\n EXPECT URL - \n "{expect_url}"'
                         f'\n ACTUAL URL - \n "{self.get_current_url()}"')

    def wd_wait(self, condition, locator, timeout=waiting_timeout, err_msg=''):
        """Ожидает какого либо состояния относительно локатора"""
        return WDWait(self.driver, timeout).until(condition((self.locator_type, locator)), err_msg)

    def get_element(self, locator):
        """Возвращает элемент, который присутствует на странице"""
        return self.wd_wait(ec.presence_of_element_located, locator,
                            err_msg=f'Could not find element with locator {locator}')

    def get_elements(self, locator):
        """Возвращает элементы, которые присутствуют на странице"""
        return self.wd_wait(ec.presence_of_all_elements_located, locator,
                            err_msg=f'Could not find elements with locator {locator}')

    def element_is_visible(self, locator, timeout=5):
        """Определяет виден ли элемент на странице"""
        try:
            self.wd_wait(ec.visibility_of_element_located, locator, timeout=timeout,
                         err_msg=f'Element with locator {locator} is not visible on the page')
            return True
        except TimeoutException:
            return False

    def elements_are_visible(self, locator, timeout=2):
        """Определяет видны ли все элементы на странице"""
        try:
            self.wd_wait(ec.visibility_of_all_elements_located, locator, timeout=timeout,
                         err_msg=f'Elements  with locator {locator} is not visible on the page')
            return True
        except TimeoutException:
            return False

    def is_element_visible_on_display(self, locator: str = None, element: WebElement = None, wait=True,
                                      timeout: int = 5, time_step: int = 1) -> bool:
        """
        Определяет виден ли локатор(элемент) на экране полностью
        Если wait = True, то ищем элемент с ожиданием, иначе без ожидания
        """
        global result
        script = (" elem = arguments[0];                                                                  "
                  " box = elem.getBoundingClientRect();                                                   "
                  " x_top_left_corner = box.left;                                                         "
                  " y_top_left_corner = box.top;                                                          "
                  " top_left_corner_element = Boolean(document.elementFromPoint(x_top_left_corner,        "
                  "                                                             y_top_left_corner));      "
                  " x_lower_right_corner = box.right;                                                     "
                  " y_lower_right_corner = box.bottom;                                                    "
                  " lower_right_corner_element = Boolean(document.elementFromPoint(x_lower_right_corner,  "
                  "                                                                y_lower_right_corner));"
                  " return top_left_corner_element && lower_right_corner_element;                         "
                  )
        if not element:
            element = self.get_element(locator)
        if wait:
            start_time = time()
            while time() - start_time < timeout:
                result = self.driver.execute_script(script, element)
                if result:
                    break
                sleep(time_step)
        else:
            result = self.driver.execute_script(script, element)
        return result

    def move_mouse_to_element(self, element, x_offset=0, y_offset=0):
        """Перемещает курсор мышки к элементу"""
        ActionChains(self.driver).move_to_element_with_offset(element, x_offset, y_offset).perform()

    def scroll_to_locator(self, locator, x_offset=0, y_offset=0):
        """
        Выполняет скролл до локатора.
        :param locator: локатор элемента
        :param x_offset: смещение по оси X
        :param y_offset: смещение по оси Y
        """
        element = self.get_element(locator)
        self.driver.execute_script(f'window.scrollTo({element.location["x"] + x_offset}, '
                                   f'{element.location["y"] + y_offset});                ')

    def click_element(self, locator, timeout=3):
        """Выполняет клик на элементе по указанному локатору"""
        element = self.wd_wait(ec.element_to_be_clickable, locator, timeout=timeout,
                               err_msg=f'Didn`t wait for element with locator {locator} to become clickable')
        element.click()

    def enter_text_in_field(self, text, locator, clear=False, click_enter=False):
        """
        Выполняет ввод текста в поле.
        Если clear = True, то выполнить очистку поля перед вводом текста
        Если click_enter = True, то выполнить нажатие кнопки 'Enter'
        """
        field = self.get_element(locator)
        if clear:
            field.click()
            field.clear()
        field.send_keys(text)
        if click_enter:
            field.send_keys(Keys.ENTER)

    """Методы верхнего колонтитула"""

    def header_area_is_visible(self):
        with allure.step('Определить видна ли область верхнего колонтитула'):
            return self.element_is_visible(header_area)

    def wait_header_area(self):
        with allure.step('Подождать отображения области верхнего колонтитула'):
            wait(lambda: self.header_area_is_visible(), err_msg='Header area isn`t visible')

    def profile_name_button_is_visible(self):
        with allure.step('Определить видна кнопка "Имя профиля"'):
            return self.element_is_visible(profile_name_button)

    def wait_profile_name_button(self):
        with allure.step('Подождать отображение кнопки "Имя профиля"'):
            wait(lambda: self.profile_name_button_is_visible(), err_msg='"Profile name" button isn`t visible')

    def click_come_in_button(self):
        with allure.step('Кликнуть по кнопке "Войти"'):
            self.click_element(come_in_button)

    def enter_to_search_field(self, text):
        with allure.step(f'Ввести текст: "{text}" в поле "Поиск"'):
            self.enter_text_in_field(text, search_field, click_enter=True)

    def click_search_field(self):
        with allure.step('Кликнуть по полю "Поиск"'):
            self.click_element(search_field)

    def basket_button_in_button(self):
        with allure.step('Кликнуть по кнопке "Корзина"'):
            self.click_element(basket_button)
