import pandas as pd
import re

FILE_TOKEN = './datasets/book_token.csv'
FILE_KEYWORD = './datasets/book_keyword.csv'

df_book = pd.read_csv(FILE_TOKEN, index_col=0)

PAT_NO_KOREAN = re.compile(r'[^가-힣]*$')

for book_code in df_book.index:
    tokens = df_book.loc[book_code]['info'].split(' ')

    keywords = []
    for token in tokens:
        if PAT_NO_KOREAN.match(token):
            continue

        keywords.append(token)

    df_book.loc[book_code]['info'] = ' '.join(keywords)

df_book.to_csv(FILE_KEYWORD)
