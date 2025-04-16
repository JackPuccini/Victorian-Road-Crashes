import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import string
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

stopwords = set(stopwords.words("english"))


# classity a day into four time period
def classification(time):
    try:
        hour = int(time[0:2])
    except:
        return None

    if 6 <= hour <= 11:
        return "Morning"
    if 12 <= hour <= 17:
        return "Afternoon"
    if 18 <= hour <= 23:
        return "Evening"
    else:
        return "Late Night"


# delete stopwrods
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


def task2_2():
    # load data
    df = pd.read_csv("/course/accident.csv")
    # delete missing data
    df = df.dropna(subset=["ACCIDENT_TIME", "DCA_DESC"])
    # make each accident corespond to a time period
    df["TIME_PERIOD"] = df["ACCIDENT_TIME"].apply(classification)
    # delete the accidents that the time can not be classified
    df = df.dropna(subset=["TIME_PERIOD"])

    # Bar chart: timeofday
    count = (
        df["TIME_PERIOD"]
        .value_counts()
        .reindex(["Morning", "Afternoon", "Evening", "Late Night"])
    )
    plt.figure(figsize=(10, 10))
    count.plot(kind="bar", color="green")
    plt.xlabel("TIME_PERIOD")
    plt.ylabel("NUMBER_OF_ACCIDENTS")
    plt.title("NUMBER_OF_ACCIDENTS_BY_TIME_PERIOD")
    plt.tight_layout()
    plt.savefig("task2_2_timeofday.png")
    plt.close()

    # Pie chart: wordpies
    fig, axs = plt.subplots(2, 2, figsize=(20, 20))
    time_period = [["Morning", "Afternoon"], ["Evening", "Late Night"]]
    for i in range(2):
        for j in range(2):
            period = time_period[i][j]
            filtered_table1 = df[df["TIME_PERIOD"] == period]
            cleaned_text = preprocessing(
                filtered_table1["DCA_DESC"].dropna(axis=0, how="any")
            )
            # build bag of words model
            vectorizer = CountVectorizer()
            vectorizer.fit(cleaned_text)
            matrix = vectorizer.transform(cleaned_text)
            array = matrix.toarray()
            # calculate the frequency of words
            totalnum = array.sum(axis=0)
            words = vectorizer.get_feature_names_out()
            frequency = {word: freq for word, freq in zip(words, totalnum)}
            # filter top 10 words
            top_10_words = dict(
                sorted(frequency.items(), key=lambda i: i[1], reverse=True)[0:10]
            )
            # generate graph
            axs[i, j].pie(
                top_10_words.values(),
                labels=top_10_words.keys(),
                autopct="%1.2f%%",
                textprops={"fontsize": 20},
            )
            axs[i, j].set_title(
                f"Top 10 words related to {period} accidents", fontsize=30
            )
    plt.tight_layout()
    plt.savefig("task2_2_wordpies.png")
    plt.close()

    # Bar chart: stackbar
    df["DAY_OF_WEEK"] = pd.to_datetime(df["ACCIDENT_DATE"]).dt.day_name()
    day_labels = ["Monday", "Friday", "Sunday"]
    day = [day in day_labels for day in df["DAY_OF_WEEK"]]
    filtered_table2 = df[day]
    bar_chart = (
        filtered_table2.groupby(["DAY_OF_WEEK", "TIME_PERIOD"])
        .size()
        .unstack()
        .fillna(0)
    )
    bar_chart = bar_chart[["Morning", "Afternoon", "Evening", "Late Night"]]
    bar_chart.plot(kind="bar", stacked=True, figsize=(10, 10))
    plt.xlabel("Day of week")
    plt.ylabel("Number of accidents")
    plt.title("Number of accidents on Monday,Friday and Sunday")
    plt.tight_layout()
    plt.savefig("task2_2_stackbar.png")
    plt.close()


# call the funciton and run the task
task2_2()
