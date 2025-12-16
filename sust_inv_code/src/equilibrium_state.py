# src/equilibrium_state.py
from dataclasses import dataclass
from typing import Dict, Set
from .types import FirmType, InvestorType

@dataclass
class EquilibriumAllocationOnly:
    # Firm and Investor Outcomes
    N: Dict[FirmType, float]        # number of firms of each type N[f]
    P: Dict[FirmType, float]        # share prices P[f]
    X: Dict[InvestorType, Dict[FirmType, float]] # Investor positions: X[i][f]
    # Regime Information
    active_firms: Set[FirmType]
    active_links: Dict[InvestorType, Set[FirmType]]
    regime: str

@dataclass
class EquilibriumAllocationTransformation:
    # Firm and Investor Outcomes
    N: Dict[FirmType, float]        # number of firms of each type N[f]
    P: Dict[FirmType, float]        # share prices P[f]
    X: Dict[InvestorType, Dict[FirmType, float]] # Investor positions: X[i][f]
    pi : float                      # reform action clearing price
    # Regime Information
    active_firms: Set[FirmType]
    active_links: Dict[InvestorType, Set[FirmType]]
    regime: str
