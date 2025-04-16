def task1_1():
    # DATA PRE-PROCESSING
    import pandas as pd

    person = pd.read_csv("/course/person.csv")

    # Handles missing data in "HELMET_BELT_WORN"
    helmet_belt_mode = person["HELMET_BELT_WORN"].mode()[0]
    person["HELMET_BELT_WORN"] = person["HELMET_BELT_WORN"].fillna(helmet_belt_mode)

    # Converts categorical variables into numerical (one-hot encoding)
    person_OHE = pd.get_dummies(person, columns=["SEX", "ROAD_USER_TYPE_DESC"])

    # Cateforises age groups <16, 17-25, 26-39, 40-64, >65
    # Make a list of max ages per row in 'AGE_GROUPS'
    age_list = [
        int(age) if pd.notna(age) else None
        for age in person_OHE["AGE_GROUP"].str.extract(r"(\d+)(?!.*\d)")[0]
    ]
    # Initialise columns
    person_OHE["AGE_UNDER_16"] = None
    person_OHE["AGE_17_TO_25"] = None
    person_OHE["AGE_26_TO_39"] = None
    person_OHE["AGE_40_TO_64"] = None
    person_OHE["AGE_OVER_65"] = None
    # Fill columns
    for index, age in enumerate(age_list):
        if pd.notna(age):
            if age <= 16:
                person_OHE.loc[index, "AGE_UNDER_16"] = age
            elif age <= 25:
                person_OHE.loc[index, "AGE_17_TO_25"] = age
            elif age <= 39:
                person_OHE.loc[index, "AGE_26_TO_39"] = age
            elif age <= 64:
                person_OHE.loc[index, "AGE_40_TO_64"] = age
            else:
                person_OHE.loc[index, "AGE_OVER_65"] = age

    return person_OHE
