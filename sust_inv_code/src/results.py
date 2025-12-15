from sust_inv_code.src.data_structures import ModelParams, EquilibriumOutcome, ModelResults

# ----- Subfunctions ---------------------------------------------------------

def compute_risk_adjusted_welfare(outcome: EquilibriumOutcome, params: ModelParams) -> float:
    n_mean = (outcome.xnA * params.mu_c + outcome.xnU * params.mu_d)
    n_risk = 1/(2* params.tau)  * (
        outcome.xnA**2 * params.sigma_c**2 + outcome.xnU**2 * params.sigma_d**2 + 2 * outcome.xnA * outcome.xnU * params.sigma_cd)
    g_mean = (outcome.xgA * params.mu_c + outcome.xgS * params.mu_d)
    g_risk = 1/(2* params.tau)  * (
        outcome.xgA**2 * params.sigma_c**2 + outcome.xgS**2 * params.sigma_d**2 + 2 * outcome.xgA * outcome.xgS * params.sigma_cd)
    s_mean = (outcome.xsR * params.mu_d)
    s_risk = 1/(2* params.tau)  * (outcome.xsR**2 * params.sigma_d**2)
    risk_adjusted_welfare = params.In*(n_mean - n_risk) + params.Ig*(g_mean - g_risk) + params.Is*(s_mean - s_risk)
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