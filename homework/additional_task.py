import pandas as pd
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

df = pd.read_csv('https://raw.githubusercontent.com/AnnSenina/Python_for_CL/main/data/elonmusk.csv', encoding="utf-8")

tweets = df["tweet"].to_string()


# составив частотный список (с нормализацией, удалением пунктуации, токенизацией и удалением стоп-слов)


def normalize(text):
    normalized = text.lower().translate(str.maketrans('', '', string.punctuation))
    return normalized


normalized_tweets = normalize(tweets)


text_list_nltk = word_tokenize(normalized_tweets)


stop_words = stopwords.words('english')


text_clean = []
for word in text_list_nltk:
    if word not in stop_words:
        text_clean.append(word)


word_freqs = Counter(text_clean)
print(word_freqs.most_common(10))