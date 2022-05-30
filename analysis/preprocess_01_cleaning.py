import pandas as pd
import re

categories = ["China", "english", 'Europe', 'France', 'german', 'Japan',
              'Korea_1', 'Korea_2', 'Korea_3', 'others', 'russian', 'spanish']

PAT_BLANK = re.compile(r'\s')

for category in categories:
    df = pd.read_csv(f'./crawling/book_info_{category}.csv', index_col=0)

    # info가 null인 항목 제거
    df.dropna(axis=0, how='any', subset=["info"], inplace=True)

    # 공백 제거
    for idx in df.index:
        info = df.loc[idx]['info']
        df.loc[idx]['info'] = PAT_BLANK.sub(' ', info)

    df.to_csv(f'./crawling/cleaned_book_info_{category}.csv')
    print(df.info(), '\n')
