from dataclasses import dataclass
from typing import Optional
from sust_inv_code.src.types import FirmType, InvestorType

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
    @property
    def I(self) -> float:
        return self.Ig + self.In + self.Is
    @property
    def phi(self) -> float:
        return self.sigma_c**2 * self.sigma_d**2 - self.sigma_cd**2
    @property
    def psi(self) -> float:
        return self.sigma_c**2 - 2 * self.sigma_cd + self.sigma_d**2 

@dataclass
class ModelResults:
    risk_adjusted_welfare: float
    reformed_assets: float
    secondary_trading: float
    market_capitalization: float

