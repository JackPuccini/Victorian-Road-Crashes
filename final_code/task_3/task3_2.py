import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import os

# input path
INPUT_CSV_PATH = "/course/filtered_vehicle.csv"
# output path
OUTPUT_PLOT_PATH = "task3_2_elbow.png"


def task3_2():

    df = pd.read_csv(INPUT_CSV_PATH, encoding="utf-8")

    # define grouping columns and feature columns
    grouping_cols = ["VEHICLE_YEAR_MANUF", "VEHICLE_BODY_STYLE", "VEHICLE_MAKE"]
    feature_cols = [
        "NO_OF_WHEELS",
        "NO_OF_CYLINDERS",
        "SEATING_CAPACITY",
        "TARE_WEIGHT",
        "TOTAL_NO_OCCUPANTS",
    ]

    # group by three features and calculate the average value of the specified feature column
    grouped_data = df.groupby(grouping_cols)[feature_cols].mean().reset_index()

    # select numerical features for clustering purposes only
    features_for_clustering = grouped_data[feature_cols]

    scaler = MinMaxScaler()
    # assumin features_for_clustering has no NaN value
    normalized_features = scaler.fit_transform(features_for_clustering)

    # use elbow rules
    sse = []  #  Sum of Squared Errors / Inertia
    k_range = range(1, 11)  # setting k range from 1 to 10

    for k in k_range:
        # use random_state to ensure the result can be reproduced
        kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
        kmeans.fit(normalized_features)
        sse.append(kmeans.inertia_)
        print(f"  k={k}, SSE={kmeans.inertia_:.2f}")

    # produce line plot
    plt.figure(figsize=(10, 6))
    plt.plot(k_range, sse, marker="o", linestyle="-")
    plt.xlabel("k")
    plt.ylabel("Sum of Squared Errors")
    plt.title("Elbow Method for Determining Optimal k")
    plt.xticks(k_range)
    plt.grid(True, linestyle="--", alpha=0.6)

    # save graph
    plt.savefig(OUTPUT_PLOT_PATH)
    print(f"elbow graph were saved in {OUTPUT_PLOT_PATH}")

    # close garph
    plt.close()


task3_2()
