from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import json
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'

driver = webdriver.Chrome(
    'C:\\Users\이수민\Desktop\chromedriver_win32\chromedriver.exe', chrome_options=options)


def no_space(text):
    text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', text)
    text2 = re.sub('\n\n', '', text1)
    text2.strip()
    return text2


def crawl(target_url, pageNum):
    driver.get(target_url)

    time.sleep(1)

    soup = bs(driver.page_source, 'html.parser')

    # 1 book
    for links in soup.find_all("b"):
        arr = []
        bookName = links.get_text()
        print(bookName)
        if(bookName == '7년의 밤' or bookName == '베르나르 베르베르의 상상력 사전' or bookName == '청년 반크, 세계를 품다' or bookName == '서찰을 전하는 아이' or bookName == '박씨 부인전' or bookName == '책과 노니는 집' or bookName == '책 먹는 여우' or bookName == '잘못 뽑은 반장' or bookName == '여행의 이유' or bookName == '기억 전달자' or bookName == '신경 끄기의 기술' or bookName == 'The Secret 시크릿' or bookName == '마당을 나온 암탉' or bookName == '조금만 기다려 봐' or bookName == '고릴라' or bookName == 'YES24 중고 상품 포장팩 3호 묶음(10장)' or bookName == '휘리리후 휘리리후' or bookName == '아홉 켤레의 구두로 남은 사내' or bookName == '수상한 진흙' or bookName == '그래요 정말 그래요!' or bookName == '오른발 왼발' or bookName == '박지원의 한문소설' or bookName == 'YES24 중고 상품 포장팩 2호 묶음(10장)' or bookName == '총, 균, 쇠' or bookName == '제랄다와 거인' or bookName == '샬롯의 거미줄'):
            continue

        # if(bookName == '달러구트 꿈 백화점'):
        #     continue

        url = links.parent.get('href')
        time.sleep(1)
        driver.get(url)

        soup1 = bs(driver.page_source, 'html.parser')

        # category
        if(len(soup1.find_all("a", {"class": "yLocaDepth"})) > 2):
            cat = no_space(soup1.find_all(
                "a", {"class": "yLocaDepth"})[2].get_text())
        else:
            cat = '없음'

        # year
        year = no_space(soup1.find("span", {"class": "gd_date"}).get_text())

        # origin price
        originPrice = re.sub(r'[^0-9]', '', driver.find_element_by_xpath(
            '//*[@id="yHubTopWrap"]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td').text)

        books = 0
        priceBooks = 0

        time.sleep(1)
        # 1page books
        for kk in soup1.find_all("span", {"class": "ico_used"}):

            books += 1
            priceBooks += 1
            print(books)
            arr.append(bookName)
            arr.append(cat.strip())
            arr.append(year)
            arr.append(kk.get_text())
            arr.append(originPrice)

            discountPrice = re.sub(r'[^0-9]', '', driver.find_elements_by_css_selector(
                'div.info_price > strong > em.yes_b')[books-1].text)

            print(books, priceBooks)
            if(int(originPrice) <= int(discountPrice)):
                percent = '마이너스'
                priceBooks -= 1
            else:
                percent = driver.find_elements_by_css_selector(
                    'div.info_price > span > em.num')[priceBooks-1].text
            arr.append(percent)

            # print(kk.get_text())

            bookClick = driver.find_elements_by_css_selector(
                'a.gd_name')[priceBooks-1].get_attribute('href')
            print(bookClick)

            driver.get(bookClick)

            soup2 = bs(driver.page_source, 'html.parser')
            for bookClickOne in soup2.find_all("td", {"class": "txt ac"}):
                arr.append(bookClickOne.get_text().strip())
                # print(bookClickOne.get_text().strip())

            arr.append('/')

            driver.back()
            bs(driver.page_source, 'html.parser')

        # page init
        lens = 0
        nextTrue = False

        # page nums
        for kkk in soup1.find("div", {"data-search-type": "page"}).children:
            if(not str(kkk).isspace()):
                print(kkk)
                lens += 1

        if(bookName == "The Secret 시크릿"):
            lens = 24

        elif(bookName == "모모"):
            lens = 11

        elif(bookName == "자전거 도둑"):
            lens = 15

        elif(bookName == "연금술사"):
            lens = 12

        elif(bookName == "인생 수업"):
            lens = 12

        elif(bookName == "재주 많은 다섯 친구"):
            lens = 3

        elif(bookName == "책 먹는 여우"):
            lens = 11

        elif(bookName == "우리들의 일그러진 영웅"):
            lens = 17

        for page in range(2, lens+1):
            print("페이지")
            print(page)

            # 11페이지
            if(page == 11 or page == 21 or page == 31):
                driver.find_element_by_link_text('다음').send_keys('\n')

            else:
                driver.find_element_by_link_text(str(page)).send_keys('\n')

            bs(driver.page_source, 'html.parser')

            books = 0
            priceBooks = 0
            aa = []
            time.sleep(2)
            for kkkk in driver.find_elements_by_class_name("ico_used"):
                aa.append(kkkk.text)
            print(aa)
            for ks in aa:

                books += 1
                priceBooks += 1
                print(books)
                obj = {}
                arr.append(bookName)
                arr.append(cat.strip())
                arr.append(year)
                time.sleep(2)
                arr.append(ks)
                arr.append(originPrice)

                discountPrice = re.sub(r'[^0-9]', '', driver.find_elements_by_css_selector(
                    'div.info_price > strong > em.yes_b')[books-1].text)

                print(books, priceBooks)
                if(int(originPrice) - 999 <= int(discountPrice)):
                    percent = '마이너스'
                    priceBooks -= 1
                else:
                    percent = driver.find_elements_by_css_selector(
                        'div.info_price > span > em.num')[priceBooks-1].text
                arr.append(percent)

                bookClick = driver.find_elements_by_css_selector(
                    'a.gd_name')[priceBooks-1].get_attribute('href')
                print(bookClick)

                # ------
                driver.get(bookClick)

                soup3 = bs(driver.page_source, 'html.parser')
                for bookClickOne in soup3.find_all("td", {"class": "txt ac"}):
                    arr.append(bookClickOne.get_text().strip())

                arr.append('/')

                driver.back()
                bs(driver.page_source, 'html.parser')

        time.sleep(1)
        driver.back()
        # print(arr)
        with open('test' + bookName + str(pageNum) + '.txt', 'w', encoding='UTF-8') as f:
            for name in arr:
                f.write(name + '\n')

    # with open('testt' + str(pageNum) + '.txt', 'w', encoding='UTF-8') as f:
    #     for name in arr:
    #         f.write(name + '\n')


for i in range(10, 11):
    crawl('http://www.yes24.com/24/Category/BestSeller?CategoryNumber=018&sumgb=06&PageNumber='+str(i), i)
    time.sleep(2)
# crawl('http://www.yes24.com/24/Category/BestSeller?CategoryNumber=018&sumgb=06&PageNumber=1')


# bookClick = driver.find_elements_by_css_selector(
#                     'a.gd_name')[priceBooks-1]
# bookClick.send_keys(Keys.CONTROL +"\n")

# last_tab = driver.window_handles[-1]
# driver.switch_to.window(window_name=last_tab)
