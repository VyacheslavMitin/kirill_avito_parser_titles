import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

from lxml import html

# КОНСТАНТЫ
DRIVER = webdriver.Chrome()
DT_NOW = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')
LIST_DATA = []


def read_links() -> list[str]:
    """Функция чтения файла со ссылками"""
    with open("links.txt", 'r', encoding='utf-8') as file_links:
        file_links_output = file_links.read()
    file_links_output = file_links_output.split('\n')
    return file_links_output


def read_cities() -> list[str]:
    """Функция чтения файла с городами"""
    with open('cities.txt', 'r', encoding='utf-8') as file_cities:
        file_cities_output = file_cities.read()
    file_cities_output = file_cities_output.split('\n')
    return file_cities_output


def parse(link):
    """Функция парсинга ссылок"""
    titles = []
    # prices = []
    ret = ""
    cat_list = ""
    no = [False, False, False, ]
    is_count = False
    count = ""
    req_ = ""

    for y in range(5):
        if no[y - 2]:
            continue
        else:
            DRIVER.get(f"{link}&p={y}")
            html_doc = DRIVER.page_source
            lx = html.fromstring(html_doc)

            titles_list = lx.xpath('//h3[@itemprop="name"]/text()')
            # prices1 = lx.xpath('//p[@data-marker="item-price"]/strong/span/text()')
            category = lx.xpath('//span[@itemprop="itemListElement"]/a/span/text()')
            is_count = DRIVER.find_element(By.XPATH, '//span[@data-marker="page-title/count"]').is_enabled()
            if is_count:
                count = lx.xpath('//span[@data-marker="page-title/count"]/text()')[0]
                count = count.replace("\xa0", "")
                count = int(count)
                # print(count)
                pages = count // 50
                # print(pages)
                for z in range(8 - pages):
                    no[-z] = True

            for cat_split in category:
                # item = cat_split
                cat_list += f"-> {cat_split} "

            req_ = category[-1]

            for title in titles_list:
                if title in titles_list:
                    titles.append(title)
            titles = set(titles)  # удаление дублей через превращение в множество и обратно в список
            titles = list(titles)

    ret += f"Дата и время парсинга Авито: {DT_NOW}\n\n"

    if is_count:
        ret += f"Объявлений найдено: {count}\n\n"
    else:
        return f"Объявлений не найдено D:"

    ret += f"Категория {cat_list}\n"

    for z in range(len(titles)):
        ret += f'{titles[z]}\n'

    return ret, req_


if __name__ == '__main__':

    links = read_links()
    i = 0

    for element in links:
        rdata = parse(element)
        data = rdata[0]
        req = rdata[1]
        i += 1
        with open(f"{req}-{DT_NOW}.txt", 'w+', encoding='utf-8') as file:
            print(f"Ссылка №{i}")
            file.write(data)

    DRIVER.close()
