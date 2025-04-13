import pandas as pd
import json


def task4_3():
    vehicle_df = pd.read_csv("data/vehicle.csv")

    # 1. Top 5 Most Diverse Manufacturers
    # ------------------------------------

    # Count number of unique vehicle types per make
    grouped = vehicle_df.groupby("VEHICLE_MAKE")["VEHICLE_TYPE_DESC"].nunique()

    # Get top 5 manufacturers by diversity
    top5 = grouped.sort_values(ascending=False).head(5)
    top5_names = top5.index.tolist()

    # Prepare JSON output and write to file
    task4_3_1_output = {"Manufacturers": top5_names}
    for manufacturer, count in top5.items():
        task4_3_1_output[manufacturer] = int(count)

    with open("task4_3_diversity.json", "w") as f:
        json.dump(task4_3_1_output, f, indent=4)

    # 2. Most Common Vehicle Types + Probabilities
    # --------------------------------------------

    # Note: Here, the probability for each vehicle type is calculated using the total number of
    # accidents for that particular manufacturer (i.e., within the manufacturer), which is one acceptable
    # interpretation of the specification as per the Ed Discussion post #111

    task4_3_2_output = {}

    for manufacturer in top5_names:
        subset = vehicle_df[vehicle_df["VEHICLE_MAKE"] == manufacturer]
        type_counts = subset["VEHICLE_TYPE_DESC"].value_counts().head(3)

        # Use the total number of accidents for the manufacturer as the denominator.
        manufacturer_total = len(subset)

        type_info = []
        for vehicle_type, count in type_counts.items():
            probability = round(count / manufacturer_total, 2)
            type_info.append({"Vehicle Type": vehicle_type, "Probability": probability})

        task4_3_2_output[manufacturer] = type_info

    with open("task4_3_probabilities.json", "w") as f:
        json.dump(task4_3_2_output, f, indent=4)


task4_3()
