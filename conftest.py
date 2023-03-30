import allure
from os import path, makedirs
from pytest import fixture, hookimpl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import strftime

from page.main_page import MainPage
from page.sing_in_popap import SignInPopap
from settings.manager import manager


def pytest_addoption(parser):
    """Добавляет параметры при запуске теста"""
    for opt in vars(manager.options).values():
        parser.addoption(opt.name, action=opt.action,
                         default=opt.default, help=opt.info)


def pytest_make_parametrize_id(val):
    """Возвращает русские тестовые данные в корректном виде"""
    return repr(val)


def pytest_sessionstart(session):
    """Подготавливает данные"""
    # Добавляем папку с для хранения результатов прогона
    if not path.exists(manager.paths.results):
        makedirs(manager.paths.results)
    # Присваиваем значения всем кастомным ключам
    for opt_name in vars(manager.options).keys():
        arg_value = getattr(session.config.option, opt_name)
        setattr(getattr(manager.options, opt_name), 'value', arg_value)
    # Парсим конфиги на основе кастомных screenshots
    manager.set_configs()


def pytest_runtest_setup(item):
    """Получает имя теста и время его запуска"""
    manager.test_name = item.name or item.originalname
    manager.test_start = strftime("%d-%m-%Y_%H-%M")


@hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """Хук для перехвата статуса тест кейса"""
    outcome = yield
    result = outcome.get_result()
    # rep_{result.when} используется в фикстуре kill_driver()
    setattr(item, f'rep_{result.when}', result)


@fixture()
def driver(request):
    br_name = manager.options.br_name.value
    br_size = manager.options.br_size.value
    selenoid_cfg = manager.selenoid
    capabilities = {
        'browserName': br_name,
        'browserVersion': selenoid_cfg['version'],
        'selenoid:options': {
            'enableVNC': selenoid_cfg['vnc'],
            'enableVideo': selenoid_cfg['video'],
            'name': manager.test_name
        }
    }
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Remote(
        command_executor=selenoid_cfg['url'],
        desired_capabilities=capabilities,
        options=chrome_options)
    res_width, res_height = br_size.split('x')
    driver.set_window_size(res_width, res_height)

    yield driver

    if request.node.rep_setup.failed or request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f'Screenshot before test crash',
            attachment_type=allure.attachment_type.PNG
        )
    driver.quit()


@fixture()
def main_page(driver):
    """Переходит на 'Главную страницу' и возвращает ее инстанс"""
    page = MainPage(driver)
    page.go()
    page.wait_header_area()
    page.wait_for_url_change_to_expected()
    return page


@fixture()
def main_page_user(request, main_page, driver):
    """Переходит на 'Главную страницу' с кредами юзера полученных из маркера 'auth_user'"""
    user_name = request.node.get_closest_marker('auth_user').args[0]
    user_info = manager.users[user_name]
    sign_in_popap = SignInPopap(main_page.driver)
    sign_in_popap.sign_in(user_info['email'], user_info['password'])
    main_page = MainPage(main_page.driver)
    main_page.wait_profile_name_button()
    return main_page
