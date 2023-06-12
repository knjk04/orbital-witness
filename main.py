import json
import logging
import sys


# 1. Registration date and plan ref: This is the date at which the sub lease was registered with the Land Registry and a qualitative description of how it is represented on the Title Plan (a separate document)
# 2. Property description: Typically the address of the sub lease property
# 3. Date of lease and term: The date the lease was executed and the duration of the lease from that date
# 4. Lessee’s title: The unique identifier for the sub lease property
# 5. (Optional) notes

def read_input():
    with open('sample.json', 'r') as file:
        json_data = json.load(file)[0]
        # print(json.dumps(json_data, indent=4))
        # print(json.dumps(json_data['leaseschedule']['scheduleEntry'], indent=4))
        return json_data


def main():
    json_data = read_input()
    # print('\n*********\n')

    # TODO: inline read_input
    for entries in json_data['leaseschedule']['scheduleEntry']:
        reg_date = ''
        property_desc = ''
        lease_date = ''
        lessee_title = ''
        note = ''

        for entry_text in entries['entryText']:
            print(entry_text)
            # split on at 2 spaces (1 space is insufficient)
            split = entry_text.split("  ")
            # remove empty strings
            split = list(filter(None, split))
            print('Split: ', split)

            if len(split) >= 1:
                if is_note(split[0]):
                    # TODO: handle multiple notes by splitting them with a character
                    note += split[0]
                else:
                    reg_date += ' ' + split[0]
            print('  -> Reg date:', reg_date)

            if len(split) >= 2:
                property_desc = split[1]
            print('  -> Property description:', property_desc)

            if len(split) >= 3:
                lease_date = split[2]
            print('  -> Lease date:', lease_date)

            if len(split) >= 4:
                lessee_title = split[3]
            print('  -> Lessee title:', lessee_title)

        print('  -> Note:', note)

        print('\n')
        # TODO: output JSON


def is_date(s: str) -> bool:
    import datetime
    try:
        day, month, year = s.split(".")
    except ValueError:
        logging.debug("Not enough values to unpack: " + s)
        # not enough values to unpack
        return False

    try:
        datetime.datetime(year=int(year), month=int(month), day=int(day))
        return True
    except ValueError:
        return False


def is_note(s: str) -> bool:
    # assumes we are interested in all notes
    return s.startswith("NOTE")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    main()


