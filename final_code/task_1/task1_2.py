from task1_1 import task1_1


def task1_2():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    """
    1.0: "Seatbelt Worn"
    2.0: "Vehicle Does Not Have Seatbelt"
    3.0: "Helmet Not Worn"
    4.0: "Child Restraint Used"
    5.0: "Child Restraint Not Used"
    6.0: "Helmet Worn"
    7.0: "Airbag Deployed"
    8.0: "Seatbelt Not Worn"
    9.0: "Airbag Not Deployed"
    """
    person = task1_1()
    # Bar Chart: distribution of seatbelt use (worn (1) vs not worn (8)) across age groups
    # task1_2_age.png
    # Keep only rows where 'HELMET_BELT_WORN' is 1 or 8
    person_hbw18 = person[person["HELMET_BELT_WORN"].isin([1, 8])]
    person_hbw18 = person_hbw18[
        [
            "HELMET_BELT_WORN",
            "AGE_UNDER_16",
            "AGE_17_TO_25",
            "AGE_26_TO_39",
            "AGE_40_TO_64",
            "AGE_OVER_65",
        ]
    ]

    # Plot
    # print(person_hbw18)
    groups = [
        "AGE_UNDER_16",
        "AGE_17_TO_25",
        "AGE_26_TO_39",
        "AGE_40_TO_64",
        "AGE_OVER_65",
    ]
    barchart_dict = {}
    for group in groups:
        worn = person_hbw18[
            (person_hbw18["HELMET_BELT_WORN"] == 1.0) & (person_hbw18[group].notna())
        ]["HELMET_BELT_WORN"].shape[0]
        not_worn = person_hbw18[
            (person_hbw18["HELMET_BELT_WORN"] == 8.0) & (person_hbw18[group].notna())
        ]["HELMET_BELT_WORN"].shape[0]
        barchart_dict[group] = (worn, not_worn)
    print(barchart_dict)

    count_1s = [x[0] for x in barchart_dict.values()]
    count_8s = [x[1] for x in barchart_dict.values()]

    formatting = np.arange(len(groups))
    width = 0.25

    fig1, ax1 = plt.subplots(layout="constrained")
    worn = ax1.bar(formatting - width / 2, count_1s, width, label="Seatbelt Worn")
    not_worn = ax1.bar(
        formatting + width / 2, count_8s, width, label="Seatbelt Not Worn"
    )

    # Labels and title
    ax1.bar_label(worn, padding=3)
    ax1.bar_label(not_worn, padding=3)
    ax1.set_ylabel("Number")
    ax1.set_title("Helmet/Belt Worn Data by Age Group")
    ax1.set_xticks(formatting)
    ax1.set_xticklabels(groups, rotation=45)
    ax1.legend()

    fig1.savefig("task1_2_age.png")

    del (
        person_hbw18,
        groups,
        barchart_dict,
        worn,
        not_worn,
        count_1s,
        count_8s,
        formatting,
        width,
    )
    # Plot of Pie Charts comparing seatbelt use between drivers and passengers
    # task1_2_driver.png
    # Keep only required data
    person_hbw18 = person[person["HELMET_BELT_WORN"].isin([1, 8])]
    person_dripas = person_hbw18[
        [
            "HELMET_BELT_WORN",
            "ROAD_USER_TYPE_DESC_Drivers",
            "ROAD_USER_TYPE_DESC_Passengers",
        ]
    ]

    # Organising data
    pies = ["ROAD_USER_TYPE_DESC_Drivers", "ROAD_USER_TYPE_DESC_Passengers"]
    piechart_dict = {}
    for pie in pies:
        worn = person_dripas[
            ((person_dripas[pie] == True) & person_dripas["HELMET_BELT_WORN"] == 1.0)
        ]["HELMET_BELT_WORN"].shape[0]
        not_worn = person_dripas[
            (person_dripas[pie] == True) & (person_dripas["HELMET_BELT_WORN"] == 8.0)
        ]["HELMET_BELT_WORN"].shape[0]
        piechart_dict[pie] = (worn, not_worn)

    # Pie
    labels = "Seatbelt Worn", "Seatbelt Not Worn"
    sizes_dri = [
        piechart_dict["ROAD_USER_TYPE_DESC_Drivers"][0],
        piechart_dict["ROAD_USER_TYPE_DESC_Drivers"][1],
    ]
    sizes_pas = [
        piechart_dict["ROAD_USER_TYPE_DESC_Passengers"][0],
        piechart_dict["ROAD_USER_TYPE_DESC_Passengers"][1],
    ]

    fig2, ax2 = plt.subplots(1, 2)
    ax2[0].pie(sizes_dri, labels=labels, autopct="%1.2f%%")
    ax2[0].set_title("Seatbelt Use of Drivers")
    ax2[1].pie(
        sizes_pas, labels=labels, autopct="%1.2f%%", colors=["olivedrab", "saddlebrown"]
    )
    ax2[1].set_title("Seatbelt Use of Passengers")

    fig2.savefig("task1_2_driver.png")

    del (
        person_hbw18,
        person_dripas,
        pies,
        piechart_dict,
        worn,
        not_worn,
        labels,
        sizes_dri,
        sizes_pas,
    )
    # Plot of Pie Charts comparing seatbelt use between front/rear passengers (use regex)
    # task1_2_seat.png
    """ Hi, LF, CF, and PL are front passenger positions, and RR, CR, LR, and OR are rear passenger positions """
    # Keep only required data
    person_hbw18 = person[
        (person["HELMET_BELT_WORN"].isin([1, 8]) & person["SEATING_POSITION"].notna())
    ]
    person_frobac = person_hbw18[["HELMET_BELT_WORN", "SEATING_POSITION"]]

    # Organising data
    pies = ["Front_Seat_Passengers", "Back_Seat_Passengers"]
    front_pattern = r"LF|CF|PL"
    back_pattern = r"RR|CR|LR|OR"
    front = person_frobac[person_frobac["SEATING_POSITION"].str.contains(front_pattern)]
    back = person_frobac[person_frobac["SEATING_POSITION"].str.contains(back_pattern)]

    # Pie
    size_fro = [
        front[front["HELMET_BELT_WORN"] == 1.0]["HELMET_BELT_WORN"].shape[0],
        front[front["HELMET_BELT_WORN"] == 8.0]["HELMET_BELT_WORN"].shape[0],
    ]
    size_bac = [
        back[back["HELMET_BELT_WORN"] == 1.0]["HELMET_BELT_WORN"].shape[0],
        back[back["HELMET_BELT_WORN"] == 8.0]["HELMET_BELT_WORN"].shape[0],
    ]
    labels = "Seatbelt Worn", "Seatbelt Not Worn"

    fig3, ax3 = plt.subplots(1, 2)
    ax3[0].pie(size_fro, labels=labels, autopct="%1.2f%%")
    ax3[0].set_title("Seatbelt Use of Front Seat Passengers")
    ax3[1].pie(
        size_bac, labels=labels, autopct="%1.2f%%", colors=["olivedrab", "saddlebrown"]
    )
    ax3[1].set_title("Seatbelt Use of Back Seat Passengers")
    fig3.savefig("task1_2_seat.png")

    del (
        person_hbw18,
        person_frobac,
        pies,
        front_pattern,
        back_pattern,
        front,
        back,
        size_fro,
        size_bac,
        labels,
    )
    # plt.show()
    return


task1_2()
