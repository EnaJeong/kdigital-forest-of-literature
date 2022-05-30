import pandas as pd

categories = ["China", "english", 'Europe', 'France', 'german', 'Japan',
              'Korea_1', 'Korea_2', 'Korea_3', 'others', 'russian', 'spanish']


dfs = []

for category in categories:
    df = pd.read_csv(f'./datasets/book_token_{category}.csv', index_col=0)
    print(df.head())
    dfs.append(df)


df = pd.concat(dfs)
print(df.info())

print('------------------------------------')

# info 없는 row 삭제
df.dropna(axis=0, how="any", subset=["info"], inplace=True)
print(df.info())

print('------------------------------------')

# 중복 제거
df.reset_index(inplace=True)
df.drop_duplicates('code', inplace=True)
df.set_index('code', inplace=True)
print(df.info())

print('------------------------------------')

# 이름순 정렬
df = df.loc[df['title'].sort_values().index]
print(df.info())

df.to_csv('./datasets/book_token.csv')
