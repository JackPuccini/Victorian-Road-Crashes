from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt


# 6:00AM - 11:59AM → Morning
# 12:00PM - 5:59PM → Afternoon
# 6:00PM - 11:59PM → Evening
# 12:00AM - 5:59AM → Late Night

# Based on the above, we have:
# 00:00:00 - 05:59:00 = Late Night
# 06:00:00 - 11:59:00 = Morning
# 12:00:00 - 17:59:00 = Afternoon
# 18:00:00 - 23:59:00 = Evening


def convert_time(s):
    try:
        hour = int(s[:2])
        if hour < 6:
            return "Late Night"
        elif hour < 12:
            return "Morning"
        elif hour < 18:
            return "Afternoon"
        elif hour < 24:
            return "Evening"
    except:
        return "Unknown"


def task2_2():

    # Use adjusted data from task2_1
    accident_df = pd.read_csv("data/accident_adjusted.csv")

    # --------------- Bar Chart 1 --------------- #

    accident_df["TIME_OF_DAY"] = accident_df["ACCIDENT_TIME"].apply(convert_time)
    grouped_time = accident_df.groupby("TIME_OF_DAY").size()
    grouped_time.plot(kind="bar")
    plt.title("Number of Accidents by Time of Day")
    plt.xlabel("Time of Day")
    plt.ylabel("Number of Accidents")
    plt.xticks(rotation=50)
    plt.tight_layout()
    plt.savefig("task2_2_timeofday.png", bbox_inches="tight")
    plt.show()

    # --------------- Pie Charts --------------- #

    grouped_text = (
        accident_df.groupby("TIME_OF_DAY")["DCA_DESC_CLEANED"]
        .agg(" ".join)
        .reset_index()
    )

    top_words_by_time = {}

    # Loop through each time of day group
    for _, row in grouped_text.iterrows():
        time_of_day = row["TIME_OF_DAY"]
        text = row["DCA_DESC_CLEANED"]

        tokens = text.split()
        # Use Counter to retrieve word counts dict
        counter = Counter(tokens)
        top_words = counter.most_common(10)

        top_words_by_time[time_of_day] = top_words

    afternoon_words = top_words_by_time["Afternoon"]
    morning_words = top_words_by_time["Morning"]
    evening_words = top_words_by_time["Evening"]
    late_night_words = top_words_by_time["Late Night"]

    # Plot side by side pie charts (2 rows x 2 columns)
    fig, axes = plt.subplots(2, 2, figsize=(20, 10))

    axes[0][0].pie(
        [x[1] for x in afternoon_words],
        labels=[x[0] for x in afternoon_words],
        labeldistance=1.1,
        autopct="%1.0f%%",
        textprops={"fontsize": 8},
        startangle=90,
    )
    axes[0][0].set_title("Afternoon Words")

    axes[0][1].pie(
        [x[1] for x in morning_words],
        labels=[x[0] for x in morning_words],
        labeldistance=1.1,
        autopct="%1.0f%%",
        textprops={"fontsize": 8},
        startangle=90,
    )
    axes[0][1].set_title("Morning Words")

    axes[1][0].pie(
        [x[1] for x in evening_words],
        labels=[x[0] for x in evening_words],
        labeldistance=1.1,
        autopct="%1.0f%%",
        textprops={"fontsize": 8},
        startangle=90,
    )
    axes[1][0].set_title("Evening Words")

    axes[1][1].pie(
        [x[1] for x in late_night_words],
        labels=[x[0] for x in late_night_words],
        labeldistance=1.1,
        autopct="%1.0f%%",
        textprops={"fontsize": 8},
        startangle=90,
    )
    axes[1][1].set_title("Late Night Words")

    plt.suptitle(
        "Top 10 Accident Description Words by Time of Day", fontsize=16, y=1.05
    )
    plt.tight_layout()
    plt.savefig("task2_2_wordpies.png", bbox_inches="tight")
    plt.show()

    # --------------- Stacked Bar Chart --------------- #

    grouped_time = accident_df.groupby(["TIME_OF_DAY", "DAY_WEEK_DESC"]).size()
    stack_data = grouped_time.unstack(fill_value=0)[["Monday", "Friday", "Sunday"]]
    stack_data.plot(kind="bar", stacked=True)
    plt.xticks(rotation=50)
    plt.title("Number of Accidents By Time of Day, By Day")
    plt.xlabel("Time of Day")
    plt.ylabel("Number of Accidents")
    plt.tight_layout()
    plt.legend()
    plt.savefig("task2_2_stackbar.png")
    plt.show()


task2_2()
