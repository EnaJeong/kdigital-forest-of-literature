import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

categories = {"China": "017001045023", "english": "017001045007", 'Europe': "",
              'France': "", 'german': "", 'Japan': "",
              'Korea': "", 'others': "", 'russian': "", 'spanish': ""}

##############################################################################
def get_url(national_code, page=1):
    return f"http://www.yes24.com/24/Category/Display/{national_code}?ParamSortTp=03&AO=2&PageNumber={page}"


# CSS selector
CSS_BOOK_TITLE = '#category_layout .goods_name > a:first-of-type'
CSS_AUTH = '#category_layout .goods_auth'
CSS_PUB = '#category_layout .goods_pub'
CSS_END_BUTTON = '.bgYUI.end'

# Attribute for book code & RE patterns
ATTR_BOOK_CODE = 'href'
PAT_BOOK_CODE = re.compile(r'Goods/(.+)$')

# Attribute for novel code & RE patterns
ATTR_END_PAGE = 'href'
PAT_END_PAGE = r'(?<=PageNumber=).+$'

# 체험판 제외
REMOVAL_TYPE = "체험판"
##############################################################################

for category, national_code in categories.items():
    save_file = f'./data_raw/book_additional_{category}.csv'

    url = get_url(national_code)
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    end_btn = soup.select(CSS_END_BUTTON)[0]
    end_page = re.search(PAT_END_PAGE, end_btn.get(ATTR_END_PAGE)).group()

    code_list = []
    auth_list = []
    pub_list = []

    for page in range(1, int(end_page) + 1):
        url = get_url(national_code, page)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        books = soup.select(CSS_BOOK_TITLE)
        auths = soup.select(CSS_AUTH)
        pubs = soup.select(CSS_PUB)

        for i, book in enumerate(books):
            if REMOVAL_TYPE in book.text:
                continue

            code = PAT_BOOK_CODE.findall(book.get(ATTR_BOOK_CODE))[0]
            code_list.append(code)
            auth_list.append(auths[i].get_text().strip())
            pub_list.append(pubs[i].get_text().strip())

    df_result = pd.DataFrame({'code': code_list, 'auth': auth_list, 'pub': pub_list})
    df_result.set_index('code', inplace=True)
    df_result.to_csv(save_file)
    print(df_result)
