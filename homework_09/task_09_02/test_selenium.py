from selenium import webdriver
from time import sleep


def auto_create_item():
    driver = webdriver.Firefox()
    driver.get('http://127.0.0.1:8000/1/2/addItem')

    element_value = {
        'id_name': 'Пиво "Аливария"',
        'id_description': 'Страна-производитель: Беларусь',
        'id_price': 2,
        'id_comments': 'Классное пиво',
    }

    for key in element_value.keys():
        element = driver.find_element_by_id(key)
        element.send_keys(element_value.get(key))
        sleep(1)
    button = driver.find_elements_by_tag_name('input').pop()
    button.submit()

    sleep(1)

    driver.get('http://127.0.0.1:8000/1')

    sleep(5)

    driver.close()


if __name__ == '__main__':
    auto_create_item()
