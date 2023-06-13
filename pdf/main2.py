import re

import pandas as pd
import tabula


class ScheduleOfNoticesOfLeases:
    def __init__(self, reg_date: str, property_desc: str, lease_date: str, lessee_title: str, note: str = None):
        self.reg_date = reg_date
        self.property_desc = property_desc
        self.lease_date = lease_date
        self.lessee_title = lessee_title
        self.note = note


def value_present(s) -> bool:
    return str(s) != "nan"


print("\n******************\n")
file = "Official_Copy_Register.pdf"
# Without specifying the header option as None, the first row will be treated as a header row
df_list: list[pd.DataFrame] = tabula.read_pdf(file, pages="all", pandas_options={'header': None})
print(df_list[2].to_string(index=False))

num_rows = len(df_list[2])
print(f"\nNumber of rows: {num_rows}")

print("\n******************\n")

notices_of_leases: [ScheduleOfNoticesOfLeases] = []
# Start from 2 as this is where the schedule of notices is
row_num = 1
for rows in df_list[2:]:
    print("First set of rows:\n")
    print(rows)
    rows.columns = ["index", "reg_date", "property_desc", "lease_date", "lessee_title"]

    default_val = float('-inf')
    index = default_val
    for i in range(len(rows)):
        row = rows.iloc[i]

        if value_present(str(row.loc["index"])):
            if index != default_val:
                # Then index was updated, so this row represents a new entry
                # This only needs to apply for the first time it is set to 1. On subsequent occasions, e.g. ...
                # index = 2.0, this will still work.
                # Save the previous entry
                notices_of_leases.append(ScheduleOfNoticesOfLeases(
                    reg_date=reg_date, property_desc=property_desc, lease_date=lease_date, lessee_title=lessee_title
                ))
            # TODO: stop accessing value from series multiple times
            # start of a new row, so add
            index = row.loc["index"]
            reg_date = row.loc["reg_date"]
            property_desc = row.loc["property_desc"]
            lease_date = row.loc["lease_date"]
            lessee_title = row.loc["lessee_title"]
        else:
            # continuation of row, so append
            reg_date += " " + row.loc["reg_date"] if value_present(row.loc["reg_date"]) else ""
            property_desc += " " + row.loc["property_desc"] if value_present(row.loc["property_desc"]) else ""
            lease_date += " " + row.loc["lease_date"] if value_present(row.loc["lease_date"]) else ""
            lessee_title += " " + row.loc["lessee_title"] if value_present(row.loc["lessee_title"]) else ""

        print(f"Row {row_num} Index: ", index)
        print(f"Row {row_num} Reg date: ", reg_date)
        print(f"Row {row_num} Property desc: ", property_desc)
        print(f"Row {row_num} Lease date: ", lease_date)
        print(f"Row {row_num} Lessee title: ", lessee_title, "\n")
        row_num += 1

        x = 5
