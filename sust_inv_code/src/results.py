from sust_inv_code.src.data_structures import ModelParams, ModelResults
from sust_inv_code.src.data_structures import FirmType, InvestorType
from sust_inv_code.src.data_structures import EquilibriumAllocationOnly


# ----- Subfunctions ---------------------------------------------------------

def get_clean_dirty_pos(i, eqm):
    clean_pos = sum(eqm.X[i].get(f, 0.0) for f in {FirmType.A, FirmType.Aprime}
                  if f in eqm.active_links.get(i, set())
    )
    dirty_pos = sum(eqm.X[i].get(f, 0.0) for f in {FirmType.U, FirmType.S, FirmType.R, FirmType.Uprime}
                  if f in eqm.active_links.get(i, set())
    )
    return clean_pos, dirty_pos

def get_c_pos_squares(i, eqm):
    clean_pos, _ = get_clean_dirty_pos(i, eqm)
    return clean_pos**2

def get_d_pos_squares(i, eqm):
    _, dirty_pos = get_clean_dirty_pos(i, eqm)
    return dirty_pos**2

def net_risk_adjusted_return(clean_pos: float, dirty_pos: float, params: ModelParams) -> float:
    
    p = params
    mean_return = clean_pos * p.mu_c + dirty_pos * p.mu_d
    risk_exposure = 1/(2* p.tau)  * (clean_pos**2 * p.sigma_c**2 + dirty_pos**2 * p.sigma_d**2 + 2 * clean_pos * dirty_pos * p.sigma_cd)
    return mean_return - risk_exposure

def compute_risk_adjusted_returns(eqm: EquilibriumAllocationOnly, params: ModelParams) -> float:
    
    p, e = params, eqm
    
    n_clean_pos, n_dirty_pos = get_clean_dirty_pos(InvestorType.n, e)
    n_net_risk_adjusted_return = net_risk_adjusted_return(n_clean_pos, n_dirty_pos, params)
    n_risk_adjusted_return = p.In * n_net_risk_adjusted_return

    g_clean_pos, g_dirty_pos = get_clean_dirty_pos(InvestorType.g, e)   
    g_net_risk_adjusted_return = net_risk_adjusted_return(g_clean_pos, g_dirty_pos, params)
    g_risk_adjusted_return = p.Ig * g_net_risk_adjusted_return

    s_clean_pos, s_dirty_pos = get_clean_dirty_pos(InvestorType.s, e)
    s_net_risk_adjusted_return = net_risk_adjusted_return(s_clean_pos, s_dirty_pos, params) 
    s_risk_adjusted_return = p.Is * s_net_risk_adjusted_return
    
    print("CHECKING INVESTOR MASSES...")
    import math
    assert(math.isclose(
        n_clean_pos*p.In + g_clean_pos*p.Ig + s_clean_pos*p.Is,
        p.Nc,
        rel_tol=1e-9,
        abs_tol=1e-12,
    )), "Clean positions do not sum to clean investor mass"
    print("FLAG -- ")
    assert(math.isclose(
        n_dirty_pos*p.In + g_dirty_pos*p.Ig + s_dirty_pos*p.Is,
        p.Nd,
        rel_tol=1e-9,
        abs_tol=1e-12,
    )), "Dirty positions do not sum to dirty investor mass"
    print("Investor masses check out.")
    return n_risk_adjusted_return, g_risk_adjusted_return, s_risk_adjusted_return

def compute_mean_returns(eqm: EquilibriumAllocationOnly, params: ModelParams) -> float:
    
    p, e = params, eqm
    n_clean_pos, n_dirty_pos = get_clean_dirty_pos(InvestorType.n, e)
    n_mean_return = p.In * (n_clean_pos * p.mu_c + n_dirty_pos * p.mu_d)
    g_clean_pos, g_dirty_pos = get_clean_dirty_pos(InvestorType.g, e)   
    g_mean_return = p.Ig * (g_clean_pos * p.mu_c + g_dirty_pos * p.mu_d)
    s_clean_pos, s_dirty_pos = get_clean_dirty_pos(InvestorType.s, e)
    s_mean_return = p.Is * (s_clean_pos * p.mu_c + s_dirty_pos * p.mu_d)
    return n_mean_return, g_mean_return, s_mean_return

def compute_risk_penalty(eqm: EquilibriumAllocationOnly, params: ModelParams) -> float:
    p, e = params, eqm
    n_clean_pos, n_dirty_pos = get_clean_dirty_pos(InvestorType.n, e)
    n_risk_penalty = p.In * (1/(2* p.tau)  * (n_clean_pos**2 * p.sigma_c**2 + n_dirty_pos**2 * p.sigma_d**2 + 2 * n_clean_pos * n_dirty_pos * p.sigma_cd))
    g_clean_pos, g_dirty_pos = get_clean_dirty_pos(InvestorType.g, e)   
    g_risk_penalty = p.Ig * (1/(2* p.tau)  * (g_clean_pos**2 * p.sigma_c**2 + g_dirty_pos**2 * p.sigma_d**2 + 2 * g_clean_pos * g_dirty_pos * p.sigma_cd))
    s_clean_pos, s_dirty_pos = get_clean_dirty_pos(InvestorType.s, e)
    s_risk_penalty = p.Is * (1/(2* p.tau)  * (s_clean_pos**2 * p.sigma_c**2 + s_dirty_pos**2 * p.sigma_d**2 + 2 * s_clean_pos * s_dirty_pos * p.sigma_cd))
    risk_penalty = n_risk_penalty + g_risk_penalty + s_risk_penalty
    return risk_penalty

def compute_investor_transfers(eqm: EquilibriumAllocationOnly, params: ModelParams) -> float:
    p, e = params, eqm

    normalized_n_transfers = sum(eqm.X[InvestorType.n][f]*eqm.P[f] for f in eqm.active_links.get(InvestorType.n, set()))
    n_all_transfers = params.In* normalized_n_transfers

    normalized_g_transfers = sum(eqm.X[InvestorType.g][f]*eqm.P[f] for f in eqm.active_links.get(InvestorType.g, set()))
    g_all_transfers = params.Ig* normalized_g_transfers

    normalized_s_transfers = sum(eqm.X[InvestorType.s][f]*eqm.P[f] for f in eqm.active_links.get(InvestorType.s, set()))
    s_all_transfers = params.Is* normalized_s_transfers
    return n_all_transfers, g_all_transfers, s_all_transfers
# ----- Main routine ---------------------------------------------------------

def compute_results(eqm, params):
    
    n_c_pos_squares = get_c_pos_squares(InvestorType.n, eqm)
    n_d_pos_squares = get_d_pos_squares(InvestorType.n, eqm)
    g_c_pos_squares = get_c_pos_squares(InvestorType.g, eqm)
    g_d_pos_squares = get_d_pos_squares(InvestorType.g, eqm)
    s_c_pos_squares = get_c_pos_squares(InvestorType.s, eqm)
    s_d_pos_squares = get_d_pos_squares(InvestorType.s, eqm)

    c_pos_squares = {
        InvestorType.n: n_c_pos_squares,
        InvestorType.g: g_c_pos_squares,
        InvestorType.s: s_c_pos_squares
    }
    d_pos_squares = {
        InvestorType.n: n_d_pos_squares,
        InvestorType.g: g_d_pos_squares,
        InvestorType.s: s_d_pos_squares
    }
    investor_risk_penalty = {
        InvestorType.n: params.In * (1/(2* params.tau)  * (n_c_pos_squares * params.sigma_c**2 + n_d_pos_squares * params.sigma_d**2 + 2 * get_clean_dirty_pos(InvestorType.n, eqm)[0] * get_clean_dirty_pos(InvestorType.n, eqm)[1] * params.sigma_cd)),
        InvestorType.g: params.Ig * (1/(2* params.tau)  * (g_c_pos_squares * params.sigma_c**2 + g_d_pos_squares * params.sigma_d**2 + 2 * get_clean_dirty_pos(InvestorType.g, eqm)[0] * get_clean_dirty_pos(InvestorType.g, eqm)[1] * params.sigma_cd)),
        InvestorType.s: params.Is * (1/(2* params.tau)  * (s_c_pos_squares * params.sigma_c**2 + s_d_pos_squares * params.sigma_d**2 + 2 * get_clean_dirty_pos(InvestorType.s, eqm)[0] * get_clean_dirty_pos(InvestorType.s, eqm)[1] * params.sigma_cd))
    }
    reformed_assets = sum(eqm.N[f] for f in {FirmType.R, FirmType.Uprime}
                            if f in eqm.active_firms)
    secondary_trading  = sum(eqm.N[f] for f in {FirmType.S}
                            if f in eqm.active_firms)
    n_risk_adjusted, g_risk_adjusted, s_risk_adjusted = compute_risk_adjusted_returns(eqm, params)
    n_mean_return, g_mean_return, s_mean_return = compute_mean_returns(eqm, params)
    n_all_transfers, g_all_transfers, s_all_transfers = compute_investor_transfers(eqm, params)
    risk_adjusted_return = n_risk_adjusted + g_risk_adjusted + s_risk_adjusted
    market_capitalization = sum(eqm.N[f]*eqm.P[f] for f in eqm.active_firms)
    clean_market_capitalization = sum(eqm.N[f] * eqm.P[f] for f in {FirmType.A, FirmType.Aprime} if f in eqm.active_firms)
    dirty_market_capitalization = sum(eqm.N[f] * eqm.P[f] for f in {FirmType.U, FirmType.S, FirmType.R, FirmType.Uprime} if f in eqm.active_firms)
    clean_firms_cost = sum(eqm.N[f] * params.K for f in {FirmType.Aprime} if f in eqm.active_firms)
    dirty_firms_cost = sum(eqm.N[f] * params.K for f in {FirmType.R} if f in eqm.active_firms)
    print(market_capitalization)
    print(n_all_transfers + g_all_transfers + s_all_transfers)
    import math
    assert math.isclose(
    market_capitalization,
    n_all_transfers + g_all_transfers + s_all_transfers,
    rel_tol=1e-9,
    abs_tol=1e-12,
    ), "Market capitalization does not equal total investor transfers"
    print("Market capitalization matches total investor transfers.")
    net_market_cap = market_capitalization / (params.Nc + params.Nd)
    firm_surplus = market_capitalization - (reformed_assets * params.K + secondary_trading * params.T)
    clean_firm_surplus = clean_market_capitalization - sum(eqm.N[f] * params.K for f in {FirmType.Aprime} if f in eqm.active_firms)
    dirty_firm_surplus = dirty_market_capitalization - sum(eqm.N[f] * eqm.P[f] for f in {FirmType.A, FirmType.Aprime} if f in eqm.active_firms)
    investor_surplus = risk_adjusted_return - market_capitalization
    total_surplus = risk_adjusted_return - (reformed_assets * params.K + secondary_trading * params.T)
    firm_market_cap = {f: eqm.N[f] * eqm.P[f] if f in eqm.active_firms else 0 for f in FirmType}
    clean_market_cap = sum(
        eqm.N[f] * eqm.P[f] for f in {FirmType.A, FirmType.Aprime}
            if f in eqm.active_firms
    )
    dirty_market_cap = sum(
        eqm.N[f] * eqm.P[f] for f in {FirmType.U, FirmType.S, FirmType.R, FirmType.Uprime}
            if f in eqm.active_firms
    )
    firm_net_value = {f: (eqm.P[f] 
                                     - (params.K if f in {FirmType.R} else 0) 
                                     - (params.T if f in {FirmType.S} else 0)
                                     + (eqm.pi if f in {FirmType.Uprime} else 0)
                                     - (eqm.pi + params.K if f in {FirmType.Aprime} else 0)
                                     ) 
                        if f in eqm.active_firms else 0 for f in FirmType}
    investor_surplus_dict = {
        InvestorType.n: n_risk_adjusted - n_all_transfers,
        InvestorType.g: g_risk_adjusted - g_all_transfers,
        InvestorType.s: s_risk_adjusted - s_all_transfers
    }
    risk_penalty = compute_risk_penalty(eqm, params)
    if eqm.regime=="allocation_only":
        return ModelResults(
            risk_adjusted_return=risk_adjusted_return,
            reformed_assets=reformed_assets,
            secondary_trading=secondary_trading,
            market_capitalization=market_capitalization,
            investor_risk_penalty=investor_risk_penalty,
            investor_risk_adjusted= {
                InvestorType.n: n_risk_adjusted,
                InvestorType.g: g_risk_adjusted,
                InvestorType.s: s_risk_adjusted
            },
            investor_mean_returns= {
                InvestorType.n: n_mean_return,
                InvestorType.g: g_mean_return,
                InvestorType.s: s_mean_return
            },
            mean_return = n_mean_return + g_mean_return + s_mean_return,
            risk_penalty = risk_penalty,
            c_pos_squares = c_pos_squares,
            d_pos_squares = d_pos_squares,
            investor_transfers= {
                InvestorType.n: n_all_transfers,
                InvestorType.g: g_all_transfers,
                InvestorType.s: s_all_transfers
            },
            firm_market_cap=firm_market_cap,
            firm_net_value=firm_net_value,
            clean_market_cap=clean_market_cap,
            dirty_market_cap=dirty_market_cap,
            net_market_cap=net_market_cap,
            total_surplus=total_surplus,
            firm_surplus = firm_surplus,
            investor_surplus = investor_surplus,
            investor_surplus_dict = investor_surplus_dict
            )
    else:
                return ModelResults(
            risk_adjusted_return=risk_adjusted_return,
            reformed_assets=reformed_assets,
            secondary_trading=secondary_trading,
            market_capitalization=market_capitalization,
            investor_risk_adjusted= {
                InvestorType.n: n_risk_adjusted,
                InvestorType.g: g_risk_adjusted,
                InvestorType.s: s_risk_adjusted
            },
            investor_mean_returns= {
                InvestorType.n: n_mean_return,
                InvestorType.g: g_mean_return,
                InvestorType.s: s_mean_return
            },
            mean_return = n_mean_return + g_mean_return + s_mean_return,
            risk_penalty = risk_penalty,
            c_pos_squares = c_pos_squares,
            d_pos_squares = d_pos_squares,
            investor_transfers= {
                InvestorType.n: n_all_transfers,
                InvestorType.g: g_all_transfers,
                InvestorType.s: s_all_transfers
            },
            firm_market_cap=firm_market_cap,
            firm_net_value=firm_net_value,
            clean_market_cap=clean_market_cap,
            dirty_market_cap=dirty_market_cap,
            net_market_cap=net_market_cap,
            total_surplus=total_surplus,
            firm_surplus = firm_surplus,
            investor_surplus = investor_surplus,
            investor_surplus_dict = investor_surplus_dict,
            pi = eqm.pi
            )
    