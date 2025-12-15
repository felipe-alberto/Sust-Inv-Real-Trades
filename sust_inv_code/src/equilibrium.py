# Equilibrium Computation
# Project: Sustainable Investing Strategies For Real Asset Trades: Incentives to Own and Transform Pollutive Assets
# Author: Felipe Verastegui, PhD IEOR Columbia University
# Last Update: December 2025

# ----- Imports ---------------------------------------------------------------

from sust_inv_code.src.data_structures import ModelParams, EquilibriumOutcome

# ----- Subfunctions ---------------------------------------------------------

PrintBool = True

def alloc_only_corporate_choices(params: ModelParams):
    
    # Unpacking Parameters
    Ig, In, Is = params.Ig, params.In, params.Is
    K, T = params.K, params.T
    tau = params.tau
    sigma_c, sigma_d, sigma_cd = params.sigma_c, params.sigma_d, params.sigma_cd
    Nc, Nd = params.Nc, params.Nd

    # Base Calculations
    phi = (sigma_c**2) * (sigma_d**2) - (sigma_cd**2)  # Cov Matrix Det
    I = Ig + In + Is                                   # Investor Population 

    # Formulas for Optimal Corporate Choices in Market for Allocation Only
    KerNU = ((Nd + Is * K * (tau / (sigma_d**2)) - (sigma_cd/sigma_d**2) * Nc * (Is / (Ig+In)))
    + Ig * T * (tau / sigma_d**2) * ((Is * sigma_cd**2 + (Ig + In) * sigma_c**2 * sigma_d **2)/((Ig + In) * phi)))
    CoreNU = (In / I) * (KerNU)
    NU = max(0, CoreNU) 
    KerNS = ((Nd + Is * K * (tau / (sigma_d**2)) - (sigma_cd/sigma_d**2) * Nc * (Is / (Ig+In)))
    + Ig * T * (tau / sigma_d**2) * ((Ig * Is * sigma_cd**2 - (Ig + In) * (Is + In)* sigma_c**2 * sigma_d **2)/(Ig*(Ig + In) * phi)))
    CoreNS = (Ig / I) * (KerNS)
    NS = max(0, CoreNS)
    KerNR = (Nd - (Ig + In) * K * (tau / (sigma_d**2)) + (Ig) * T * (tau / (sigma_d**2)) + (sigma_cd / (sigma_d**2))*Nc)
    CoreNR = (Is / I) * (KerNR)
    NR = max(0, CoreNR)
    NA = Nc

    # Print Debug
    if PrintBool:
        print("Allocation-Only: d-Firms")
        print("Unreformed Firms: " + str(NU))
        print("Secondary Trading Firms: " + str(NS))
        print("Reformed Firms: " + str(NR))
        print("Acceptable Firms: " + str(NA))
    return NA, NU, NR, NS

def alloc_only_share_prices(params: ModelParams):

    # Unpacking Parameters
    Ig, In, Is = params.Ig, params.In, params.Is
    K, T = params.K, params.T
    tau = params.tau
    mu_c , mu_d = params.mu_c, params.mu_d
    sigma_c, sigma_d, sigma_cd = params.sigma_c, params.sigma_d, params.sigma_cd
    Nc, Nd = params.Nc, params.Nd

    I, Ign = Ig + In + Is, Ig + In        # Investor Population Groups

    # Formulas for Firm Share Prices in Market for Allocation Only
    PA = ( mu_c - 
        (Nc*sigma_c**2 + Nd*sigma_cd)/(I*tau) 
        - (Is/(Ign*I)) * (Nc/tau) * (sigma_c**2 - sigma_cd**2/sigma_d**2)
        + (Is/I) * (sigma_cd/sigma_d**2) * (-K + (Ig/Ign)*T))
    PU = mu_d  - (1/I)* (Is*K + Ig * T  + Nd*(sigma_d**2)/tau +Nc * (sigma_cd/tau))
    PS = mu_d - (1/I)*(Is * (K - T)   - In * T  +  Nd * (sigma_d**2)/tau    + Nc  * (sigma_cd/tau))
    PR = mu_d - (1/I)*( - Ig * (K-T)   - In * K  +  Nd * (sigma_d**2)/tau + Nc * (sigma_cd/tau) )
    if PrintBool:
        print("Allocation-Only: Share Prices")
        print("Share Price Unreformed Firms: " + str(PU))
        print("Share Price Secondary Trading Firms: " + str(PS))
        print("Share Price Reformed Firms: " + str(PR))
        print("Share Price Acceptable Firms: " + str(PR))
    print(PR)
    print(PU)
    print(PR - PU)
    print(K)
    return PA, PU, PR, PS

def alloc_only_investor_positions(params: ModelParams):
    # Unpacking Parameters
    tau = params.tau
    mu_c , mu_d = params.mu_c, params.mu_d
    sigma_c, sigma_d, sigma_cd = params.sigma_c, params.sigma_d, params.sigma_cd
    phi = (sigma_c**2) * (sigma_d**2) - (sigma_cd**2)  # Cov Matrix Det
    PA, PU, PR, PS = alloc_only_share_prices(params)    # Using Share Prices from Above | FIX

    xnA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PU) * sigma_cd)
    xnU = (tau / phi) * ((mu_d - PU) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xgA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PS) * sigma_cd)
    xgS = (tau / phi) * ((mu_d - PS) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xsR = (tau / (sigma_d**2)) * (mu_d - PR)

    return xnA, xnU, xgA, xgS, xsR

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

    # 1. Compute optimal corporate choices
    NA, NU, NR, NS = alloc_only_corporate_choices(params)
    # 2. Compute share prices
    PA, PU, PR, PS = alloc_only_share_prices(params)
    # 3. Compute investor positions 
    xnA, xnU, xgA, xgS, xsR = alloc_only_investor_positions(params)
    # N. Construct equilibrium object
    return EquilibriumOutcome(
        NA = NA,
        NU = NU,
        NR = NR,
        NS = NS,
        PA = PA,
        PU = PU,
        PR = PR,
        PS = PS,
        xnA = xnA,
        xnU = xnU,
        xgA = xgA,
        xgS = xgS,
        xsR = xsR
    )

