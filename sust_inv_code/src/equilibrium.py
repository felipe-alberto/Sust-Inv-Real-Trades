# Equilibrium Computation
# Project: Sustainable Investing Strategies For Real Asset Trades: Incentives to Own and Transform Pollutive Assets
# Author: Felipe Verastegui, PhD IEOR Columbia University
# Last Update: December 2025

# ----- Imports ---------------------------------------------------------------

from sust_inv_code.src.data_structures import ModelParams
from sust_inv_code.src.data_structures import FirmType, InvestorType
from sust_inv_code.src.data_structures import EquilibriumAllocationOnly, EquilibriumAllocationTransformation

# ----- Subfunctions ---------------------------------------------------------

PrintBool = True

def detect_regime(params: ModelParams, pi_op: float, pi_ob: float):
    if pi_ob < 0 or pi_op > 0:
        print("Diagnosing Instance...")
        if pi_ob< 0:
            if pi_ob >= - params.T:
                print("(Interior) Obligations Trading Instance Detected")
                return "transformation_interior_obligations_trading"
            elif pi_ob < - params.T:
                print("(Corner) Obligations Trading Instance Detected")
                return("transformation_corner_obligations_trading")
        elif pi_op > 0:
            print("Options Trading Instance Detected")
            return("transformation_options_trading")
    else:
        print("Undiagnosed Instance Detected")
        print("pi_op: ", pi_op)
        print("pi_ob: ", pi_ob)
        return "transformation_undiagnosed"

def alloc_only_corporate_choices(params: ModelParams):
    
    # Unpack

    p = params
    Ig, In, Is = p.Ig, p.In, p.Is
    K, T = p.K, p.T
    tau = p.tau
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    Igs, Isn, Ign = Ig + Is, Is + In, Ig + In
    
    # Lemma 3.1 Eqs: Allocation-Only Corporate Choice

    NA = Nc

    Unweighted_NU = (
        Nd 
        + Is * K * (tau / sigma_d**2) 
        + Ig * T * (tau / sigma_d**2) * (
            (Is * sigma_cd**2 + Ign * sigma_c**2 * sigma_d **2)/(Ign * phi))
        - (sigma_cd/sigma_d**2) * Nc * (Is / Ign)
    )
    Weighted_NU = (In / I) * (Unweighted_NU)
    NU = max(0, Weighted_NU) 

    Unweighted_NS = (
        Nd 
        + Is * K * (tau / sigma_d**2) 
        + Ig * T * (tau / sigma_d**2) * (
            (Ig * Is * sigma_cd**2 - Ign * Isn * sigma_c**2 * sigma_d **2)/(Ig*Ign* phi))
        - (sigma_cd/sigma_d**2) * Nc * (Is / Ign)
    )
    Weighted_NS = (Ig / I) * (Unweighted_NS)
    NS = max(0, Weighted_NS)

    Unweighted_NR = (
        Nd 
        - Ign * K * (tau / sigma_d**2) 
        + Ig * T * (tau / sigma_d**2) 
        + (sigma_cd / sigma_d**2)*Nc
    )
    Weighted_NR = (Is / I) * (Unweighted_NR)
    NR = max(0, Weighted_NR)
    
    return NA, NU, NR, NS

def alloc_only_share_prices(params: ModelParams):

    # Unpack

    p = params
    Ig, In, Is = p.Ig, p.In, p.Is
    K, T = p.K, p.T
    tau = p.tau
    mu_c, mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    Igs, Isn, Ign = Ig + Is, Is + In, Ig + In

    # Lemma 3.2 Eqs: Allocation-Only Share Prices

    PA = (mu_c  - (1 / I) * (
        + Nc * sigma_c**2 / tau
        + Nd * sigma_cd / tau 
        + (Is / Ign) * (Nc / tau) * (sigma_c**2 - sigma_cd**2 / sigma_d**2)
        + (Is) * (sigma_cd / sigma_d**2) * (K - (Ig / Ign) * T)
        )
    )
    PU = (mu_d  - (1 / I)*(
        + Nd * sigma_d**2 / tau 
        + Nc * sigma_cd / tau
        + Is * K 
        + Ig * T  
        )
    )
    PS = mu_d - (1 / I)*(
        + Nd * (sigma_d**2)/tau    
        + Nc  * (sigma_cd/tau)
        + Is * (K - T)   
        - In * T  
    )
    PR = mu_d - (1 / I)*(
        + Nd * (sigma_d**2)/tau 
        + Nc * (sigma_cd/tau) 
        - Ig * (K-T)   
        - In * K  
    )

    return PA, PU, PR, PS

def alloc_only_investor_positions(params: ModelParams):

    # Unpack
    p = params
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    phi = p.phi

    # Dependency
    PA, PU, PR, PS = alloc_only_share_prices(p)    

    # Positions (No Lemma)
    xnA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PU) * sigma_cd)
    xnU = (tau / phi) * ((mu_d - PU) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xgA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PS) * sigma_cd)
    xgS = (tau / phi) * ((mu_d - PS) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xsR = (tau / (sigma_d**2)) * (mu_d - PR)

    return xnA, xnU, xgA, xgS, xsR

def reform_exchange_compute_pi(params: ModelParams) -> float:

    # Unpack
    p = params
    Ig, In, Is = p.Ig, p.In, p.Is
    K, T = p.K, p.T
    tau = p.tau
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    Isn, Ign = Is + In, Ig + In

    # Eqs: Reform Exchange Prices
    pi_op = - K + (Is *Nc - (Ig + In)* Nd) * (sigma_c**2 * sigma_d**2) / (
    Is * (Ig + In) * (sigma_c**2 + sigma_d**2) * tau)                               # Hardcode sigma_cd = 0

    # Eqs: Reform Exchange Prices
    pi_ob = (
    ((Is * Nc - Ig * Nd)*(sigma_c**2 * sigma_d**2 - sigma_cd**2) # Psi Term
     - Is * K *(Ig * sigma_c**2 + (Ign)* sigma_d**2 - (2 * Ig + In) * sigma_cd) * tau)
    /
    ( (Ig*(Isn) * sigma_c**2 - 2 * Ig * Is * sigma_cd + Is * (Ign)* sigma_d**2) * tau )
                )      
    return pi_op, pi_ob 

def corner_ob_trading_corporate_choices(params: ModelParams) -> float:
    p = params
    Ig, In, Is = p.Ig, p.In, p.Is
    K, T = p.K, p.T
    tau = p.tau
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
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
    return NA, NAprime, NU, NR, NS, NUprime

def corner_ob_trading_share_prices(params: ModelParams) -> float:
    p = params
    Ig, In, Is = p.Ig, p.In, p.Is
    K, T = p.K, p.T
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    NA, NAprime, NU, NR, NS, NUprime = corner_ob_trading_corporate_choices(p)
    PA = mu_c - (1/((Ig + In)*tau)) * (NA * (sigma_c**2) + Nd * sigma_cd)
    PAprime = mu_c - (1/(Is * tau)) * (NAprime * (sigma_c**2) + NR * sigma_cd)
    PR = mu_d - (1/(Is * tau)) * (NAprime * sigma_cd + NR * (sigma_d**2))
    PU = PR - K
    PG = PU + T
    PS, PUprime = PG, PG
    return PA, PAprime, PU, PR, PS, PUprime

def corner_ob_trading_investor_positions(params: ModelParams) -> float:
    p = params
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    phi = p.phi
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

def interior_ob_trading_corporate_choices(params: ModelParams, pi_ob: float) -> float:
    
    # Unpack

    p = params
    Ig, In, Is = p.Ig, p.In, p.Is
    K, T = p.K, p.T
    tau = p.tau
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    Ign = Ig + In
    Isn = Is + In

    # Lemma 3.7

    Unweighted_NA = (Nc 
                    + K * Is * (tau / phi) * (sigma_d**2 - sigma_cd)
                    + pi_ob * Is * (tau / phi) * (sigma_d**2  - sigma_cd * (Ig / Ign)) 
    )
    Weighted_NA = ((Ig + In) / I) * (Unweighted_NA)
    NA = max(0, Weighted_NA)

    Unweighted_NA_Prime = (Nc 
                        - K * Ign * (tau / phi) * (sigma_d**2 - sigma_cd) 
                        - pi_ob * Ign * (tau / phi) * ( sigma_d**2  - sigma_cd * (Ig/Ign))
    ) 
    Weighted_NA_Prime = (Is / I ) * (Unweighted_NA_Prime)
    NAprime = max(0, Weighted_NA_Prime)

    Unweighted_NU = (Nd 
                    + K * Is * (tau / phi) * (sigma_c**2 - sigma_cd)
                    - pi_ob * Ig * (tau / phi) * (sigma_c**2 + sigma_cd * (Is/Ig))
    )  
    Weighted_NU = (In / I) * (Unweighted_NU)
    NU = max(0, Weighted_NU) 

    Unweighted_NU_Prime = (Nd 
                    + K * Is * (tau / phi)*(sigma_c**2 - sigma_cd) 
                    + pi_ob * Isn * (tau / phi) * (sigma_c**2 - sigma_cd * (Is / Isn) )
    )
    Weighted_NU_Prime = (Ig / I) * (Unweighted_NU_Prime)
    NUprime = max(0, Weighted_NU_Prime)

    Unweighted_NR = (Nd 
                    - K * Ign * (tau / phi) * (sigma_c**2 - sigma_cd)  
                    - pi_ob * Ig * (tau / phi) * (sigma_c**2 - sigma_cd * (Ign / Ig)) 
    )
    Weighted_NR = (Is / I) * (Unweighted_NR)
    NR = max(0, Weighted_NR)
  
    NS = 0

    return NA, NAprime, NU, NR, NS, NUprime

def interior_ob_trading_share_prices(params: ModelParams, pi_ob: float) -> float:

    # Unpack

    p = params
    Ig, In, Is = p.Ig, p.In, p.Is
    K, T = p.K, p.T
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    Ign = Ig + In

    PA = (mu_c - (1 / I) * (
        + Nc * sigma_c**2 / tau
        + Nd * sigma_cd / tau
        + Is * (K + pi_ob)
    )
    )
    PAprime = (mu_c - (1 / I) * (
        + Nc * sigma_c**2 / tau
        + Nd * sigma_cd / tau
        - Ign * (K + pi_ob)
    )
    )
    PU = (mu_d - (1 / I) * (
        + Nd * sigma_d**2 / tau
        + Nc * sigma_cd / tau
        + Is * K
        - Ig * pi_ob
    )
    )
    PUprime = (mu_d - (1 / I) * (
        + Nd * sigma_d**2 / tau
        + Nc * sigma_cd / tau
        + Is * (K + pi_ob)
        + In * pi_ob
    )
    )       
    PR = (mu_d - (1 / I) * (
        + Nd * sigma_d**2 / tau
        + Nc * sigma_cd / tau
        - In * K
        - Ig * (K + pi_ob)
    )
    )
    PS = (0)

    return PA, PAprime, PU, PR, PS, PUprime

def interior_ob_trading_investor_positions(params: ModelParams, pi_ob) -> float:
    p = params
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    phi = p.phi
    PA, PAprime, PU, PR, PS, PUprime = interior_ob_trading_share_prices(params, pi_ob)
    NA, NAprime, NU, NR, NS, NUprime = interior_ob_trading_corporate_choices(params, pi_ob)
    xnA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PU) * sigma_cd)
    xnU = (tau / phi) * ((mu_d - PU) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xgA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PUprime) * sigma_cd)
    xgUprime = (tau / phi) * ((mu_d - PUprime) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xsAprime = (tau / phi) * ((mu_c - PAprime) * sigma_d**2 - (mu_d - PR) * sigma_cd)
    xsR = (tau / phi) * ((mu_d - PR) * sigma_c**2 - (mu_c - PAprime) * sigma_cd)
    xgS = 0
    return xnA, xnU, xgA, xgS, xgUprime, xsAprime, xsR

def options_trading_corporate_choices(params: ModelParams, pi_op: float) -> float:
    p = params
    Ig, In, Is = p.Ig, p.In, p.Is
    K, T = p.K, p.T
    tau = p.tau
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    KerNUprime = (Nd + Is * (K + pi_op) *(tau / phi) * (sigma_c**2 - sigma_cd))
    CoreNUprime = ((In + Ig) / I) * (KerNUprime)
    NUprime = max(0, CoreNUprime) 
    KerNR = (Nd - (Ig + In) * (K + pi_op) *(tau / phi) * (sigma_c**2 - sigma_cd))
    CoreNR = (Is / I) * (KerNR)
    NR = max(0, CoreNR)
    KerNA = Nc + Is * (K + pi_op) * (tau / phi) * (sigma_d**2 - sigma_cd)
    CoreNA = ((Ig + In) / I) * (KerNA)
    NA = max(0, CoreNA)
    KerNAPrime = Nc - (Ig + In) * (K + pi_op) * (tau / phi) * (sigma_d**2 - sigma_cd)
    CoreNAPrime = (Is / I ) * (KerNAPrime)
    NAprime = max(0, CoreNAPrime)
    NU, NS = 0, 0
    return NA, NAprime, NU, NR, NS, NUprime

def options_trading_share_prices(params: ModelParams, pi_op: float) -> float:
    p = params
    Ig, In, Is = p.Ig, p.In, p.Is
    K, T = p.K, p.T
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    PA = mu_c - (Nc * sigma_c**2 + Is * (K + pi_op) * tau) / (I * tau) # HARDCODED FOR SIGMA_CD = 0
    PAprime = mu_c - (Nc * sigma_c**2 - (Ig + In) * (K + pi_op) * tau) / (I * tau) # HARDCODED FOR SIGMA_CD = 0
    PUprime = mu_d - (Nd * sigma_d**2 + Is * (K + pi_op) * tau) / (I * tau) # HARDCODED FOR SIGMA_CD = 0
    PR = mu_d - (Nd * sigma_d**2 - (Ig + In) * (K + pi_op) * tau) / (I * tau) # HARDCODED FOR SIGMA_CD = 0
    PU, PS = 0, 0
    return PA, PAprime, PU, PR, PS, PUprime

def options_trading_investor_positions(params: ModelParams, pi_op) -> float:
    p = params
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    phi = p.phi
    PA, PAprime, PU, PR, PS, PUprime = options_trading_share_prices(params, pi_op)
    xnA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PUprime) * sigma_cd)
    xnUprime = (tau / phi) * ((mu_d - PUprime) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xgA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PUprime) * sigma_cd)
    xgUprime = (tau / phi) * ((mu_d - PUprime) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xsAprime = (tau / phi) * ((mu_c - PAprime) * sigma_d**2 - (mu_d - PR) * sigma_cd)
    xsR = (tau / phi) * ((mu_d - PR) * sigma_c**2 - (mu_c - PAprime) * sigma_cd)
    xnU, xgS = 0, 0
    return xnA, xnUprime, xgA, xgS, xgUprime, xsAprime, xsR

def zero_price_corporate_choices(params: ModelParams) -> float:

    p = params
    Ig, In, Is = p.Ig, p.In, p.Is
    K, T = p.K, p.T
    tau = p.tau
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    psi, phi = p.psi, p.phi
    I = p.I
    Ign = Ig + In

    # Eqs: Zero-Price Corporate Choice
    NA = (Ign / I)* (Nc + Is * K * (sigma_d**2 - sigma_cd) * tau / phi)
    NAprime = (Is / I ) * (Nc - Ign * K * (sigma_d**2 - sigma_cd) * tau / phi)
    NUprime = (Is / I ) * (Nc - Ign * K * (sigma_d**2 - sigma_cd) * tau / phi)
    NU = (Ign / I) * (Nd - Nc * (Is / Ign) + Is * K * psi * tau / phi) 
    NR = (Is / I) * (Nd - Ign * K * (sigma_c**2 - sigma_cd) * tau / phi)
    NS = 0

    # print("Acceptable Firms:")
    # print(NA)
    # print("Indirectly Reforming Firms:")
    # print(NAprime)
    return NA, NAprime, NU, NR, NS, NUprime

def zero_price_share_prices(params: ModelParams) -> float:
    
    p = params
    Ig, In, Is = p.Ig, p.In, p.Is
    K, T = p.K, p.T
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    Ign = Ig + In
    
    """ OLD
    PremiumRK = (K / (I * phi)) * (sigma_c**2 - sigma_cd) * (Ign * sigma_d**2 - Ig * sigma_cd)
    PenaltyRNd = (Nd / (Is * I * tau)) * (Ig * sigma_cd + Is * sigma_d**2)
    PR = mu_d + PremiumRK - PenaltyRNd

    PolyD = (- Ig * sigma_c**2 * sigma_cd + 2 * Ig * sigma_cd**2 + In * sigma_cd**2 - Is * sigma_c**2 * sigma_d**2 
             - Ig * sigma_cd * sigma_d**2 - In * sigma_cd * sigma_d**2)
    PremiumDK = (K / (I * phi))*(PolyD)
    PenaltyDND = (Nd / (I * tau)) * ((Ig * sigma_cd + Is * sigma_d**2)/Is)
    PD = mu_d + PremiumDK - PenaltyDND

    PU = PD
    PUprime = PD
    PS = 0

    # 
    # PenaltyAK = - (K / (I * phi))*(- Ig * sigma_c**4 + 2 * Ig * sigma_c**2 * sigma_cd + In * sigma_c**2 * sigma_cd + Is * sigma_cd**2 - 
    #                               Ig * sigma_c**2 * sigma_d**2 - Is * sigma_c**2 * sigma_d**2 - In * sigma_c**2 * sigma_d**2)
    # PenaltyANd = (Nd / (I * tau)) * ((Ig * sigma_c**2 + Is * sigma_cd)/Is)
    # print("FLAG")
    # print(PenaltyAK)
    # print(PenaltyANd)
    # PA = mu_c - PenaltyAK - PenaltyANd
    # print(PA)
    
    PenaltyAprimeK = (K / (I * phi)) * (sigma_c**2 - sigma_cd) * (Ig * sigma_c**2 - Ign * sigma_cd)
    PenaltyAprimeNd = (Nd / (I * tau)) * ((Ig * sigma_c**2 + Is * sigma_cd)/Is)
    PAprime = mu_c - PenaltyAprimeK - PenaltyAprimeNd
    """

    # Eqs: Zero Price Share Prices
    PA = mu_c - K* (Is / I) - Nc * (sigma_c**2) / (I * tau) - Nd * (sigma_cd) / (I * tau)
    PAprime = mu_c + (Ign / I) * K - Nc * (sigma_c**2) / (I * tau) - Nd * (sigma_cd) / (I * tau)
    PD = mu_d - K * (Is / I) - Nc * (sigma_cd / (I * tau)) - Nd * (sigma_d**2) / (I * tau)
    PU = PD 
    PUprime = PD
    PR = mu_d + K * (Ign / I) - Nc * (sigma_cd / (I * tau)) - Nd * (sigma_d**2) / (I * tau)
    PS = 0
    return PA, PAprime, PU, PR, PS, PUprime

def zero_price_investor_positions(params: ModelParams) -> float:

    p = params
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    phi = p.phi
    Nc, Nd = p.Nc, p.Nd
    In, Ig, Is = p.In, p.Ig, p.Is
    I = p.I
    K = p.K
    psi = p.psi
    Ign = p.Ig + p.In
    
    # New
    xsR = (1/I) * (Nd - K * Ign * tau * (sigma_c**2 - sigma_cd) / phi)
    xsAprime = (1/I) * (Nc - K * Ign * tau * (sigma_d**2 - sigma_cd) / phi)
    xnA = (1/I) * (Nc + K * Is * tau * (sigma_d**2 - sigma_cd) / phi) 
    xnU = (1 / I) * (1 / In) * (Nd * Ign - Nc * Is + K * Is * Ign * psi * tau / phi)
    poly = - Ig * sigma_c**2 + 2 * Ig * sigma_cd + In * sigma_cd - Ig * sigma_d**2 - In * sigma_d**2
    xnUprime = (1 / I) * (1 / In) * (Nc * Is - Nd * Ig + Is * K * tau * (poly) / phi)
    xgUprime = (1/I) * (Nd + Is * K * (sigma_c**2 - sigma_cd) * tau / phi)
    xgA = (1 / I) * (Nc + Is * K * (sigma_d**2 - sigma_cd) * tau / phi)
    xgS = 0

    return xnA, xnU, xnUprime, xgA, xgS, xgUprime, xsAprime, xsR

# ----- Main solver ---------------------------------------------------------

def solve_equilibrium(params: ModelParams) -> tuple[EquilibriumAllocationOnly, EquilibriumAllocationTransformation]:

    # 1.1. Compute optimal corporate choices for allocation only
    NA, NU, NR, NS = alloc_only_corporate_choices(params)
    # 1.2. Compute share prices for allocation only
    PA, PU, PR, PS = alloc_only_share_prices(params)
    # 1.3. Compute investor positions for allocation only
    xnA, xnU, xgA, xgS, xsR = alloc_only_investor_positions(params)
    # 1.4 Eqm object for allocation only
    N = {
        FirmType.A: NA,
        FirmType.U: NU,
        FirmType.R: NR,
        FirmType.S: NS
    }
    P = {
        FirmType.A: PA,
        FirmType.U: PU,
        FirmType.R: PR,
        FirmType.S: PS,
    }
    X = {
        InvestorType.n: {
            FirmType.A: xnA,
            FirmType.U: xnU,
        },
        InvestorType.g: {
            FirmType.A: xgA,
            FirmType.S: xgS,
        },
        InvestorType.s: {
            FirmType.R: xsR,
        },
    }
    EqmAlloc = EquilibriumAllocationOnly(
        N=N,
        P=P,
        X=X,
        active_firms={FirmType.A, FirmType.U, FirmType.R, FirmType.S},
        active_links={
            InvestorType.n: {FirmType.A, FirmType.U},
            InvestorType.g: {FirmType.A, FirmType.S},
            InvestorType.s: {FirmType.R},
        },
        regime="allocation_only",
    )

    # 2. Detect Regime for Allocation + Transformation
    pi_op, pi_ob = reform_exchange_compute_pi(params)
    regime = detect_regime(params, pi_op, pi_ob)
    # 3. Compute Allocation + Transformation Equilibrium
    # 3.1 Corner Obligations Trading
    if regime == "transformation_corner_obligations_trading":
        # 3.1.1 Corner Ob Trading Eqm Computation
        NA, NAprime, NU, NR, NS, NUprime = corner_ob_trading_corporate_choices(params)      #  Corner Ob Trading Corporate Choices 
        PA, PAprime, PU, PR, PS, PUprime = corner_ob_trading_share_prices(params)           #  Corner Ob Trading Share Prices
        xnA, xnU, xgA, xgS, xgUprime, xsAprime, xsR = corner_ob_trading_investor_positions(params)    #  Corner Ob Trading Investor Positions
        # 3.1.2 Corner Ob Trading Equilibrium Object
        N = {
                FirmType.A: NA,
                FirmType.Aprime: NAprime,
                FirmType.U: NU,
                FirmType.R: NR,
                FirmType.S: NS,
                FirmType.Uprime: NUprime,
            }
        P = {
                FirmType.A: PA,
                FirmType.Aprime: PAprime,
                FirmType.U: PU,
                FirmType.R: PR,
                FirmType.S: PS,
                FirmType.Uprime: PUprime,
            }

        X = {
                InvestorType.n: {
                    FirmType.A: xnA,
                    FirmType.U: xnU,
                },
                InvestorType.g: {
                    FirmType.A: xgA,
                    FirmType.S: xgS,
                    FirmType.Uprime: xgUprime,
                },
                InvestorType.s: {
                    FirmType.Aprime: xsAprime,
                    FirmType.R: xsR,
                },
            }
        EqmTransform = EquilibriumAllocationTransformation(
                N=N,
                P=P,
                X=X,
                pi=-params.T,
                active_firms={FirmType.A, FirmType.Aprime, FirmType.U, FirmType.R, FirmType.S, FirmType.Uprime},
                active_links={
                    InvestorType.n: {FirmType.A, FirmType.U},
                    InvestorType.g: {FirmType.A, FirmType.S, FirmType.Uprime},
                    InvestorType.s: {FirmType.Aprime, FirmType.R},
                },
                regime=regime,
            )
    # 3.2 Interior Obligations Trading
    if regime == "transformation_interior_obligations_trading":
        # 3.2.1 Corner Ob Trading Eqm Computation
        NA, NAprime, NU, NR, NS, NUprime = interior_ob_trading_corporate_choices(params, pi_ob)      #  Corner Ob Trading Corporate Choices 
        PA, PAprime, PU, PR, PS, PUprime = interior_ob_trading_share_prices(params, pi_ob)           #  Corner Ob Trading Share Prices
        xnA, xnU, xgA, xgS, xgUprime, xsAprime, xsR = interior_ob_trading_investor_positions(params, pi_ob)    #  Corner Ob Trading Investor Positions
        # 3.2.2 Corner Ob Trading Equilibrium Object
        N = {
                FirmType.A: NA,
                FirmType.Aprime: NAprime,
                FirmType.U: NU,
                FirmType.R: NR,
                FirmType.S: NS,
                FirmType.Uprime: NUprime,
            }
        P = {
                FirmType.A: PA,
                FirmType.Aprime: PAprime,
                FirmType.U: PU,
                FirmType.R: PR,
                FirmType.S: PS,
                FirmType.Uprime: PUprime,
            }

        X = {
                InvestorType.n: {
                    FirmType.A: xnA,
                    FirmType.U: xnU,
                },
                InvestorType.g: {
                    FirmType.A: xgA,
                    FirmType.Uprime: xgUprime,
                },
                InvestorType.s: {
                    FirmType.Aprime: xsAprime,
                    FirmType.R: xsR,
                },
            }
        EqmTransform = EquilibriumAllocationTransformation(
                N=N,
                P=P,
                X=X,
                pi=pi_ob,
                active_firms={FirmType.A, FirmType.Aprime, FirmType.U, FirmType.R, FirmType.Uprime},
                active_links={
                    InvestorType.n: {FirmType.A, FirmType.U},
                    InvestorType.g: {FirmType.A, FirmType.Uprime},
                    InvestorType.s: {FirmType.Aprime, FirmType.R},
                },
                regime=regime,
            )
    # 3.3 Options Trading
    if regime == "transformation_options_trading":
        # 3.2.1 Corner Ob Trading Eqm Computation
        NA, NAprime, NU, NR, NS, NUprime = options_trading_corporate_choices(params, pi_op)      #  Corner Ob Trading Corporate Choices 
        PA, PAprime, PU, PR, PS, PUprime = options_trading_share_prices(params, pi_op)           #  Corner Ob Trading Share Prices
        xnA, xnUprime, xgA, xgS, xgUprime, xsAprime, xsR = options_trading_investor_positions(params, pi_op)    #  Corner Ob Trading Investor Positions
        # 3.2.2 Corner Ob Trading Equilibrium Object
        N = {
                FirmType.A: NA,
                FirmType.Aprime: NAprime,
                FirmType.U: NU,
                FirmType.R: NR,
                FirmType.S: NS,
                FirmType.Uprime: NUprime,
            }
        P = {
                FirmType.A: PA,
                FirmType.Aprime: PAprime,
                FirmType.U: PU,
                FirmType.R: PR,
                FirmType.S: PS,
                FirmType.Uprime: PUprime,
            }

        X = {
                InvestorType.n: {
                    FirmType.A: xnA,
                    FirmType.Uprime: xnUprime,
                },
                InvestorType.g: {
                    FirmType.A: xgA,
                    FirmType.S: xgS,
                    FirmType.Uprime: xgUprime,
                },
                InvestorType.s: {
                    FirmType.Aprime: xsAprime,
                    FirmType.R: xsR,
                },
            }
        EqmTransform = EquilibriumAllocationTransformation(
                N=N,
                P=P,
                X=X,
                pi=pi_op,
                active_firms={FirmType.A, FirmType.Aprime, FirmType.R, FirmType.Uprime},
                active_links={
                    InvestorType.n: {FirmType.A, FirmType.Uprime},
                    InvestorType.g: {FirmType.A, FirmType.Uprime},
                    InvestorType.s: {FirmType.Aprime, FirmType.R},
                },
                regime=regime,
            )
    # 3.4 Undiagnosed or Zero-Price Case
    if regime == "transformation_undiagnosed":
        NA, NAprime, NU, NR, NS, NUprime = zero_price_corporate_choices(params)      #  Zero Price Corporate Choices 
        PA, PAprime, PU, PR, PS, PUprime = zero_price_share_prices(params)           #  Zero Price Share Prices
        xnA, xnU, xnUprime, xgA, xgS, xgUprime, xsAprime, xsR = zero_price_investor_positions(params)    #  Zero Price Investor Positions
        N = {
                FirmType.A: NA,
                FirmType.Aprime: NAprime,
                FirmType.U: NU,
                FirmType.R: NR,
                FirmType.S: NS,
                FirmType.Uprime: NUprime,
            }
        P = {
                FirmType.A: PA,
                FirmType.Aprime: PAprime,
                FirmType.U: PU,
                FirmType.R: PR,
                FirmType.S: PS,
                FirmType.Uprime: PUprime,
            }

        X = {
                InvestorType.n: {
                    FirmType.A: xnA,
                    FirmType.U: xnU,
                    FirmType.Uprime : xnUprime,
                },
                InvestorType.g: {
                    FirmType.A: xgA,
                    FirmType.Uprime: xgUprime,
                },
                InvestorType.s: {
                    FirmType.Aprime: xsAprime,
                    FirmType.R: xsR,
                },
            }
        EqmTransform = EquilibriumAllocationTransformation(
                N=N,
                P=P,
                X=X,
                pi=0.0,
                active_firms={FirmType.A, FirmType.Aprime, FirmType.R, FirmType.Uprime, FirmType.U},
                active_links={
                    InvestorType.n: {FirmType.A, FirmType.Uprime, FirmType.U},
                    InvestorType.g: {FirmType.A, FirmType.Uprime},
                    InvestorType.s: {FirmType.Aprime, FirmType.R},
                },
                regime=regime,
            )

    return EqmAlloc, EqmTransform


"""
    if PrintBool:
        print("Obligations-Trading (Corner): d-Firms")
        print("Reformed Firms: " + str(NR))
        print("Green Firms: " + str(NG))
        print("Indirectly-Reformed Firms: " + str(NUprime))
        print("Secondary Trading Firms: " + str(NS))
        print("Obligations-Trading (Corner): c-Firms")
        print("Acceptable Firms: " + str(NA))
        print("Indirectly-Reforming Firms: " + str(NAprime))

"""