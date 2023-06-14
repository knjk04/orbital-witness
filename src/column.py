# Using enum for the column names to avoid typos as they are used multiple times throughout
from enum import Enum


class Column(Enum):
    INDEX = "index"
    REG_DATE = "reg_date"
    PROPERTY_DESC = "property_desc"
    LEASE_DATE = "lease_date"
    LESSEE_TITLE = "lessee_title"
