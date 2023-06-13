import re

import pandas as pd
import tabula


def get_position_of_date(s: str) -> (int, int):
    return re.search(r"\d\d\.\d\d\.\d\d\d\d", s).span()


class ScheduleOfNoticesOfLeases:
    def __init__(self, reg_date: str, property_desc: str, lease_date: str, lessee_title: str, note: str = None):
        self.reg_date = reg_date
        self.property_desc = property_desc
        self.lease_date = lease_date
        self.lessee_title = lessee_title
        self.note = note


print("\n******************\n")
file = "Official_Copy_Register.pdf"
# Without specifying the header option as None, the first row will be treated as a header row
df = tabula.read_pdf(file, pages="all", pandas_options={'header': None})
print(df[2].to_string(index=False))

num_rows = len(df[2])
print(f"\nNumber of rows: {num_rows}")

print("\n******************\n")

# Read a row of a dataframe
print("\nFirst row:\n")
df2 = df[2]
df2.columns = ["index", "reg_date", "property_desc", "lease_date", "lessee_title"]
row = df2.iloc[0]
print("Index: ", row.loc["index"])
print("Reg date: ", row.loc["reg_date"])
print("Property desc: ", row.loc["property_desc"])
print("Lease date: ", row.loc["lease_date"])
print("Lessee title: ", row.loc["lessee_title"])



MANUAL_SPLIT = False
if MANUAL_SPLIT:
    print("\n******************\n")
    for line in df[2].to_string(index=False).split("\n"):
        print(f"\nLine: {line}")
        split = line.split("  ")
        split = list(filter(None, split))  # remove empty strings
        index, reg_date, lease_date = split

        index = index.lstrip()
        reg_date = reg_date.lstrip()
        lease_date = lease_date.lstrip()

        # Extract the property description from the registration date
        # RegEx used instead of split() because only space separates the two columns, but the
        # property description field itself may contain spaces
        _, reg_date_end_idx = get_position_of_date(reg_date)
        property_desc = reg_date[reg_date_end_idx:].lstrip()
        # remove property description from reg date
        reg_date = reg_date[:reg_date_end_idx]

        # extract lessee title from lease date
        _, lessee_title_start_pos = get_position_of_date(lease_date)
        lessee_title = lease_date[lessee_title_start_pos:].lstrip()
        # remove lessee title from date of lease
        lease_date = lease_date[:lessee_title_start_pos]

        x=3  # TODO: remove
        # index, reg_date, property_desc, date_of_lease, lessee_title = line.split("  ")
        print(f"Index: {index}")
        print(f"Reg date: {reg_date}")
        print(f"Property description: {property_desc}")
        print(f"Date of lease: {lease_date}")
        print(f"Lessee title: {lessee_title}")
        schedule = ScheduleOfNoticesOfLeases(
            reg_date=reg_date, property_desc=property_desc, lease_date=lease_date, lessee_title=lessee_title
        )
        x=4  # TODO: remove


