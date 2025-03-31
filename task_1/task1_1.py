import pandas as pd

person_df = pd.read_csv("data/person.csv")

# Fill the nan cells with the column's mode
mode = person_df["HELMET_BELT_WORN"].mode().iloc[0]
person_df["HELMET_BELT_WORN"] = person_df["HELMET_BELT_WORN"].fillna(value=mode)

# Create a new, one-hot encoded column for each unique value in the "SEX" column
for value in person_df["SEX"].unique():
    # Ignore 'nan' values (type float in pandas)
    if isinstance(value, float):
        continue

    # Naming convention for one-hot encoded columns is uppercase and "_" characters
    new_column_name = "SEX_" + (value.replace(" ", "_")).upper()
    person_df[new_column_name] = (person_df["SEX"] == value).astype(int)

# Likewise, create corresponding one-hot encoded columns for the "ROAD_USER_TYPE_DESC" columns
for value in person_df["ROAD_USER_TYPE_DESC"].unique():
    new_column_name = "ROAD_USER_TYPE_DESC_" + (value.replace(" ", "_")).upper()
    person_df[new_column_name] = (person_df["ROAD_USER_TYPE_DESC"] == value).astype(int)


# Use a manually constructed dictionary to map age ranges to the newly adjusted/broad ranges
age_conversion_dict = {
    "0-4": "Under 16",
    "5-12": "Under 16",
    "13-15": "Under 16",
    "16-17": "17-25",
    "18-21": "17-25",
    "22-25": "17-25",
    "26-29": "26-39",
    "30-39": "26-39",
    "40-49": "40-64",
    "50-59": "40-64",
    "60-64": "40-64",
    "65-69": "65+",
    "70+": "65+",
    "Unknown": "Unknown",
}

person_df["AGE_GROUP_ADJUSTED"] = person_df["AGE_GROUP"].map(age_conversion_dict)
