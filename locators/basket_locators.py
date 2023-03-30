"""Локаторы страницы 'Корзина'"""

# Текст 'Оформление заказа'
ordering_text = '//div[contains(@class,"ordering__logo-section")]'

# Карточка продукта
product_card = '//a[contains(text(),"{product}")]//ancestor::div[contains(@class,"desc")]'

# Кнопка 'Удалить' в карточке продукта
delete_product_card_button = '//a[contains(text(),"{product}")]//ancestor::div[contains(@class,"desc")]//button[contains(@class,"delete")]'

# Текст 'Ваша корзина пуста'
your_basket_is_empty_text = '//h1[text()="Ваша корзина пуста"]'
