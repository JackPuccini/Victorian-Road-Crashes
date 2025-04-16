import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords

# download list of stopwords
nltk.download("stopwords")

stopwords = set(stopwords.words("english"))


# delete stopwords
def stopword_removing(text):
    # divid the text into single words
    words = text.split()
    cleaned_words = []
    for i in words:
        # keep the word if it is not a stopword
        if i not in stopwords:
            cleaned_words.append(i)
    # get a string without stopwrods
    return " ".join(cleaned_words)


# New pre processing step to avoid the words like 'objectparked'
def preprocessing(text_series):
    # Convert to lowercase
    text_series = text_series.str.lower()

    # Replace punctuation with spaces instead of deleting
    text_series = text_series.str.replace(r"[^\w\s]", " ", regex=True)

    # Normalize multiple spaces to a single space
    text_series = text_series.str.replace(r"\s+", " ", regex=True)

    # Remove stopwords
    text_series = text_series.apply(stopword_removing)

    return text_series


def task2_1():
    # load the data
    df = pd.read_csv("/course/accident.csv")
    # delete missing values
    cleaned_text = preprocessing(df["DCA_DESC"].dropna(axis=0, how="any"))
    # create the bag of words model
    vectorizer = CountVectorizer()
    vectorizer.fit(cleaned_text)
    matrix = vectorizer.transform(cleaned_text)
    array = matrix.toarray()
    # get the total number of words
    totalnum = array.sum(axis=0)
    # get the name of the words
    words = vectorizer.get_feature_names_out()
    # get the word-frequency dictionary
    frequency = {word: freq for word, freq in zip(words, totalnum)}
    top_20_words = dict(
        sorted(frequency.items(), key=lambda i: i[1], reverse=True)[0:20]
    )

    # get the wordcloud for top 20 words
    wordcloud = WordCloud(
        width=800, height=800, background_color="white"
    ).generate_from_frequencies(top_20_words)

    # generate the graph
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("20 most frequent words occurring in accident descriptions")
    plt.savefig("task2_1_word_cloud.png")
    plt.close()


# run the task
task2_1()
