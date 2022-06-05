from __future__ import annotations
from collections import namedtuple

import pandas as pd
from bs4 import BeautifulSoup
import requests


NATION = 'spain'

BOOK_CODE_FILE = f'./analysis/data/book_code_{NATION}.csv'
BOOK_INFO_FILE = f'./analysis/data/book_{NATION}.csv'


##############################################################################
def get_url(code):
    return f"http://www.yes24.com/Product/Goods/{code}"


# CSS selectors
CSS_BOOK_AUTH = '.gd_pubArea .gd_auth'
CSS_BOOK_PUB = '.gd_pubArea .gd_pub'
CSS_BOOK_IMG = '.gd_imgArea img'
CSS_BOOK_INTRO = '#infoset_introduce .txtContentText'
CSS_BOOK_PUB_REVIEW = '#infoset_pubReivew .infoWrap_txt'

# Attribute for img url
ATTR_IMAGE_URL = 'src'

FIELDS = ('code', 'title', 'auth', 'pub', 'img', 'info')
Book = namedtuple('Book', FIELDS)

##############################################################################

df_book = pd.read_csv(BOOK_CODE_FILE, index_col=0)
books : list[Book] = []

try:
    for book_code in df_book.index:
        title = df_book.loc[book_code]['title']
        # if title < '나는 할머니와 산다':
        #     continue
            
        print(book_code, title)

        url = get_url(book_code)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        # 이미지 링크
        img = soup.select(CSS_BOOK_IMG)
        if not img:
            continue

        img = img[0].get('src')

        # 작가, 출판사 정보
        auth = soup.select_one(CSS_BOOK_AUTH).get_text().strip()
        pub = soup.select_one(CSS_BOOK_PUB).get_text().strip()

        # 책 소개
        info = []

        intro = soup.select(CSS_BOOK_INTRO)
        if intro:
            info.append(intro[0].get_text().strip())

        pub_review = soup.select(CSS_BOOK_PUB_REVIEW)
        if pub_review:
            info.append(pub_review[0].get_text().strip())

        # 수집한 정보 추가
        books.append(Book(code=book_code, title=title, auth=auth, pub=pub, img=img, info=' '.join(info)))

finally:
    df_result = pd.DataFrame.from_records(books, columns=FIELDS)
    df_result.set_index('code', inplace=True)
    df_result.to_csv(BOOK_INFO_FILE)
