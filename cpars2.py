from selenium import webdriver
from selenium.webdriver.common.by import By

from lxml import html

import os
import datetime

# Consts
driver = webdriver.Chrome()
i = 0

def readlinks():
    with open("links.txt", 'r', encoding='utf-8') as l:
        f = l.read()
    f = f.split('\n')
    return f

def readcities():
    with open('cities.txt', 'r', encoding='utf-8') as c:
        f = c.read()
    f = f.split('\n')
    return f

def parse(link):
    titles = []
    prices = []
    ret = ""
    catlist = ""
    no = [False, False, False,]
    for i in range(5):
        if no[i-2]:
            continue
        else:
            driver.get(f"{link}&p={i}")
            html_doc = driver.page_source
            lx = html.fromstring(html_doc)


            titleslist = lx.xpath('//h3[@itemprop="name"]/text()')
            # prices1 = lx.xpath('//p[@data-marker="item-price"]/strong/span/text()')
            category = lx.xpath('//span[@itemprop="itemListElement"]/a/span/text()')
            iscount = driver.find_element(By.XPATH, '//span[@data-marker="page-title/count"]').is_enabled()
            if iscount:
                count = lx.xpath('//span[@data-marker="page-title/count"]/text()')[0]
                count = count.replace("\xa0", "")
                count = int(count)
                print(count)
                pages = count // 50
                print(pages)
                for i in range(8 - pages):
                    no[-i] = True

            for catsplit in category:
                item = catsplit
                catlist += f"-> {catsplit} "
    
            req = category[-1]
                        
            for title in titleslist:
                if title:
                    titles.append(title)
    
    ret += f"Дата парсинга: {datetime.datetime.now()}\n"
    if iscount:
        ret += f"Объявлений найдено: {count}\n"
    else:
        return f"Объявлений не найдено D:"
    
    ret += f"Категория {catlist}\n"
    
    for i in range(len(titles)):
        ret += f'{titles[i]}\n'    
    
    return ret, req

if __name__ == '__main__':
    links = readlinks()
    for link in links:
            rdata = parse(link)
            data = rdata[0]
            req = rdata[1]
            i += 1
            dtnow = str(datetime.datetime.now())
            dtnow = dtnow.split(" ")[0]
            with open(f"{req}-{dtnow}.txt", 'w+', encoding='utf-8') as f:
                f.write(data)
                print(f"Ссылка №{i}")
            
    driver.close()
