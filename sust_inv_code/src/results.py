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

def risk_adjusted_return(clean_pos: float, dirty_pos: float, params: ModelParams) -> float:
    
    p = params
    mean_return = (clean_pos * p.mu_c + dirty_pos * p.mu_d)
    risk = 1/(2* p.tau)  * (
        clean_pos**2 * p.sigma_c**2 + dirty_pos**2 * p.sigma_d**2 + 2 * clean_pos * dirty_pos * p.sigma_cd)
    
    return mean_return - risk

def compute_risk_adjusted_welfare_vector(eqm: EquilibriumAllocationOnly, params: ModelParams) -> float:
    
    p, e = params, eqm
    
    n_clean, n_dirty = get_clean_dirty_pos(InvestorType.n, e)
    n_risk_adjusted_return = risk_adjusted_return(n_clean, n_dirty, params)
    n_welfare = p.In * n_risk_adjusted_return

    g_clean, g_dirty = get_clean_dirty_pos(InvestorType.g, e)   
    g_risk_adjusted_return = risk_adjusted_return(g_clean, g_dirty, params)
    g_welfare = p.Ig * g_risk_adjusted_return

    s_clean, s_dirty = get_clean_dirty_pos(InvestorType.s, e)
    s_risk_adjusted_return = risk_adjusted_return(s_clean, s_dirty, params) 
    s_welfare = p.Is * s_risk_adjusted_return
    
    return n_welfare, g_welfare, s_welfare

# ----- Main routine ---------------------------------------------------------

def compute_results(eqm, params):
    
    reformed_assets = sum(eqm.N[f] for f in {FirmType.R, FirmType.Uprime}
                            if f in eqm.active_firms)
    secondary_trading  = sum(eqm.N[f] for f in {FirmType.S}
                            if f in eqm.active_firms)
    n_welfare, g_welfare, s_welfare = compute_risk_adjusted_welfare_vector(eqm, params)
    risk_adjusted_welfare = n_welfare + g_welfare + s_welfare
    market_capitalization = sum(eqm.N[f]*eqm.P[f] for f in eqm.active_firms)
    
    return ModelResults(
        risk_adjusted_welfare=risk_adjusted_welfare,
        reformed_assets=reformed_assets,
        secondary_trading=secondary_trading,
        market_capitalization=market_capitalization,
        investor_welfare= {
            InvestorType.n: n_welfare,
            InvestorType.g: g_welfare,
            InvestorType.s: s_welfare
        }
        )