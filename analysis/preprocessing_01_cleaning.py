import re

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

PAT_BLANK = re.compile(r"\s")

for category in CATEGORIES:
    origin_file = f"{DIRECTORY}/book_info_{category}.csv"
    result_file = f"{DIRECTORY}/cleaned_book_info_{category}.csv"

    df = pd.read_csv(origin_file, index_col=0)
    df.dropna(axis=0, how="any", subset=["info"], inplace=True)

    # 공백 제거
    for idx in df.index:
        info = df.loc[idx]["info"]
        df.loc[idx]["info"] = PAT_BLANK.sub(" ", info)

    df.to_csv(result_file)
    print(df.info(), "\n")
