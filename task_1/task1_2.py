import matplotlib.pyplot as plt
import pandas as pd

person_df = pd.read_csv("data/person_adjusted.csv")

# For "HELMET_BELT_WORN" category:
# 1.0: "Seatbelt Worn"
# 2.0: "Vehicle Does Not Have Seatbelt"
# 3.0: "Helmet Not Worn"
# 4.0: "Child Restraint Used"
# 5.0: "Child Restraint Not Used"
# 6.0: "Helmet Worn"
# 7.0: "Airbag Deployed"
# 8.0: "Seatbelt Not Worn"
# 9.0: "Airbag Not Deployed"


def task1_2():

    # Extract rows where "HELMET_BELT_WORN" is either 1 or 8
    filtered = person_df[person_df["HELMET_BELT_WORN"].isin([1, 8])]

    # ------------- Bar Chart ------------- #

    # Count number of 1s and 8s for each age range
    grouped_age_range = (
        filtered.groupby(["AGE_GROUP_ADJUSTED", "HELMET_BELT_WORN"])
        .size()
        .unstack(fill_value=0)
    )

    # Using pandas df.plot() method for generating matplotlib plots
    ax = grouped_age_range.plot(kind="bar", figsize=(10, 6))
    ax.set_title("Seatbelt Usage For Each Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Number of People")

    # Compute total people per age group and proportion worn
    seatbelt_worn = grouped_age_range[1.0]
    seatbelt_total = grouped_age_range[1.0] + grouped_age_range[8.0]
    proportions = (seatbelt_worn / seatbelt_total * 100).round(1)

    # Annotate above each 'worn' bar
    for i, (val, pct) in enumerate(zip(seatbelt_worn, proportions)):
        ax.text(
            i - 0.10, val + 3, f"{pct}%", ha="center", fontsize=9, fontweight="bold"
        )

    # Slight tilt for each x-axis tick label
    plt.xticks(rotation=50)
    ax.legend(["Seatbelt Worn", "Seatbelt Not Worn"])
    # Ensure proportions are natural and save the plot as an image
    plt.tight_layout()
    plt.savefig("task1_2_age.png")

    # ------------- Pie Chart 1 ------------- #

    # Count number of 1s and 8s for each road user type
    grouped_user_type = (
        filtered.groupby(["ROAD_USER_TYPE_DESC", "HELMET_BELT_WORN"])
        .size()
        .unstack(fill_value=0)
    )

    # Remove irrelevant user types
    grouped_user_type = grouped_user_type.loc[["Drivers", "Passengers"]]

    # Extract the counts
    labels = ["Seatbelt Worn", "Seatbelt Not Worn"]

    drivers_counts = [
        grouped_user_type.loc["Drivers", 1.0],
        grouped_user_type.loc["Drivers", 8.0],
    ]
    passengers_counts = [
        grouped_user_type.loc["Passengers", 1.0],
        grouped_user_type.loc["Passengers", 8.0],
    ]

    # Plot side by side pie charts
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].pie(drivers_counts, labels=labels, autopct="%1.1f%%", startangle=90)
    axes[0].set_title("Drivers")

    axes[1].pie(passengers_counts, labels=labels, autopct="%1.1f%%", startangle=90)
    axes[1].set_title("Passengers")

    plt.suptitle("Seatbelt Use Comparison: Drivers vs Passengers", y=1.02)
    plt.tight_layout()
    plt.savefig("task1_2_driver.png", bbox_inches="tight")

    # ------------- Pie Chart 2 ------------- #

    # LF, CF, and PL are front passenger positions, and RR, CR, LR, and OR are rear passenger positions.

    # Count number of 1s and 8s for each road user type
    grouped_user_type = (
        filtered.groupby(
            ["ROAD_USER_TYPE_DESC", "HELMET_BELT_WORN", "SEATING_POSITION"]
        )
        .size()
        .unstack(fill_value=0)
        .loc["Passengers"]
    )

    # Sum over columns for front and rear seats
    df_grouped = pd.DataFrame(
        {
            "Front": grouped_user_type[["CF", "LF", "PL"]].sum(axis=1),
            "Rear": grouped_user_type[["CR", "LR", "OR", "RR"]].sum(axis=1),
        }
    )

    backseat_counts = [
        df_grouped.loc[1.0]["Rear"],
        df_grouped.loc[8.0]["Rear"],
    ]

    frontseat_counts = [
        df_grouped.loc[1.0]["Front"],
        df_grouped.loc[8.0]["Front"],
    ]

    # Plot side by side pie charts
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Prepare the labels
    labels = ["Seatbelt Worn", "Seatbelt Not Worn"]

    axes[0].pie(backseat_counts, labels=labels, autopct="%1.1f%%", startangle=90)
    axes[0].set_title("Back-seat Passengers")

    axes[1].pie(frontseat_counts, labels=labels, autopct="%1.1f%%", startangle=90)
    axes[1].set_title("Front-seat Passengers")

    plt.suptitle("Seatbelt Use Comparison: Front-seat vs Back-seat Passengers", y=1.02)
    plt.tight_layout()
    plt.savefig("task1_2_seat.png", bbox_inches="tight")


task1_2()
