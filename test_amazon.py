import unittest
import random
from selenium.webdriver.common.keys import Keys

global link, search_form_id
link = 'https://www.amazon.com/'
search_form_id = '#twotabsearchtextbox'

# проверка на регистрозависимость поиска
def test_case_sensitive(browser):
    search_queries = ['iphone', 'IPHONE', 'IpHoNe']
    browser.get(link)
    button_id = '#nav-search-submit-button'
    list_of_results = set()
    for query in search_queries:
        search_form = browser.find_element_by_css_selector(search_form_id)
        search_form.clear()
        search_form.send_keys(query)
        browser.find_element_by_css_selector(button_id).click()
        search_result = browser.find_element_by_xpath(
            '/html/body/div[1]/div[2]/span/div/span/h1/div/div[1]/div/div/span[1]').text
        list_of_results.add(search_result.split()[2])

    assert len(list_of_results) == 1, 'Результаты тестов не совпадают, поиск регистрозависимый'


# тест отправки запроса по нажатию на ENTER
def test_search_on_enter_key(browser):
    browser.get(link)
    search_form = browser.find_element_by_css_selector(search_form_id)
    search_form.send_keys('iphone')
    search_form.send_keys(Keys.ENTER)
    try:  # ищем результаты выполнения поиска
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/span/div/span/h1/div/div[1]/div/div/span[1]')
    except Exception:
        assert False, 'Отправка запроса по клавише ENTER не работает'


# тест на вхождение данных результата уточненного запроса в множество результатов первоначального запроса
def test_for_entry(browser):
    text_selector = 'span.a-size-medium.a-color-base.a-text-normal'
    url_selector = 'h2 a.a-link-normal.a-text-normal'
    browser.get(link)
    search_form = browser.find_element_by_css_selector(search_form_id)
    search_form.send_keys('iphone')
    search_form.send_keys(Keys.ENTER)
    text = browser.find_elements_by_css_selector(text_selector)
    urls = browser.find_elements_by_css_selector(url_selector)
    result_dict = {key.get_attribute('innerHTML'): value.get_attribute("href") for key in text
                   for value in urls}
    if result_dict:
        query = random.choice(list(result_dict.keys()))
        search_form = browser.find_element_by_css_selector(search_form_id)
        search_form.clear()
        search_form.send_keys(query)
        search_form.send_keys(Keys.ENTER)
        textes = [label.get_attribute('innerHTML') for label in browser.find_elements_by_css_selector(text_selector)]
        if query not in textes:
            assert False, 'В результатах запроса не содержится ссылка, входящая в базовый запрос'

    assert result_dict, 'Пустой результат запроса'


# проверка работы фильтра по рейтингу
def test_rate_filter(browser):
    filter_selector = '/html/body/div[1]/div[2]/div[1]/div[2]/div/div[3]/span/div[1]/span/div/div/div[4]/ul/li[1]/span/a/section/i'
    browser.get(link)
    search_form = browser.find_element_by_css_selector(search_form_id)
    search_form.send_keys('iphone')
    search_form.send_keys(Keys.ENTER)
    browser.find_element_by_xpath(filter_selector).click()
    elements = [float(rate.get_attribute('innerHTML').split()[0]) for rate in browser.find_elements_by_css_selector(
        'i.a-icon.a-icon-star-small.a-star-small-4-5.aok-align-bottom span')]
    assert len(elements) == len(list(filter(lambda x: x >= 4,
                                            elements))), 'Флильтр по рейтингу (4+) выдает товары с рейтингом ниже заявленного значения'


if __name__ == '__main__':
    unittest.main()
