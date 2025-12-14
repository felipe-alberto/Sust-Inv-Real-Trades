from dataclasses import dataclass
from typing import Optional

@dataclass
class ModelParams:
    Ig: float
    In: float
    Is: float
    K: float
    T: float
    tau: float
    mu_c : float
    mu_d : float
    sigma_c: float
    sigma_d: float
    sigma_cd: float
    Nc: float
    Nd: float


@dataclass
class EquilibriumOutcome:
    NA: float
    NU: float
    NR: float
    NS: float
    PA: float
    PU: float
    PR: float
    PS: float
    xnA: float
    xnU: float
    xgA: float
    xgS: float
    xsR: float

@dataclass
class ModelResults:
    risk_adjusted_welfare: float
    reformed_assets: float
    secondary_trading: float
    market_capitalization: float

