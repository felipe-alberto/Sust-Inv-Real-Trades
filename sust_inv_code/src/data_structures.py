from enum import Enum
from typing import Optional
from typing import Dict, Set
from dataclasses import dataclass

class FirmType(str, Enum):
    A = "A"        
    Aprime = "A'"  
    U = "U"        
    R = "R"        
    S = "S"        
    Uprime = "U'"  

class InvestorType(str, Enum):
    g = "g"        
    n = "n"        
    s = "s"        

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
class EquilibriumAllocationOnly:
    N: Dict[FirmType, float]        
    P: Dict[FirmType, float]        
    X: Dict[InvestorType, Dict[FirmType, float]] 
    active_firms: Set[FirmType]
    active_links: Dict[InvestorType, Set[FirmType]]
    regime: str

@dataclass
class EquilibriumAllocationTransformation:
    N: Dict[FirmType, float]        
    P: Dict[FirmType, float]        
    X: Dict[InvestorType, Dict[FirmType, float]] 
    pi : float                      
    active_firms: Set[FirmType]
    active_links: Dict[InvestorType, Set[FirmType]]
    regime: str

@dataclass
class ModelResults:
    total_surplus: float
    firm_surplus: float
    investor_surplus: float
    risk_adjusted_return: float
    reformed_assets: float
    secondary_trading: float
    market_capitalization: float
    firm_market_cap: Dict[FirmType, float]
    firm_net_value: Dict[FirmType, float]
    investor_risk_adjusted: Dict[InvestorType, float]
    investor_transfers: Dict[InvestorType, float]
    net_market_cap: float
    firm_surplus_dict: Optional[Dict[FirmType, float]] = None
    investor_surplus_dict: Optional[Dict[InvestorType, float]] = None
    clean_market_cap: Optional[float] = None
    dirty_market_cap: Optional[float] = None