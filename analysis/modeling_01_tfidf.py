import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite


FILE_INPUT = "./analysis/datasets/book_token.csv"
FILE_MATRIX = "./analysis/datasets/tfidf.mtx"
FILE_PICKLE = "./analysis/datasets/tfidf.pickle"


df_book = pd.read_csv(FILE_INPUT, index_col=0)

# tf -> 문장 안의 단어 수 / df -> 모든 문서에서 단어 수 (idx -> inverse dx)
Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_book["info"])

mmwrite(FILE_MATRIX, Tfidf_matrix)

with open(FILE_PICKLE, "wb") as f:
    pickle.dump(Tfidf, f)
