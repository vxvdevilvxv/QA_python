Скачайте с сайта https://sites.google.com/a/chromium.org/chromedriver/downloads драйвер для вашей версии браузера. Разархивируйте скачанный файл.
Создайте на диске C: папку chromedriver и положите разархивированный ранее файл chromedriver.exe в папку C:\chromedriver.
Добавьте в системную переменную PATH папку C:\chromedriver
Для установки всех модулей используйте команду pip install requirements.txt
Для запуска теста в браузере Chrome используйте команду pytest test_amazon.py
Для запуска в браузере Firefox используйте команду pytest --browser_name=firefox test_amazon.py