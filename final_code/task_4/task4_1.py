import pandas as pd
import json
import matplotlib.pyplot as plt


def task4_1():
    accident_df = pd.read_csv("/course/accident.csv")
    vehicle_df = pd.read_csv("/course/vehicle.csv")

    # Merge datasets on the accident number and drop rows missing information
    merged_df = accident_df.merge(vehicle_df, on="ACCIDENT_NO")
    merged_df = merged_df.dropna(subset=["VEHICLE_YEAR_MANUF", "ACCIDENT_DATE"])

    # Extract accident year and compute vehicle age at the time of the accident
    merged_df["ACCIDENT_YEAR"] = merged_df["ACCIDENT_DATE"].apply(
        lambda d: int(d.split("-")[0])
    )
    merged_df["VEHICLE_AGE"] = (
        merged_df["ACCIDENT_YEAR"] - merged_df["VEHICLE_YEAR_MANUF"]
    )

    # Classify vehicles as "Old" or "New"
    merged_df["VEHICLE_AGE_GROUP"] = merged_df["VEHICLE_AGE"].apply(
        lambda age: "Old" if age > 10 else "New"
    )

    # Count the number of accidents for each vehicle age group and write to json file
    grouped_age_groups = merged_df["VEHICLE_AGE_GROUP"].value_counts()
    output = {
        "New": int(grouped_age_groups.get("New", 0)),
        "Old": int(grouped_age_groups.get("Old", 0)),
    }
    with open("task4_1_carstat.json", "w") as f:
        json.dump(output, f, indent=4)

    # Group data by accident year and vehicle age group for visualisation
    bar_chart_grouping = merged_df.groupby(
        ["ACCIDENT_YEAR", "VEHICLE_AGE_GROUP"]
    ).size()
    unstacked = bar_chart_grouping.unstack(fill_value=0).sort_index()

    # Create a stacked bar chart and save
    unstacked.plot(kind="bar", stacked=True)
    plt.xlabel("Accident Year")
    plt.ylabel("Number of Accidents")
    plt.title("Vehicle Age Group Distribution per Year")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("task4_1_stackbar.png")


task4_1()
