import pandas as pd


DIRECTORY = "./analysis/datasets"
ORIGIN_FILE = f"{DIRECTORY}/book_refined_token.csv"
RESULT_FILE = f"{DIRECTORY}/book_info.csv"

df = pd.read_csv(ORIGIN_FILE, index_col=0)
df.drop("info", axis=1, inplace=True)
df.to_csv(RESULT_FILE)
