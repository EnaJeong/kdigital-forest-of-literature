import pandas as pd
from bs4 import BeautifulSoup
import requests


LANGUAGE = 'english'

BOOK_FILE = f'./crawling/book_code_{LANGUAGE}.csv'
SAVE_FILE = f'./crawling/book_{LANGUAGE}.csv'

##############################################################################


def get_url(code):
    return f"http://www.yes24.com/Product/Goods/{code}"


# CSS selectors
CSS_BOOK_INTRO = '#infoset_introduce .txtContentText'
CSS_BOOK_PUB_REVIEW = '#infoset_pubReivew .infoWrap_txt'
CSS_BOOK_IMG = '.gd_imgArea img'

# Attribute for img url
ATTR_IMAGE_URL = 'src'

##############################################################################

df_book = pd.read_csv(BOOK_FILE, index_col=0)

codes = []
titles = []
imgs = []
infos = []

try:
    for book_code in df_book.index:
        title = df_book.loc[book_code]['title']
        # if title < '나는 할머니와 산다':
        #     continue
            
        print(book_code, title)

        url = get_url(book_code)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        img = soup.select(CSS_BOOK_IMG)

        if not img:
            continue

        img = img[0].get('src')

        info = []

        intro = soup.select(CSS_BOOK_INTRO)
        if intro:
            info.append(intro[0].get_text().strip())

        pub_review = soup.select(CSS_BOOK_PUB_REVIEW)
        if pub_review:
            info.append(pub_review[0].get_text().strip())

        imgs.append(img)
        infos.append(' '.join(info))
        codes.append(book_code)
        titles.append(title)

finally:
    df_result = pd.DataFrame({'code': codes, 'title': titles, 'img': imgs, 'info': infos})
    df_result.set_index('code', inplace=True)
    df_result.to_csv(SAVE_FILE)
