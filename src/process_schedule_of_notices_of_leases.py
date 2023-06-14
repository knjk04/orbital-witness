import logging
import sys

import pandas as pd
import tabula

from schedule_of_notices_of_leases import ScheduleOfNoticesOfLeases


def value_present(s) -> bool:
    return str(s) != "nan"


def read_pdf() -> list[pd.DataFrame]:
    print("\n******************\n")
    # To make this more flexible, this can be passed in as an argument coming from the command line to make it easier
    # to switch files at runtime
    file = "input/Official_Copy_Register.pdf"
    # Without specifying the header option as None, the first row will be treated as a header row
    df_list: list[pd.DataFrame] = tabula.read_pdf(file, pages="all", pandas_options={'header': None})
    print(df_list[8].to_string(index=False))
    return df_list


def process_pdf():
    df_list = read_pdf()
    print("\n******************\n")

    notices_of_leases: [ScheduleOfNoticesOfLeases] = []
    # Start from 2 as this is where the schedule of notices is
    for rows in df_list[2:]:
        logging.debug("Next set of rows:\n")
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

            logging.debug(f"Index: {index}")
            logging.debug(f"Reg date: {reg_date}")
            logging.debug(f"Property desc: {property_desc}")
            logging.debug(f"Lease date: {lease_date}")
            logging.debug(f"Lessee title: {lessee_title}")

            x = 5


# TODO: take list of objects and output JSON
def output_json():
    raise NotImplementedError


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    process_pdf()


if __name__ == "__main__":
    main()
