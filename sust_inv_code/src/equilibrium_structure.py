
# TODO:
# 1. There is a naming issue which should be fixed. Update notation for consistency with paper.
# 2. How does the equilibrium change with a carbon tax?
# 3. How does the equilibrium change with an emissions-trading scheme? 
# 4. Is there a consistency issue? In some regimes we are reporting 0 positions for some investor pairs,
# whereas in others there is no output. A definition should be made for this. 

# Equilibrium Structure

# ----- Imports ---------------------------------------------------------------

from sust_inv_code.src.data_structures import ModelParams, FirmType, InvestorType

# ----- Subfunctions ---------------------------------------------------------


def allocation_only_corporate_choices(params: ModelParams):
    
    # Unpack

    p = params
    In, Iv, Im = p.In, p.Iv, p.Im
    K, T = p.K, p.T
    tau = p.tau
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    Inm = In + Im
    Inv = In + Iv
    
    # Lemma 3.1 Eq: Allocation Only Corporate Choice

    n_a = Nc
    unweighted_n_u = (
        Nd 
        + Im * K * (tau / sigma_d**2) 
        + Iv * T * (tau ) * (sigma_c**2)/(phi)
        + Iv * T * (tau / sigma_d**2) * (Im * sigma_cd**2 )/(Inv * phi)
        - (sigma_cd/sigma_d**2) * Nc * (Im / Inv)
    )
    weighted_n_u = (In / I) * (unweighted_n_u)
    n_u = max(0, weighted_n_u) 

    unweighted_n_s = (
        Nd 
        + Im * K * (tau / sigma_d**2) 
        + Iv * T * (tau / sigma_d**2) * (
            (Iv * Im * sigma_cd**2 - Inv * Inm * sigma_c**2 * sigma_d **2)/(Iv*Inv* phi))
        - (sigma_cd/sigma_d**2) * Nc * (Im / Inv)
    )
    weighted_n_s = (Iv / I) * (unweighted_n_s)
    n_s = max(0, weighted_n_s)

    unweighted_n_r = (
        Nd 
        - Inv * K * (tau / sigma_d**2) 
        + Iv * T * (tau / sigma_d**2) 
        + (sigma_cd / sigma_d**2)*Nc
    )
    weighted_n_r = (Im / I) * (unweighted_n_r)
    n_r = max(0, weighted_n_r)
    N = {
        FirmType.A: n_a,
        FirmType.U: n_u,
        FirmType.R: n_r,
        FirmType.S: n_s
    }
    return N

def allocation_only_share_prices(params: ModelParams):

    # Unpack

    p = params
    In, Iv, Im = p.In, p.Iv, p.Im
    K, T = p.K, p.T
    tau = p.tau
    mu_c, mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    Ivm, Inm, Inv = Iv + Im, In + Im, In + Iv

    # Risk Penalties
    risk_c = (Nc * sigma_c**2 + Nd * sigma_cd) / (I*tau)
    risk_d = (Nd * sigma_d**2 + Nc * sigma_cd) / (I*tau)

    # Lemma 3.2 Eq: Allocation-Only Share Prices

    p_a = (mu_c  
          - risk_c 
          - (1 / I) * (
        + (Im / Inv) * (Nc / tau) * (sigma_c**2)
        - (Im / Inv) * (Nc / tau) * (sigma_cd**2 / sigma_d**2)
        + (Im) * (sigma_cd / sigma_d**2) * (K - (Iv / Inv) * T)
        )
    )
    p_u = (mu_d  
          - risk_d 
          - (1 / I)*(Im * K + Iv * T )
    )
    p_s = (mu_d 
          - risk_d 
          - (1 / I)*(Im * (K - T)   - In * T  )
    )
    p_r = (mu_d 
          - risk_d 
          + (1 / I)*(Iv * (K-T) + In * K  )
    )
    P = {
        FirmType.A: p_a,
        FirmType.U: p_u,
        FirmType.R: p_r,
        FirmType.S: p_s,
    }
    return P

def allocation_only_investor_positions(params: ModelParams):

    # Unpack
    p = params
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    phi = p.phi

    # Dependency
    P = allocation_only_share_prices(p)
    PA = P[FirmType.A]
    PU = P[FirmType.U]
    PR = P[FirmType.R]
    PS = P[FirmType.S]

    # Positions (No Lemma)
    xnA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PU) * sigma_cd)
    xnU = (tau / phi) * ((mu_d - PU) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xvA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PS) * sigma_cd)
    xvS = (tau / phi) * ((mu_d - PS) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xmR = (tau / (sigma_d**2)) * (mu_d - PR)
    X = {
        InvestorType.n: {
            FirmType.A: xnA,
            FirmType.U: xnU,
        },
        InvestorType.v: {
            FirmType.A: xvA,
            FirmType.S: xvS,
        },
        InvestorType.m: {
            FirmType.R: xmR,
        },
    }
    return X

def reform_exchange_compute_pi(params: ModelParams) -> tuple:

    # Unpack
    p = params
    In, Iv, Im = p.In, p.Iv, p.Im
    K, T = p.K, p.T
    tau = p.tau
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    Inv = In + Iv
    Inm = In + Im
    psi = p.psi
    phi = p.phi

    # Eqs: Option Price
    pi_op = (Nc / Inv - Nd / Im) * (phi) / (psi * tau) - K                                
    
    # Eqs: Obligation Price
    pi_ob = (
    ((Im * Nc - Iv * Nd)*(phi) # Phi Term
     - Im * K *(Iv * sigma_c**2 + (Inv)* sigma_d**2 - (2 * Iv + In) * sigma_cd) * tau)
    /
    ( (Iv*(Inm) * sigma_c**2 - 2 * Iv * Im * sigma_cd + Im * (Inv)* sigma_d**2) * tau )
                )
          
    return pi_op, pi_ob 

def corner_ob_trading_corporate_choices(params: ModelParams) -> dict:

    # Unpack
    p = params
    In, Iv, Im = p.In, p.Iv, p.Im
    K, T = p.K, p.T
    tau = p.tau
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    NR = (Im / I) * (
        Nd - K * (Iv + In) * (tau / phi) * sigma_c**2 + T* Iv * (tau / phi) * sigma_c**2)
    NG = (Iv / I) * (
        Nd + (K - T) * Im * (tau / phi) * sigma_c**2 - T * In * (tau / phi) * sigma_c**2)
    NAprime = (Im / I) * (
        Nc - (K - T) * Iv * (tau / phi) * sigma_d**2 - K * In * (tau / phi) * sigma_d**2 + T * In * (tau / phi) * sigma_d**2)
    NUprime = NAprime
    NS = NG - NUprime
    NA = Nc - NAprime
    NU = Nd - NR - NG
    N = {
            FirmType.A: NA,
            FirmType.Aprime: NAprime,
            FirmType.U: NU,
            FirmType.R: NR,
            FirmType.S: NS,
            FirmType.Uprime: NUprime,
        }
    return N

def corner_ob_trading_share_prices(params: ModelParams) -> dict:

    # Unpack
    p = params
    In, Iv, Im = p.In, p.Iv, p.Im
    K, T = p.K, p.T
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd

    # Dependency
    N = corner_ob_trading_corporate_choices(p)
    NA, NAprime = N[FirmType.A], N[FirmType.Aprime]
    NU, NR, NS, NUprime = N[FirmType.U], N[FirmType.R], N[FirmType.S], N[FirmType.Uprime]

    # Partial (?)
    PA = mu_c - (1/((Iv + In)*tau)) * (NA * (sigma_c**2) + Nd * sigma_cd)
    PAprime = mu_c - (1/(Im * tau)) * (NAprime * (sigma_c**2) + NR * sigma_cd)
    PR = mu_d - (1/(Im * tau)) * (NAprime * sigma_cd + NR * (sigma_d**2))
    PU = PR - K
    PG = PU + T
    PS, PUprime = PG, PG

    P = {
            FirmType.A: PA,
            FirmType.Aprime: PAprime,
            FirmType.U: PU,
            FirmType.R: PR,
            FirmType.S: PS,
            FirmType.Uprime: PUprime,
        }
    
    return P

def corner_ob_trading_investor_positions(params: ModelParams) -> dict:

    # Unpack
    p = params
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    phi = p.phi

    # Dependency 1
    P = corner_ob_trading_share_prices(params)
    PA, PAprime = P[FirmType.A], P[FirmType.Aprime]
    PU, PR, PS, PUprime = P[FirmType.U], P[FirmType.R], P[FirmType.S], P[FirmType.Uprime]

    # Dependency 2
    N = corner_ob_trading_corporate_choices(params)
    NA, NAprime = N[FirmType.A], N[FirmType.Aprime]
    NU, NR, NS, NUprime = N[FirmType.U], N[FirmType.R], N[FirmType.S], N[FirmType.Uprime]

    PG = PS
    xnA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PU) * sigma_cd)
    xnU = (tau / phi) * ((mu_d - PU) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xvA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PG) * sigma_cd)
    xvG = (tau / phi) * ((mu_d - PG) * sigma_c**2 - (mu_c - PA) * sigma_cd)    
    xvS = NS / p.Iv
    xvUprime = NUprime / p.Iv
    xmAprime = (tau / phi) * ((mu_c - PAprime) * sigma_d**2 - (mu_d - PR) * sigma_cd)
    xmR = (tau / phi) * ((mu_d - PR) * sigma_c**2 - (mu_c - PAprime) * sigma_cd)

    X = {
            InvestorType.n: {FirmType.A: xnA, 
                             FirmType.U: xnU},
            InvestorType.v: {FirmType.A: xvA,
                             FirmType.S: xvS,
                             FirmType.Uprime: xvUprime,
            },
            InvestorType.m: {FirmType.Aprime: xmAprime, 
                             FirmType.R: xmR},
        }
    
    return X

def interior_ob_trading_corporate_choices(params: ModelParams, pi_ob: float) -> dict:
    
    # Unpack
    p = params
    In, Iv, Im = p.In, p.Iv, p.Im
    K, T = p.K, p.T
    tau = p.tau
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    Inv = In + Iv
    Inm = In + Im

    # Lemma 3.7

    Unweighted_NA = (Nc 
                    + K * Im * (tau / phi) * (sigma_d**2 - sigma_cd)
                    + pi_ob * Im * (tau / phi) * (sigma_d**2  - sigma_cd * (Iv / Inv)) 
    )
    Weighted_NA = ((Iv + In) / I) * (Unweighted_NA)
    NA = max(0, Weighted_NA)

    Unweighted_NA_Prime = (Nc 
                        - K * Inv * (tau / phi) * (sigma_d**2 - sigma_cd) 
                        - pi_ob * Inv * (tau / phi) * ( sigma_d**2  - sigma_cd * (Iv/Inv))
    ) 
    Weighted_NA_Prime = (Im / I ) * (Unweighted_NA_Prime)
    NAprime = max(0, Weighted_NA_Prime)

    Unweighted_NU = (Nd 
                    + K * Im * (tau / phi) * (sigma_c**2 - sigma_cd)
                    - pi_ob * Iv * (tau / phi) * (sigma_c**2 + sigma_cd * (Im/Iv))
    )  
    Weighted_NU = (In / I) * (Unweighted_NU)
    NU = max(0, Weighted_NU) 

    Unweighted_NU_Prime = (Nd 
                    + K * Im * (tau / phi)*(sigma_c**2 - sigma_cd) 
                    + pi_ob * Inm * (tau / phi) * (sigma_c**2 - sigma_cd * (Im / Inm) )
    )
    Weighted_NU_Prime = (Im / I) * (Unweighted_NU_Prime)
    NUprime = max(0, Weighted_NU_Prime)

    Unweighted_NR = (Nd 
                    - K * Inv * (tau / phi) * (sigma_c**2 - sigma_cd)  
                    - pi_ob * Iv * (tau / phi) * (sigma_c**2 - sigma_cd * (Inv / Iv)) 
    )
    Weighted_NR = (Im / I) * (Unweighted_NR)
    NR = max(0, Weighted_NR)
    NS = 0
    N = {
            FirmType.A: NA,
            FirmType.Aprime: NAprime,
            FirmType.U: NU,
            FirmType.R: NR,
            FirmType.S: NS,
            FirmType.Uprime: NUprime,
        }
    return N

def interior_ob_trading_share_prices(params: ModelParams, pi_ob: float) -> dict:

    # Unpack

    p = params
    In, Iv, Im = p.In, p.Iv, p.Im
    K, T = p.K, p.T
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    Inv = In + Iv

    PA = (mu_c - (1 / I) * (
        + Nc * sigma_c**2 / tau
        + Nd * sigma_cd / tau
        + Im * (K + pi_ob)
    )
    )
    PAprime = (mu_c - (1 / I) * (
        + Nc * sigma_c**2 / tau
        + Nd * sigma_cd / tau
        - Inv * (K + pi_ob)
    )
    )
    PU = (mu_d - (1 / I) * (
        + Nd * sigma_d**2 / tau
        + Nc * sigma_cd / tau
        + Im * K
        - Iv * pi_ob
    )
    )
    PUprime = (mu_d - (1 / I) * (
        + Nd * sigma_d**2 / tau
        + Nc * sigma_cd / tau
        + Im * (K + pi_ob)
        + In * pi_ob
    )
    )       
    PR = (mu_d - (1 / I) * (
        + Nd * sigma_d**2 / tau
        + Nc * sigma_cd / tau
        - In * K
        - Iv * (K + pi_ob)
    )
    )
    PS = (0)

    P = {
                FirmType.A: PA,
                FirmType.Aprime: PAprime,
                FirmType.U: PU,
                FirmType.R: PR,
                FirmType.S: PS,
                FirmType.Uprime: PUprime,
            }
    
    return P

def interior_ob_trading_investor_positions(params: ModelParams, pi_ob) -> dict:

    # Unpack
    p = params
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    phi = p.phi

    # Dependency
    P = interior_ob_trading_share_prices(params, pi_ob)
    PA, PAprime = P[FirmType.A], P[FirmType.Aprime]
    PU, PR, PS, PUprime = P[FirmType.U], P[FirmType.R], P[FirmType.S], P[FirmType.Uprime]

    # Positions (No Lemma)
    xnA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PU) * sigma_cd)
    xnU = (tau / phi) * ((mu_d - PU) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xvA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PUprime) * sigma_cd)
    xvUprime = (tau / phi) * ((mu_d - PUprime) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xmAprime = (tau / phi) * ((mu_c - PAprime) * sigma_d**2 - (mu_d - PR) * sigma_cd)
    xmR = (tau / phi) * ((mu_d - PR) * sigma_c**2 - (mu_c - PAprime) * sigma_cd)
    xvS = 0

    X = {
                InvestorType.n: {FirmType.A: xnA, FirmType.U: xnU},
                InvestorType.v: {FirmType.A: xvA, FirmType.Uprime: xvUprime},
                InvestorType.m: {FirmType.Aprime: xmAprime, FirmType.R: xmR},
            }
    return X

def options_trading_corporate_choices(params: ModelParams, pi_op: float) -> dict:

    # Unpack
    p = params
    In, Iv, Im = p.In, p.Iv, p.Im
    K, T = p.K, p.T
    tau = p.tau
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    Inv = In + Iv

    # Lemma 3.4: Options Trading Corporate Choice

    Unweighted_NA = (
        Nc 
        + Im * (K + pi_op) * (tau / phi) * (sigma_d**2 - sigma_cd)
    )
    Weighted_NA = (Inv / I) * (Unweighted_NA)
    NA = max(0, Weighted_NA)

    Unweighted_NA_Prime = (
        Nc 
        - (Iv + In) * (K + pi_op) * (tau / phi) * (sigma_d**2 - sigma_cd)
    )
    Weighted_NA_Prime = (Im / I ) * (Unweighted_NA_Prime)
    NAprime = max(0, Weighted_NA_Prime)

    Unweighted_NU_Prime = (
        Nd 
        + Im * (K + pi_op) *(tau / phi) * (sigma_c**2 - sigma_cd)
    )
    Weighted_NU_Prime = (Inv/ I) * (Unweighted_NU_Prime)

    NUprime = max(0, Weighted_NU_Prime) 

    Unweighted_NR = (
        Nd 
        - Inv * (K + pi_op) *(tau / phi) * (sigma_c**2 - sigma_cd)
    )
    Weighted_NR = (Im / I) * (Unweighted_NR)
    NR = max(0, Weighted_NR)
    NU, NS = 0, 0
    N = {
            FirmType.A: NA,
            FirmType.Aprime: NAprime,
            FirmType.U: NU,
            FirmType.R: NR,
            FirmType.S: NS,
            FirmType.Uprime: NUprime,
        }

    return N

def options_trading_share_prices(params: ModelParams, pi_op: float) -> dict:
    
    # Unpack
    p = params
    In, Iv, Im = p.In, p.Iv, p.Im
    K, T = p.K, p.T
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I

    # Risk Penalties
    risk_c = (Nc * sigma_c**2 + Nd * sigma_cd) / (I*tau)
    risk_d = (Nd * sigma_d**2 + Nc * sigma_cd) / (I*tau)

    # Lemma 3.5 - Eqs: Options Trading Share Prices
    PA = (mu_c   
        - risk_c
        - (Im / I) * (K + pi_op)
    )
    PAprime = (mu_c  
        - risk_c
        + ((Iv + In) / I) * (K + pi_op)
    )
    PUprime = (mu_d  
        - risk_d
        - (Im / I) * (K + pi_op)
    )
    PR = (mu_d 
        - risk_d
        + ((Iv + In)/ I) * (K + pi_op)
    )
    PU, PS = 0, 0

    P = {
            FirmType.A: PA,
            FirmType.Aprime: PAprime,
            FirmType.U: PU,
            FirmType.R: PR,
            FirmType.S: PS,
            FirmType.Uprime: PUprime,
        }
    return P

def options_trading_investor_positions(params: ModelParams, pi_op) -> dict:
    
    # Unpack
    p = params
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    phi = p.phi

    # Dependency
    P = options_trading_share_prices(params, pi_op)
    PA, PAprime = P[FirmType.A], P[FirmType.Aprime]
    PU, PR, PS, PUprime = P[FirmType.U], P[FirmType.R], P[FirmType.S], P[FirmType.Uprime]

    # Positions (No Lemma)
    xnA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PUprime) * sigma_cd)
    xnUprime = (tau / phi) * ((mu_d - PUprime) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xvA = (tau / phi) * ((mu_c - PA) * sigma_d**2 - (mu_d - PUprime) * sigma_cd)
    xvUprime = (tau / phi) * ((mu_d - PUprime) * sigma_c**2 - (mu_c - PA) * sigma_cd)
    xmAprime = (tau / phi) * ((mu_c - PAprime) * sigma_d**2 - (mu_d - PR) * sigma_cd)
    xmR = (tau / phi) * ((mu_d - PR) * sigma_c**2 - (mu_c - PAprime) * sigma_cd)
    xnU, xvS = 0, 0

    X = {
            InvestorType.n: {FirmType.A: xnA, FirmType.Uprime: xnUprime},
            InvestorType.v: {
                FirmType.A: xvA,
                FirmType.S: xvS,
                FirmType.Uprime: xvUprime,
            },
            InvestorType.m: {FirmType.Aprime: xmAprime, FirmType.R: xmR},
        }

    return X


def zero_price_corporate_choices(params: ModelParams) -> dict:

    p = params
    In, Iv, Im = p.In, p.Iv, p.Im
    K, T = p.K, p.T
    tau = p.tau
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    psi, phi = p.psi, p.phi
    I = p.I
    Inv = In + Iv

    # Eqs: Zero-Price Corporate Choice
    NA = (Inv / I)* (Nc + Im * K * (sigma_d**2 - sigma_cd) * tau / phi)
    NAprime = (Im / I ) * (Nc - Inv * K * (sigma_d**2 - sigma_cd) * tau / phi)
    NUprime = (Im / I ) * (Nc - Inv * K * (sigma_d**2 - sigma_cd) * tau / phi)
    NU = (Inv / I) * (Nd - Nc * (Im / Inv) + Im * K * psi * tau / phi) 
    NR = (Im / I) * (Nd - Inv * K * (sigma_c**2 - sigma_cd) * tau / phi)
    NS = 0
    N = {
            FirmType.A: NA,
            FirmType.Aprime: NAprime,
            FirmType.U: NU,
            FirmType.R: NR,
            FirmType.S: NS,
            FirmType.Uprime: NUprime,
        }
    return N

def zero_price_share_prices(params: ModelParams) -> dict:
    
    p = params
    In, Iv, Im = p.In, p.Iv, p.Im
    K, T = p.K, p.T
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    Nc, Nd = p.Nc, p.Nd
    phi = p.phi
    I = p.I
    Inv = In + Iv
    

    # Eqs: Zero Price Share Prices
    PA = mu_c - K* (Im / I) - Nc * (sigma_c**2) / (I * tau) - Nd * (sigma_cd) / (I * tau)
    PAprime = mu_c + (Inv / I) * K - Nc * (sigma_c**2) / (I * tau) - Nd * (sigma_cd) / (I * tau)
    PD = mu_d - K * (Im / I) - Nc * (sigma_cd / (I * tau)) - Nd * (sigma_d**2) / (I * tau)
    PU = PD 
    PUprime = PD
    PR = mu_d + K * (Inv / I) - Nc * (sigma_cd / (I * tau)) - Nd * (sigma_d**2) / (I * tau)
    PS = 0
    P = {
            FirmType.A: PA,
            FirmType.Aprime: PAprime,
            FirmType.U: PU,
            FirmType.R: PR,
            FirmType.S: PS,
            FirmType.Uprime: PUprime,
        }
    return P

def zero_price_investor_positions(params: ModelParams) -> dict:

    p = params
    tau = p.tau
    mu_c , mu_d = p.mu_c, p.mu_d
    sigma_c, sigma_d, sigma_cd = p.sigma_c, p.sigma_d, p.sigma_cd
    phi = p.phi
    Nc, Nd = p.Nc, p.Nd
    In, Iv, Im = p.In, p.Iv, p.Im
    I = p.I
    K = p.K
    psi = p.psi
    Inv = p.In + p.Iv
    
    # New
    xmR = (1/I) * (Nd - K * Inv * tau * (sigma_c**2 - sigma_cd) / phi)
    xmAprime = (1/I) * (Nc - K * Inv * tau * (sigma_d**2 - sigma_cd) / phi)
    xnA = (1/I) * (Nc + K * Im * tau * (sigma_d**2 - sigma_cd) / phi) 
    xnU = (1 / I) * (1 / In) * (Nd * Inv - Nc * Im + K * Im * Inv * psi * tau / phi)
    poly = - Iv * sigma_c**2 + 2 * Iv * sigma_cd + In * sigma_cd - Iv * sigma_d**2 - In * sigma_d**2
    xnUprime = (1 / I) * (1 / In) * (Nc * Im - Nd * Iv + Im * K * tau * (poly) / phi)
    xvUprime = (1/I) * (Nd + Im * K * (sigma_c**2 - sigma_cd) * tau / phi)
    xvA = (1 / I) * (Nc + Im * K * (sigma_d**2 - sigma_cd) * tau / phi)
    xvS = 0

    X = {
                InvestorType.n: {
                    FirmType.A: xnA,
                    FirmType.U: xnU,
                    FirmType.Uprime: xnUprime,
                },
                InvestorType.v: {FirmType.A: xvA, FirmType.Uprime: xvUprime},
                InvestorType.m: {FirmType.Aprime: xmAprime, FirmType.R: xmR},
            }

    return X

