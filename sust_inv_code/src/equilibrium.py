# Equilibrium Computation
# Project: Sustainable Investing Strategies For Real Asset Trades: Incentives to Own and Transform Pollutive Assets
# Author: Felipe Verastegui, PhD IEOR Columbia University
# Last Update: December 2025

# ----- Imports ---------------------------------------------------------------

from sust_inv_code.src.data_structures import ModelParams, EquilibriumOutcome

# ----- Subfunctions ---------------------------------------------------------

def alloc_only_corporate_choices(params: ModelParams):
    
    Ig, In, Is = params.Ig, params.In, params.Is
    K, T = params.K, params.T
    tau = params.tau
    sigma_c, sigma_d, sigma_cd = params.sigma_c, params.sigma_d, params.sigma_cd
    Nc, Nd = params.Nc, params.Nd

    phi = (sigma_c**2) * (sigma_d**2) - (sigma_cd**2)  # Determinant of cov matrix
    I = Ig + In + Is

    print(Ig, In, Is, K, T, tau, sigma_c, sigma_d, sigma_cd, Nc, Nd, I, phi)
    f = (Is / (Ig + In))*(Ig * T * sigma_cd * (tau / phi) - Nc)
    KerNU = (Nd + Is * K * (tau / (sigma_d**2)) + Ig * T * (tau * (sigma_c**2) / phi) + (sigma_cd / (sigma_d**2))*f)
    CoreNU = (In / I) * (KerNU)
    NU = max(0, CoreNU) 
    KerNS = (Nd + Is * K * (tau / (sigma_d**2)) - (Is + In) * T * (tau * (sigma_c**2) / phi) - (sigma_cd / (sigma_d**2))*f)
    CoreNS = (Ig / I) * (KerNS)
    NS = max(0, CoreNS)
    KerNR = (Nd - (Ig + In) * K * (tau / (sigma_d**2)) + (Ig) * T * (tau / (sigma_d**2)) + (sigma_cd / (sigma_d**2))*Nc)
    CoreNR = (Is / I) * (KerNR)
    NR = max(0, CoreNR)
    NA = Nc
    print("Allocation-Only: d-Firms")
    print("Unreformed Firms: " + str(NU))
    print("Secondary Trading Firms: " + str(NS))
    print("Reformed Firms: " + str(NR))
    print("Acceptable Firms: " + str(NA))
    return NA, NU, NR, NS

def alloc_only_share_prices(params: ModelParams, pi: float):
    NU, coreNU = ...
    NUp, coreNUp = ...
    NR, coreNR = ...
    return NU, NUp, NR, coreNU, coreNUp, coreNR

def alloc_only_investor_positions(params: ModelParams, pi: float):
    NU, coreNU = ...
    NUp, coreNUp = ...
    NR, coreNR = ...
    return NU, NUp, NR, coreNU, coreNUp, coreNR

def reform_exchange_compute_pi(params: ModelParams) -> float:
    # compute α, β, φ
    # compute π*
    pi = 0
    return pi 

def reform_exchange_corporate_choices(params: ModelParams) -> float:
    # compute α, β, φ
    # compute π*
    pi = 0
    return pi

def reform_exchange_share_prices(params: ModelParams) -> float:
    # compute α, β, φ
    # compute π*
    pi = 0
    return pi


def reform_exchange_investor_positions(params: ModelParams) -> float:
    # compute α, β, φ
    # compute π*
    pi = 0
    return pi

# ----- Main solver ---------------------------------------------------------

def solve_equilibrium(params: ModelParams) -> EquilibriumOutcome:
    """
    Computes the equilibrium allocations and prices.
    """

    # 1. Compute optimal corporate choices
    NA, NU, NR, NS = alloc_only_corporate_choices(params)

    # 5. Construct equilibrium object
    return EquilibriumOutcome(
        NA = NA,
        NU = NU,
        NR = NR,
        NS = NS,
    )

