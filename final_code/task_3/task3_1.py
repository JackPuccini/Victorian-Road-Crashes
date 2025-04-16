import pandas as pd
import matplotlib.pyplot as plt
import os

# setting input path
INPUT_CSV_PATH = "/course/filtered_vehicle.csv"
# setting output path
OUTPUT_PLOT_PATH = "task3_1_scatter.png"


def task3_1():

    df = pd.read_csv(INPUT_CSV_PATH, encoding="utf-8")

    # setting the three unique combination
    grouping_cols = ["VEHICLE_YEAR_MANUF", "VEHICLE_BODY_STYLE", "VEHICLE_MAKE"]

    # count the number of crashes occurring for each unique three combination.
    crash_counts = df.groupby(grouping_cols).size().reset_index(name="crash_count")

    # adjust the windows of graph
    plt.figure(figsize=(12, 8))

    # creat scatter graph set x-axis as Year of Vehicle Manufacture and y-axis as Number of crashes.
    plt.scatter(
        crash_counts["VEHICLE_YEAR_MANUF"],
        crash_counts["crash_count"],
        alpha=0.6,  # add some transparency
        s=10,  # adjust the point size if needed
    )

    # label the graph's x-axis, y-axis and title
    plt.xlabel("Year of Vehicle Manufacture")
    plt.ylabel("Number of crashes")
    plt.title("Number of crashes vs. Year of Vehicle Manufacture")
    plt.grid(True, linestyle="--", alpha=0.6)  # apply grid for better reading

    # save graph
    plt.savefig(OUTPUT_PLOT_PATH)
    print(f"scatter graph were saved in {OUTPUT_PLOT_PATH}")

    # close graph to release memories
    plt.close()


task3_1()
