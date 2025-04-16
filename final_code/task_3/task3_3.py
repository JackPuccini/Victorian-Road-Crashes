import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import os

# input path
INPUT_CSV_PATH = "/course/filtered_vehicle.csv"
# output path
OUTPUT_SCATTER_PATH = "task3_3_scattercolour.png"
# name of CSV file
OUTPUT_CSV_PREFIX = "task3_3_cluster"

OPTIMAL_K = 3


def task3_3():

    print(f"use the best k = {OPTIMAL_K} (setting in the program)")

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

    # 1a. count the number of collision
    crash_counts = df.groupby(grouping_cols).size().reset_index(name="crash_count")

    # 1b. calculate the average statistical data
    mean_stats = df.groupby(grouping_cols)[feature_cols].mean().reset_index()

    # 1c. Merge collision frequency and average statistical data
    combined_data = pd.merge(crash_counts, mean_stats, on=grouping_cols, how="left")

    # 1d. Prepare features for clustering (normalization)
    # use .copy() to avoid SettingWithCopyWarning
    features_for_clustering = combined_data[feature_cols].copy()

    # normalized features (assuming no NaN according to instructions)
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(features_for_clustering)

    print(f"processing K-Means (k={OPTIMAL_K})...")
    kmeans = KMeans(n_clusters=OPTIMAL_K, random_state=42, n_init="auto")
    cluster_labels = kmeans.fit_predict(normalized_features)

    # after adding cluster labels to a round and merging the DataFrame
    combined_data["cluster_label"] = cluster_labels
    print(f"Data points have been assigned to {OPTIMAL_K} clusters.")

    plt.figure(figsize=(14, 9))

    # use matplotlib's scatter fuction，and apply color by the reference 'c'
    # It will automatically map integer labels to the colors in the default color map (such as 'viridis')
    colors = plt.cm.get_cmap("tab10", OPTIMAL_K)

    plt.figure(figsize=(8, 6))
    for i in range(OPTIMAL_K):
        plt.scatter(
            combined_data[combined_data["cluster_label"] == i]["VEHICLE_YEAR_MANUF"],
            combined_data[combined_data["cluster_label"] == i]["crash_count"],
            c=[colors(i)],
            label=f"Cluster {i}",
            alpha=0.6,
        )

    # apply graph
    plt.legend()

    # setting attributs
    plt.title("Crash Count by Vehicle Manufacture Year with Clustering")
    plt.xlabel("Year of Vehicle Manufacture")
    plt.ylabel("Number of Crashes")
    # plt.show()
    plt.grid(True, linestyle="--", alpha=0.6)

    # save graph
    plt.savefig(OUTPUT_SCATTER_PATH)
    print(f"colored scatter graph were saved in {OUTPUT_SCATTER_PATH}")

    # close graph
    plt.close()

    print("generate top 10 crash number CSV file...")
    # define the columns to be included in the CSV output
    # Including combination information (grouping column), summary statistics information (feature column), and collision frequency
    output_cols = grouping_cols + ["crash_count"] + feature_cols

    for i in range(OPTIMAL_K):
        # select the data
        cluster_data = combined_data[combined_data["cluster_label"] == i]

        # sort in desending order by crash count
        top_10 = cluster_data.sort_values(by="crash_count", ascending=False).head(10)

        # choose the number of col needed
        top_10_output = top_10[output_cols]

        # setting output CSV filename
        csv_filename = f"{OUTPUT_CSV_PREFIX}{i}.csv"

        # saved to CSV
        top_10_output.to_csv(csv_filename, index=False, encoding="utf-8")
        print(f"  saved {i} the top 10 rows to {csv_filename}")


task3_3()
