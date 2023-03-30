#### Запуск тестов локально

1. Установить библиотеки
```bash
pip install -r requirements.txt
```

2. Запустить тесты
```bash
python3 -m pytest -n 2 tests/test_product.py
```


#### Запуск тестов через docker-compose

```bash
docker-compose up --build
```


#### Запуск allure отчета

```bash
allure serve results
```
