from sust_inv_code.src.data_structures import ModelParams, ModelResults
from sust_inv_code.src.data_structures import FirmType, InvestorType
from sust_inv_code.src.data_structures import EquilibriumAllocationOnly

# ----- Helpers ---------------------------------------------------------

CLEAN_FIRMS = {FirmType.A, FirmType.Aprime}
DIRTY_FIRMS = {FirmType.U, FirmType.S, FirmType.R, FirmType.Uprime}
INVESTOR_MASS = {
    InvestorType.n: "In",
    InvestorType.g: "Ig",
    InvestorType.s: "Is",
}

# ----- Subfunctions ---------------------------------------------------------

def get_positions(eqm):
    positions = {}
    for i in InvestorType:
        active = eqm.active_links.get(i, set())
        clean = sum(eqm.X[i].get(f, 0.0) for f in CLEAN_FIRMS if f in active)
        dirty = sum(eqm.X[i].get(f, 0.0) for f in DIRTY_FIRMS if f in active)
        positions[i] = {'clean':clean, 'dirty':dirty}
    return positions 

def net_risk_adjusted_return(clean, dirty, p):
    mean = clean * p.mu_c + dirty * p.mu_d
    risk = ( 1 / (2* p.tau)  
             * (
                clean**2 * p.sigma_c**2 
                + dirty**2 * p.sigma_d**2 
                + 2 * clean * dirty * p.sigma_cd
                )
            )
    return mean - risk

def investor_metrics(positions, params):
    risk_adj = {}
    mean = {}
    penalty = {}

    for i, pos in positions.items():
          mass = getattr(params, INVESTOR_MASS[i])
          c, d = pos["clean"], pos["dirty"]
          
          net = net_risk_adjusted_return(c, d, params)
          risk_adj[i] = mass * net
          mean[i] = mass * (c * params.mu_c + d * params.mu_d)
          penalty[i] = ( 1 / (2* params.tau)  
             * (
                c**2 * params.sigma_c**2 
                + d**2 * params.sigma_d**2 
                + 2 * c * d * params.sigma_cd
                )
            )
    return risk_adj, mean, penalty

def investor_transfers(eqm, params):
    transfers = {}

    for i in InvestorType:
        mass = getattr(params, INVESTOR_MASS[i])
        active = eqm.active_links.get(i, set())
        normalized = sum(eqm.X[i][f] * eqm.P[f] for f in active)
        transfers[i] = mass * normalized

    return transfers

def check_investor_masses(positions, params):
    import math

    clean_total = sum(
        getattr(params, INVESTOR_MASS[i]) * pos["clean"]
        for i, pos in positions.items()
    )
    dirty_total = sum(
        getattr(params, INVESTOR_MASS[i]) * pos["dirty"]
        for i, pos in positions.items()
    )

    assert math.isclose(clean_total, params.Nc, rel_tol=1e-9, abs_tol=1e-12)
    assert math.isclose(dirty_total, params.Nd, rel_tol=1e-9, abs_tol=1e-12)

# ----- Main routine ---------------------------------------------------------

def compute_results(eqm, params):

    # --- Positions ---
    positions = get_positions(eqm)
    check_investor_masses(positions, params)

    # --- Investor Metrics (Per Investor) ---
    risk_adj, mean, risk_penalty_by_i = investor_metrics(positions, params)
    transfers = investor_transfers(eqm, params)

    # --- Investor Metrics (Aggregates) ---
    total_risk_adj = sum(risk_adj.values())
    total_mean = sum(mean.values())
    total_risk_penalty = sum(risk_penalty_by_i.values())

    # --- Firm Metrics (Aggregates) ---
    market_cap = sum(eqm.N[f] * eqm.P[f] for f in eqm.active_firms)

    clean_market_cap = sum(
        eqm.N[f] * eqm.P[f] for f in CLEAN_FIRMS if f in eqm.active_firms
    )
    dirty_market_cap = sum(
        eqm.N[f] * eqm.P[f] for f in DIRTY_FIRMS if f in eqm.active_firms
    )

    firm_market_cap = {
        f: eqm.N[f] * eqm.P[f] if f in eqm.active_firms else 0
        for f in FirmType
    }

    # --- Transfers Consistency ---
    import math
    assert math.isclose(
        market_cap,
        sum(transfers.values()),
        rel_tol=1e-9,
        abs_tol=1e-12,
    )

    # --- Real Assets  ---
    reformed_assets = sum(eqm.N[f] for f in {FirmType.R, FirmType.Uprime} if f in eqm.active_firms)
    secondary_trading = sum(eqm.N[f] for f in {FirmType.S} if f in eqm.active_firms)

    # --- Surpluses ---
    firm_surplus = market_cap - (reformed_assets * params.K + secondary_trading * params.T)
    investor_surplus_dict = {
        i: risk_adj[i] - transfers[i] for i in InvestorType
    }
    investor_surplus = sum(investor_surplus_dict.values())
    total_surplus = total_risk_adj - (reformed_assets * params.K + secondary_trading * params.T)

    # --- Squares (for diagnostics) ---
    c_pos_squares = {i: pos["clean"]**2 for i, pos in positions.items()}
    d_pos_squares = {i: pos["dirty"]**2 for i, pos in positions.items()}

    # --- Net firm value ---
    firm_net_value = {
        f: (
            eqm.P[f]
            - (params.K if f == FirmType.R else 0)
            - (params.T if f == FirmType.S else 0)
            + (eqm.pi if f == FirmType.Uprime else 0)
            - (eqm.pi + params.K if f == FirmType.Aprime else 0)
        )
        if f in eqm.active_firms else 0
        for f in FirmType
    }

    # --- Output ---
    return ModelResults(
        risk_adjusted_return=total_risk_adj,
        mean_return=total_mean,
        risk_penalty=total_risk_penalty,
        reformed_assets=reformed_assets,
        secondary_trading=secondary_trading,
        market_capitalization=market_cap,
        firm_market_cap=firm_market_cap,
        firm_net_value=firm_net_value,
        clean_market_cap=clean_market_cap,
        dirty_market_cap=dirty_market_cap,
        net_market_cap=market_cap / (params.Nc + params.Nd),
        total_surplus=total_surplus,
        firm_surplus=firm_surplus,
        investor_surplus=investor_surplus,
        investor_surplus_dict=investor_surplus_dict,
        investor_risk_adjusted=risk_adj,
        investor_mean_returns=mean,
        investor_transfers=transfers,
        investor_risk_penalty=risk_penalty_by_i,
        c_pos_squares=c_pos_squares,
        d_pos_squares=d_pos_squares,
        pi=eqm.pi if eqm.regime != "allocation_only" else None,
    )

