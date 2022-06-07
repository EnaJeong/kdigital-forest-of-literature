import os
import re
from sre_parse import CATEGORIES

from bs4 import BeautifulSoup
import pandas as pd
import requests


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
def get_url(page=1):
    return f"http://www.yes24.com/24/Category/Display/{national_code}?ParamSortTp=03&AO=2&PageNumber={page}"


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

# 수집한 code와 title 정보 csv로 저장
df_title = pd.DataFrame(titles.items(), columns=['code', 'title'])
df_title.set_index('code', inplace=True)

if not os.path.exists(DIRECTORY):
    os.mkdir(DIRECTORY)
df_title.to_csv(file_name)

print(df_title)
