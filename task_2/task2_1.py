import re
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk import word_tokenize
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer

stopwords = set(stopwords.words("english"))


def text_preprocess(s):
    s = s.lower()
    s = re.sub(r"\.(?=\w)", ". ", s)
    s = re.sub(r"[^A-Za-z\s]", " ", s)
    s = re.sub(r"\s+", " ", s)
    tokens = word_tokenize(s)
    tokens = [w for w in tokens if not w in stopwords]

    return " ".join(tokens)


def task2_1():

    accident_df = pd.read_csv("data/accident.csv")

    accident_df["DCA_DESC_CLEANED"] = accident_df["DCA_DESC"].apply(lambda s: s.lower())
    accident_df["DCA_DESC_CLEANED"] = accident_df["DCA_DESC_CLEANED"].apply(
        text_preprocess
    )

    # Join all descriptions into one string
    all_text = " ".join(accident_df["DCA_DESC_CLEANED"].dropna())

    # Generate word cloud for top 20 words
    wordcloud = WordCloud(
        width=800, height=400, background_color="white", max_words=20
    ).generate(all_text)

    vectorizer = CountVectorizer()
    # BoW vectors created here as required - although not necessary for plotting
    bow = vectorizer.fit_transform(accident_df["DCA_DESC_CLEANED"])

    # Plot, save and show
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("task2_1_word_cloud.png")
    plt.show()

    accident_df.to_csv("data/accident_adjusted.csv")


task2_1()
