import re

from konlpy.tag import Komoran
import pandas as pd


DIRECTORY = "./analysis/data"
CATEGORIES = (
    "china",
    "english",
    "europe",
    "france",
    "german",
    "japan",
    "korea_1",
    "korea_2",
    "korea_3",
    "others",
    "russia",
    "spain",
)

TAG_NORMAL = {"NA", "NF", "NNG", "NNP", "XR"}

komoran = Komoran()

for category in CATEGORIES:
    origin_file = f"{DIRECTORY}/cleaned_book_info_{category}.csv"
    result_file = f"{DIRECTORY}/book_token_{category}.csv"

    df = pd.read_csv(origin_file, index_col=0)

    codes = []
    for idx in df.index:
        text = df.loc[idx, "info"]

        # 숫자,한글 제외 문자 제거
        text = re.sub("[^가-힣0-9]", " ", str(text))

        # 문자가 없는 경우 token화 생략
        text = re.sub(r"^\s*$", " ", text)
        if text == " ":
            continue

        # 품사 별로 token 화하여 TAG_NORMAL 품사들만 추출
        token = komoran.pos(text)
        df_token = pd.DataFrame(token, columns=["word", "tag"])
        df_cleaned_token = df_token[df_token["tag"].isin(TAG_NORMAL)]["word"]

        df.loc[idx, "info"] = " ".join(df_cleaned_token)
        codes.append(idx)

    df_result = df[df.index.isin(codes)]
    df_result.to_csv(result_file)
    print(df_result.head())
