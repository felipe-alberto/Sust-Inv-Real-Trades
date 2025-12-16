# src/types.py
from enum import Enum

class FirmType(str, Enum):
    A = "A"        # acceptable / clean
    Aprime = "A'"  # reform right clean (buyer)
    U = "U"        # unreformed dirty
    R = "R"        # reformed dirty
    S = "S"        # secondary traded dirty
    Uprime = "U'"  # reform right dirty (seller)

class InvestorType(str, Enum):
    g = "g"        # green
    n = "n"        # neutral
    s = "s"        # secondary
