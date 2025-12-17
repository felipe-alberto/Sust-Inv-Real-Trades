from sust_inv_code.src.data_structures import ModelParams, ModelResults
from sust_inv_code.src.types import FirmType, InvestorType
from sust_inv_code.src.equilibrium_state import EquilibriumAllocationOnly


# ----- Subfunctions ---------------------------------------------------------

def compute_risk_adjusted_welfare(eqm: EquilibriumAllocationOnly, params: ModelParams) -> float:
    p, e = params, eqm
    i = InvestorType.n
    n_clean = sum(e.X[i].get(f, 0.0) for f in {FirmType.A, FirmType.Aprime}
                  if f in e.active_links.get(i, set())
    )
    n_dirty = sum(e.X[i].get(f, 0.0) for f in {FirmType.U, FirmType.S, FirmType.R, FirmType.Uprime}
                  if f in e.active_links.get(i, set())
    )
    n_mean = (n_clean * params.mu_c + n_dirty * params.mu_d)
    n_risk = 1/(2* params.tau)  * (
        n_clean**2 * params.sigma_c**2 + n_dirty**2 * params.sigma_d**2 + 2 * n_clean * n_dirty * params.sigma_cd)
    i = InvestorType.g
    g_clean = sum(e.X[i].get(f, 0.0) for f in {FirmType.A, FirmType.Aprime}
                    if f in e.active_links.get(i, set())
    )
    g_dirty = sum(e.X[i].get(f, 0.0) for f in {FirmType.U, FirmType.S, FirmType.R, FirmType.Uprime}
                    if f in e.active_links.get(i, set())
    )
    g_mean = (g_clean * params.mu_c + g_dirty * params.mu_d)
    g_risk = 1/(2* params.tau)  * (
        g_clean**2 * params.sigma_c**2 + g_dirty**2 * params.sigma_d**2 + 2 * g_clean * g_dirty * params.sigma_cd)
    i = InvestorType.s
    s_clean = sum(e.X[i].get(f, 0.0) for f in {FirmType.A, FirmType.Aprime}
                    if f in e.active_links.get(i, set())
    )
    s_dirty = sum(e.X[i].get(f, 0.0) for f in {FirmType.U, FirmType.S, FirmType.R, FirmType.Uprime}
                    if f in e.active_links.get(i, set())
    )
    s_mean = (s_clean * params.mu_c + s_dirty * params.mu_d)
    s_risk = 1/(2* params.tau)  * (
        s_clean**2 * params.sigma_c**2 + s_dirty**2 * params.sigma_d**2 + 2 * s_clean * s_dirty * params.sigma_cd)
    risk_adjusted_welfare = p.In*(n_mean - n_risk) + p.Ig*(g_mean - g_risk) + p.Is*(s_mean - s_risk)
    return risk_adjusted_welfare

# ----- Main routine ---------------------------------------------------------

def compute_results(outcome, params):
    
    reformed_assets = outcome.NR
    secondary_trading = outcome.NS
    risk_adjusted_welfare = compute_risk_adjusted_welfare(outcome, params)
    market_capitalization = (
        outcome.NA * outcome.PA + outcome.NU * outcome.PU + outcome.NS * outcome.PS + outcome.NR * outcome.PR
        )

    return ModelResults(
        risk_adjusted_welfare=risk_adjusted_welfare,
        reformed_assets=reformed_assets,
        secondary_trading=secondary_trading,
        market_capitalization=market_capitalization
        )

def compute_results(eqm, params):
    reformed_assets = sum(eqm.N[f] for f in {FirmType.R, FirmType.Uprime}
                            if f in eqm.active_firms)
    secondary_trading  = sum(eqm.N[f] for f in {FirmType.S}
                            if f in eqm.active_firms)
    risk_adjusted_welfare = compute_risk_adjusted_welfare(eqm, params)
    market_capitalization = sum(eqm.N[f]*eqm.P[f] for f in eqm.active_firms)

    return ModelResults(
        risk_adjusted_welfare=risk_adjusted_welfare,
        reformed_assets=reformed_assets,
        secondary_trading=secondary_trading,
        market_capitalization=market_capitalization
        )