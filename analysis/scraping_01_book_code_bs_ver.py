import pandas as pd
from bs4 import BeautifulSoup
import requests
import re


NATIONAL_CODE = "017001045013"
FILE_NAME = './crawling/book_code_spanish.csv'


##############################################################################
def get_url(page=1):
    return f"http://www.yes24.com/24/Category/Display/{NATIONAL_CODE}?ParamSortTp=03&AO=2&PageNumber={page}"


# CSS selector
# CSS_BOOK_TITLE = '#category_layout .goods_name > a:nth-of-type(1)'
CSS_BOOK_TITLE = '#category_layout .goods_name > a:first-of-type'   # 동작하지 않는 경우에는 위 코드 사용
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

url = get_url()
soup = BeautifulSoup(requests.get(url).text, 'html.parser')

end_btn = soup.select(CSS_END_BUTTON)[0]
end_page = re.search(PAT_END_PAGE, end_btn.get(ATTR_END_PAGE)).group()

titles = {}

for page in range(1, int(end_page) + 1):
    url = get_url(page)
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    books = soup.select(CSS_BOOK_TITLE)

    for book in books:
        if REMOVAL_TYPE in book.text:
            continue

        code = PAT_BOOK_CODE.findall(book.get(ATTR_BOOK_CODE))[0]
        titles[code] = book.text

# 모은 책 code 정보 csv로 저장
df_title = pd.DataFrame(titles.items(), columns=['code', 'title'])
df_title.set_index('code', inplace=True)
df_title.to_csv(FILE_NAME)

print(df_title)