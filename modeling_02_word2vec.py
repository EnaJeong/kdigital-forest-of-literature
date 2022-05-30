import pandas as pd
from gensim.models import Word2Vec


FILE_TOKEN = './datasets/book_token.csv'
FILE_MODEL = './datasets/book_token_word2Vec.model'


df_book = pd.read_csv(FILE_TOKEN, index_col=0)

tokens = []
for info in df_book['info']:
    token = info.split(' ')
    tokens.append(token)

print(tokens[0])

# embedding model 생성
embedding_model = Word2Vec(tokens, size=100, window=4,  workers=4, iter=100, sg=1)
embedding_model.save(FILE_MODEL)
print(embedding_model.wv.vocab.keys())
print(len(embedding_model.wv.vocab.keys()))

