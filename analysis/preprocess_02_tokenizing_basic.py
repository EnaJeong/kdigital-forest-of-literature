import pandas as pd
import numpy as np
from konlpy.tag import Komoran
import re

CATEGORY = 'Japan'

TAG_NORMAL = {'NA', 'NF', 'NNG', 'NNP', 'XR'}

CSV_ORIGIN = f"./crawling/cleaned_book_info_{CATEGORY}.csv"
CSV_RESULT = f"./datasets/book_token_{CATEGORY}.csv"

df = pd.read_csv(CSV_ORIGIN, index_col=0)

komoran = Komoran()

cleaned_sentences = []
codes = []

for idx in df.index:
    text = df.loc[idx]['info']

    # 숫자,한글 제외 문자 제거
    text = re.sub('[^가-힣0-9]', ' ', str(text))

    # 문자가 없는 경우 token화 생략
    text = re.sub(r'^\s*$', ' ', text)
    if text == ' ':
        continue

    token = komoran.pos(text) # 품사 별로 token 화
    df_token = pd.DataFrame(token, columns=['word', 'tag'])

    df_cleaned_token = df_token[df_token['tag'].isin(TAG_NORMAL)]['word'] # TAG_NORMAL 에 있는 품사만 뽑아내는 작업
    cleaned_sentence = ' '.join(df_cleaned_token) # 단어들 이어붙이기

    cleaned_sentences.append(cleaned_sentence)
    codes.append(idx)

df_result = df[df.index.isin(codes)].copy()
df_result['info'] = cleaned_sentences

df_result.to_csv(CSV_RESULT)

