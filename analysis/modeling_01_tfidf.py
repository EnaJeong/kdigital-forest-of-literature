import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle

df_book = pd.read_csv('./datasets/book_keyword.csv', index_col=0)

# tf -> 문장 안의 단어 수 / df -> 모든 문서에서 단어 수 (idx -> inverse dx)
Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_book['info'])

mmwrite('./datasets/tfidf.mtx', Tfidf_matrix)

with open("./datasets/tfidf.pickle", "wb") as f:
    pickle.dump(Tfidf, f)