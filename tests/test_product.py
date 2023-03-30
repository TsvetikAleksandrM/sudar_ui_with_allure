import allure
from pytest import mark

from constans.base_constans import Username
from page.account_page import AccountPage
from page.basket_page import BasketPage
from page.product_page import ProductPage
from page.catalog_page import CatalogPage
from utils.common import rnd_phone
user = Username.user


@mark.auth_user(user)
@mark.parametrize('product', ['Шапка'])
@allure.title('Добавление и удаление продукта в корзине')
def test_add_and_delete_product_in_basket(main_page_user, product):
    main_page = main_page_user
    # Найти продукт по совпадению и добавить его в корзину
    main_page.enter_to_search_field(product)
    catalog_page = CatalogPage(main_page.driver)
    catalog_page.wait_you_searched_text()
    catalog_page.open_random_card()
    product_page = ProductPage(main_page_user.driver)
    product_page.click_add_in_basket_button()
    assert product_page.added_in_basket_button_is_visible()
    product_page.basket_button_in_button()
    basket_page = BasketPage(main_page.driver)
    # Удалить добавленный продукт из корзины и проверить удаление
    basket_page.wait_ordering_text()
    basket_page.click_delete_product_card_button(product)
    assert basket_page.your_basket_is_empty_text_is_visible()


@mark.auth_user(user)
@allure.title('Изменить номер телефона в аккаунте')
def test_change_phone_in_account(main_page_user):
    main_page = main_page_user
    phone = rnd_phone()
    account_page = AccountPage(main_page.driver)
    # Перейти на страницу 'Аккаунт'
    account_page.go_url(account_page.url)
    account_page.wait_for_url_change_to_expected(account_page.url)
    # Ввести рандомный номер телефона и проверить, что он сохранился
    account_page.enter_to_phone(phone)
    account_page.scroll_to_save_button()
    account_page.click_save_button()
    assert account_page.data_updated_message_is_visible()
