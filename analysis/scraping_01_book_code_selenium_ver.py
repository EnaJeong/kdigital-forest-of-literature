import os
import re

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


NATION = "spain"
DIRECTORY = './analysis/data'

CATEGORIES = {
    "korea": "017001045006", 
    "english": "017001045007",
    "japan": "017001045008",
    "china": "017001045023", 
    "france": "017001045010", 
    "germany": "017001045011", 
    "russia": "017001045012", 
    "spain": "017001045013", 
    "europe": "017001045014",
    "others": "017001045015", 
}

national_code = CATEGORIES[NATION]
file_name = f"{DIRECTORY}/book_code_{NATION}.csv"

##############################################################################
CHROMEDRIVER = "./resources/chromedriver_win.exe"  # "./resources/chromedriver_linux"


def get_url(page=1):
    return f"http://www.yes24.com/24/Category/Display/{national_code}?ParamSortTp=03&AO=2&PageNumber={page}"


# CSS selector
CSS_BOOK_TITLE = '#category_layout .goods_name > a:first-of-type'
CSS_END_BUTTON = '.bgYUI.end'

# Attributes & RE patterns
ATTR_BOOK_CODE = 'href'
PAT_BOOK_CODE = re.compile(r'Goods/(.+)$')

ATTR_END_PAGE = 'href'
PAT_END_PAGE = r'(?<=PageNumber=).+$'

# 체험판 제외
REMOVAL_TYPE = "체험판"
##############################################################################

# Chromedriver 설정
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome(CHROMEDRIVER, options=options)

# 목록 첫 페이지로 이동
driver.get(get_url())

# 제일 마지막 페이지 정보 수집
end_btn = driver.find_elements(By.CSS_SELECTOR, CSS_END_BUTTON)[0]
end_page = re.search(PAT_END_PAGE, end_btn.get_attribute(ATTR_END_PAGE)).group()

# 책코드와 책 제목 수집
titles = {}

try:
    for page in range(1, int(end_page) + 1):
        # 목록의 해당 페이지로 이동
        url = get_url(page)
        driver.get(url)

        # 책 제목들 찾기
        books = driver.find_elements(By.CSS_SELECTOR, CSS_BOOK_TITLE)

        for book in books:
            # 수집목록에서 제외하고 싶은 책
            if REMOVAL_TYPE in book.text:
                continue

            # 정규식 이용해서 책 code 추출
            code = PAT_BOOK_CODE.findall(book.get_attribute(ATTR_BOOK_CODE))[0]

            # 책 코드와 책 제목 dictionary에 추가
            titles[code] = book.text

    # 수집한 code와 title 정보 csv로 저장
    df_title = pd.DataFrame(titles.items(), columns=['code', 'title'])
    df_title.set_index('code', inplace=True)

    if not os.path.exists(DIRECTORY):
        os.mkdir(DIRECTORY)
    df_title.to_csv(file_name)

    print(df_title)

finally:
    driver.close()
