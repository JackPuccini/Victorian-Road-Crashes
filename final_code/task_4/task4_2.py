import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def task4_2():
    accident_df = pd.read_csv("/course/accident.csv")
    vehicle_df = pd.read_csv("/course/vehicle.csv")

    # Merge datasets on the accident number
    merged_df = accident_df.merge(vehicle_df, on="ACCIDENT_NO")

    # Group by road geometry and surface type
    grouped = merged_df.groupby(["ROAD_GEOMETRY_DESC", "ROAD_SURFACE_TYPE_DESC"]).size()
    heatmap_data = grouped.unstack(fill_value=0)

    # Create a heatmap and save
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu")
    plt.title("Accident Counts by Road Geometry and Surface Type")
    plt.xlabel("Road Surface Type")
    plt.ylabel("Road Geometry")
    plt.tight_layout()
    plt.savefig("task4_2_heatmap.png")


task4_2()
