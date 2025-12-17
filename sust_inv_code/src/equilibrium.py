# Equilibrium Computation
# Project: Sustainable Investing Strategies For Real Asset Trades: Incentives to Own and Transform Pollutive Assets
# Author: Felipe Verastegui, PhD IEOR Columbia University
# Last Update: December 2025

# ----- Imports ---------------------------------------------------------------

from sust_inv_code.src.data_structures import ModelParams, EqmAllocationOnly, EqmCornerObTrading

# ----- Subfunctions ---------------------------------------------------------

PrintBool = False

def alloc_only_corporate_choices(params: ModelParams):
    
    # Params
    Ig, In, Is = params.Ig, params.In, params.Is
    K, T = params.K, params.T
    tau = params.tau
    sigma_c, sigma_d, sigma_cd = params.sigma_c, params.sigma_d, params.sigma_cd
    Nc, Nd = params.Nc, params.Nd

    # Key Values
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
    p = params
    # Unpacking Parameters
    Nc, Nd = p.Nc, p.Nd
    I, Ig, In, Is = p.I, p.Ig, p.In, p.Is
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    K, T = p.K, p.T
    Ign = Ig + In       
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
    # Unpacking Parameters
    Ig, In, Is = params.Ig, params.In, params.Is
    K, T = params.K, params.T
    tau = params.tau
    sigma_c, sigma_d, sigma_cd = params.sigma_c, params.sigma_d, params.sigma_cd
    Nc, Nd = params.Nc, params.Nd
    # compute π*
    pi_op = - K + (Is *Nc - (Ig + In)* Nd) * (sigma_c**2 * sigma_d**2) / (
    Is * (Ig + In) * (sigma_c**2 + sigma_d**2) * tau)                               # Hardcode sigma_cd = 0
    pi_ob = (((Is * Nc - Ig * Nd)*(sigma_c**2 * sigma_d**2) - Is * K *(Ig * sigma_c**2 + (Ig + In)* sigma_d**2) * tau)/
                ((Ig*(Is + In) * sigma_c**2 + Is * (Ig + In)* sigma_d**2)*tau))         # Hardcode sigma_cd = 0
    if PrintBool:
        print("Option-Price Threshold")
        print(pi_op)
        print("Obligation-Price Threshold")
        print(pi_ob)
        print(pi_ob <0)
        if pi_ob < 0 or pi_op > 0:
            print("FLAG")
            if pi_ob >= - T:
                print("(Interior) Obligations Trading Instance Detected")
            else:
                print("(Corner) Obligations Trading Instance Detected")
            if pi_op > 0:
                print("Options Trading Instance Detected")
        else:
            print("Undiagnosed Instance Detected")
    return pi_op, pi_ob 

def corner_ob_trading_corporate_choices(params: ModelParams) -> float:
    # Unpacking Parameters
    Ig, In, Is = params.Ig, params.In, params.Is
    K, T = params.K, params.T
    tau = params.tau
    sigma_c, sigma_d, sigma_cd = params.sigma_c, params.sigma_d, params.sigma_cd
    Nc, Nd = params.Nc, params.Nd
    phi = (sigma_c**2) * (sigma_d**2) - (sigma_cd**2)  # Cov Matrix Det
    I = Ig + In + Is                                   # Investor Population
    # Formulas for Optimal Corporate Choices in Corner Obligations Trading
    NR = (Is / I) * (
        Nd - K * (Ig + In) * (tau / phi) * sigma_c**2 + T* Ig * (tau / phi) * sigma_c**2)
    NG = (Ig / I) * (
        Nd + (K - T) * Is * (tau / phi) * sigma_c**2 - T * In * (tau / phi) * sigma_c**2)
    NAprime = (Is / I) * (
        Nc - (K - T) * Ig * (tau / phi) * sigma_d**2 - K * In * (tau / phi) * sigma_d**2 + T * In * (tau / phi) * sigma_d**2)
    NUprime = NAprime
    NS = NG - NUprime
    NA = Nc - NAprime
    NU = Nd - NR - NG
    if PrintBool:
        print("Obligations-Trading (Corner): d-Firms")
        print("Reformed Firms: " + str(NR))
        print("Green Firms: " + str(NG))
        print("Indirectly-Reformed Firms: " + str(NUprime))
        print("Secondary Trading Firms: " + str(NS))
        print("Obligations-Trading (Corner): c-Firms")
        print("Acceptable Firms: " + str(NA))
        print("Indirectly-Reforming Firms: " + str(NAprime))
    return NA, NAprime, NU, NR, NS, NUprime

def corner_ob_trading_share_prices(params: ModelParams) -> float:
    # Unpacking Parameters
    Ig, In, Is = params.Ig, params.In, params.Is
    K, T = params.K, params.T
    tau = params.tau
    mu_c , mu_d = params.mu_c, params.mu_d
    sigma_c, sigma_d, sigma_cd = params.sigma_c, params.sigma_d, params.sigma_cd
    Nc, Nd = params.Nc, params.Nd
    NA, NAprime, NU, NR, NS, NUprime = corner_ob_trading_corporate_choices(params)
    PA = mu_c - (1/((Ig + In)*tau)) * (NA * (sigma_c**2) + Nd * sigma_cd)
    PAprime = mu_c - (1/(Is * tau)) * (NAprime * (sigma_c**2) + NR * sigma_cd)
    PR = mu_d - (1/(Is * tau)) * (NAprime * sigma_cd + NR * (sigma_d**2))
    PU = PR - K
    PG = PU + T
    PS, PUprime = PG, PG

    return PA, PAprime, PU, PR, PS, PUprime

def corner_ob_trading_investor_positions(params: ModelParams) -> float:
    # Unpacking Parameters
    tau = params.tau
    mu_c , mu_d = params.mu_c, params.mu_d
    sigma_c, sigma_d, sigma_cd = params.sigma_c, params.sigma_d, params.sigma_cd
    phi = (sigma_c**2) * (sigma_d**2) - (sigma_cd**2)  # Cov Matrix Det
    PA, PAprime, PU, PR, PS, PUprime = corner_ob_trading_share_prices(params)
    NA, NAprime, NU, NR, NS, NUprime = corner_ob_trading_corporate_choices(params)
    PG = PS
    xnA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PU) * sigma_cd)
    xnU = (tau / phi) * ((mu_d - PU) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xgA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PG) * sigma_cd)
    xgG = (tau / phi) * ((mu_d - PG) * sigma_c**2 - (mu_c - PA) * sigma_cd)    
    xgS = NS / params.Ig
    xgUprime = NUprime / params.Ig
    xsAprime = (tau / phi) * ((mu_c - PAprime) * sigma_d**2 - (mu_d - PR) * sigma_cd)
    xsR = (tau / phi) * ((mu_d - PR) * sigma_c**2 - (mu_c - PAprime) * sigma_cd)
    return xnA, xnU, xgA, xgS, xgUprime, xsAprime, xsR

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

def solve_equilibrium(params: ModelParams) -> EqmAllocationOnly:

    # 1.1. Compute optimal corporate choices for allocation only
    NA, NU, NR, NS = alloc_only_corporate_choices(params)
    # 1.2. Compute share prices for allocation only
    PA, PU, PR, PS = alloc_only_share_prices(params)
    # 1.3. Compute investor positions for allocation only
    xnA, xnU, xgA, xgS, xsR = alloc_only_investor_positions(params)
    # 1.4 Eqm object for allocation only
    eqm_allocation_only = EqmAllocationOnly(
        NA = NA,
        NU = NU,
        NS = NS,
        NR = NR,
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

    # 2. Compute reform exchange thresholds
    pi_op, pi_ob = reform_exchange_compute_pi(params)
    # 2.1 Corner Obligations Trading
    if pi_ob < -params.T:
        if PrintBool:
            print("Corner Obligations Trading Detected")
        # 2.1.1 Corner Ob Trading Eqm Computation
        NA, NAprime, NU, NR, NS, NUprime = corner_ob_trading_corporate_choices(params)      #  Corner Ob Trading Corporate Choices 
        PA, PAprime, PU, PR, PS, PUprime = corner_ob_trading_share_prices(params)           #  Corner Ob Trading Share Prices
        xnA, xnU, xgA, xgS, xgUprime, xsAprime, xsR = corner_ob_trading_investor_positions(params)    #  Corner Ob Trading Investor Positions
        # 2.1.2 Corner Ob Trading Equilibrium Object
        eqm_corner_ob_trading = EqmCornerObTrading(
            NA = NA,
            NAprime = NAprime,
            NR = NR,
            NS = NS,
            NU = NU,
            NUprime = NUprime,
            PA = PA,
            PAprime = PAprime,
            PU = PU,
            PR = PR,
            PS = PS,
            PUprime = PUprime,
            xnA = xnA,
            xnU = xnU,
            xgA = xgA,
            xgS = xgS,
            xgUprime = xgUprime,
            xsAprime = xsAprime,
            xsR = xsR,
            pi = -params.T
        )

    return eqm_allocation_only, eqm_corner_ob_trading

