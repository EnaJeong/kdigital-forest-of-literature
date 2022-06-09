import os

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

RESULT_DIRECTORY = "./analysis/datasets"
RESULT_FILE = f"{RESULT_DIRECTORY}/book_token.csv"


dfs = []

for category in CATEGORIES:
    df = pd.read_csv(f"{DIRECTORY}/book_token_{category}.csv", index_col=0)
    print(df.head())
    dfs.append(df)


df: pd.DataFrame = pd.concat(dfs)
print(df.info())

print("------------------------------------")

# info 없는 row 삭제
df.dropna(axis=0, how="any", subset=["info"], inplace=True)
print(df.info())

print("------------------------------------")

# 중복 제거
df.reset_index(inplace=True)
df.drop_duplicates("code", inplace=True)
df.set_index("code", inplace=True)
print(df.info())

print("------------------------------------")

# 이름순 정렬
df = df.loc[df["title"].sort_values().index]
print(df.info())

if not os.path.exists(RESULT_DIRECTORY):
    os.mkdir(RESULT_DIRECTORY)
df.to_csv(RESULT_FILE)
