import csv
import json

import requests

DRUG_PROGRAM = (
    "LEKI W PROGRAMIE LEKOWYM - LECZENIE CHORYCH NA CZERNIAKA SKÓRY LUB BŁON ŚLUZOWYCH"
)

provinces = {
    "01": "dolnośląskie",
    "02": "kujawsko-pomorskie",
    "03": "lubelskie",
    "04": "lubuskie",
    "05": "łódzkie",
    "06": "małopolskie",
    "07": "mazowieckie",
    "08": "opolskie",
    "09": "podkarpackie",
    "10": "podlaskie",
    "11": "pomorskie",
    "12": "śląskie",
    "13": "świętokrzyskie",
    "14": "warmińsko-mazurskie",
    "15": "wielkopolskie",
    "16": "zachodniopomorskie",
}

genders = {
    "F": "Kobieta",
    "M": "Mężczyzna",
    "N": "Nieznana",
}

age_groups = {
    "1": "poniżej 1",
    "2": "1 - 6",
    "3": "7 - 18",
    "4": "19 - 40",
    "5": "41 - 60",
    "6": "61 - 80",
    "7": "81 i więcej",
    "8": "wiek nieustalony",
}

output_file = "drug_costs_czerniak.csv"

fieldnames = [
    "active_substance_code",
    "active_substance_name",
    "province",
    "gender",
    "age_group",
    "number_of_patients",
    "refund",
]

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for province_code in provinces:
        for gender_code in genders:
            for age_code in age_groups:
                page = 1
                while True:
                    url = (
                        f"https://api.nfz.gov.pl/app-stat-api-pl/drug-costs-by-active-substance?"
                        f"drugProgram={DRUG_PROGRAM}&"
                        f"province={province_code}&"
                        f"gender={gender_code}&"
                        f"ageGroup={age_code}&"
                        f"page={page}&"
                        f"limit=10&"
                        f"format=json"
                    )
                    response = requests.get(url)
                    data = response.json()

                    actual_data_array = data.get("data", {}).get("data", [])

                    if not actual_data_array:
                        print("Actual data array is empty, skipping")
                    else:
                        print(
                            "Proceeding to write ", len(actual_data_array), " entries"
                        )

                    for entry in actual_data_array:
                        writer.writerow(
                            {
                                "active_substance_code": entry.get(
                                    "active-substance-code"
                                ),
                                "active_substance_name": entry.get(
                                    "active-substance-name"
                                ),
                                "province": provinces[province_code],
                                "gender": genders[gender_code],
                                "age_group": age_groups[age_code],
                                "number_of_patients": entry.get("number-of-patients"),
                                "refund": entry.get("refund"),
                            }
                        )

                    if data.get("links", {}).get("next", []):
                        page += 1
                    else:
                        break

print(f"✅ Data saved to {output_file}")
