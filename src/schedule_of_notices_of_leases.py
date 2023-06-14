# While not stated as required, I have added the index in to serve as a unique key to make it easier to match  which
# entry in the register document corresponds to which ScheduleOfNoticesOfLeases object
class ScheduleOfNoticesOfLeases:
    def __init__(self, index: float, reg_date: str, property_desc: str, lease_date: str, lessee_title: str,
                 note: str = None):
        """
        :param index: the index of the entry in the register document
        it is represented on the Title Plan
        :param reg_date: date the sub lease was registered with the Land Registry and a qualitative description of how
        it is represented on the Title Plan
        :param property_desc: the address of the sub lease property (type: str)
        :param lease_date: The date the lease was executed and the duration of the lease from that date (type: str)
        :param lessee_title: unique identifier for the sub lease property (type: str)
        :param note: This is None because this is an optional field
        """
        self.index = int(index)
        self.reg_date = reg_date
        self.property_desc = property_desc
        self.lease_date = lease_date
        self.lessee_title = lessee_title
        self.note = note
