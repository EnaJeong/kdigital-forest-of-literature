import re

from konlpy.tag import Komoran
import pandas as pd


# tokenizing은 조금 더 테스트가 필요합니다.
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

PAT_NO_KOREAN = re.compile(r"[^가-힣]*")
PAT_QUOTES = re.compile(r"[󰡔󰡕󰡒󰡓\[\]「」『』<>〈〉《》‘’“”]")

PAT_ADDITIONAL = re.compile(r"\([^가-힣]+\)")
PAT_NO_MEANING = re.compile(r'[^가-힣0-9a-zA-Z.,"\'()]')  # r'[^가-힣0-9.,"\'()]' 비교
PAT_PAREN = re.compile(r"[()]")
PAT_OTHERS = re.compile(r'[.,"\']')
PAT_ENGLISH = re.compile(r"[a-zA-Z]")


komoran = Komoran(userdic="./analysis/komoran/user_dic.txt")

try:
    text = None  # exception 확인용
    for category in CATEGORIES:
        origin_file = f"{DIRECTORY}/cleaned_book_info_{category}.csv"
        result_file = f"{DIRECTORY}/book_refined_token_{category}.csv"

        df = pd.read_csv(origin_file, index_col=0)

        codes = []
        for idx in df.index:
            text = df.loc[idx, "info"]

            # 한글이 없는 경우 token화 생략
            if PAT_NO_KOREAN.fullmatch(text):
                continue

            # 한글, 숫자, 문장부호 외 제거
            text = PAT_QUOTES.sub("'", text)  # 특수 기호 조정
            text = PAT_ADDITIONAL.sub("", text)  # 한글 없는 () 제거
            text = PAT_NO_MEANING.sub(" ", text)

            # tokenizing
            token = komoran.pos(text, flatten=True)
            df_token = pd.DataFrame(token, columns=["word", "tag"])

            # 의미 있는 명사만 추출
            keywords = df_token[df_token["tag"].isin(TAG_NORMAL)]["word"]

            # 정제되지 않은 숫자와 단위 제거. 단, 문장의 일부인 경우는 수용
            keywords = keywords[keywords.str.match("[^0-9]|([0-9].+ [가-힣])")]

            keywords_no_space = []
            for word in keywords:
                # ' ' 제거 (' '가 구분자라서 ' '이 있는 경우 하나의 token으로 인식하지 못하기 때문에)
                word = word.replace(" ", "")

                # 괄호가 있는 경우 두 단어가 분리되지 않은 형태로 판단
                word = word.replace("(", " ")
                loc = word.find(")")
                if loc > -1:
                    word = word[:loc]

                # 남은 문장부호들 제거
                word = PAT_OTHERS.sub("", word)

                keywords_no_space.append(word)

            df.loc[idx, "info"] = " ".join(keywords_no_space)
            codes.append(idx)

        df_result = df[df.index.isin(codes)].copy()
        df_result.to_csv(result_file)

except UnicodeDecodeError as e:
    print(e)
    print(text)
