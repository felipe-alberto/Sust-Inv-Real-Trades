
# src/main.py
# TODO: Debug market cap and risk adjusted welfare. 

from sust_inv_code.src.data_structures import ModelParams, EquilibriumOutcome
from sust_inv_code.src.equilibrium import solve_equilibrium
from sust_inv_code.src.tests import check_equilibrium
from sust_inv_code.src.results import compute_results

PrintBool = True

def run_model(params: ModelParams):
    outcome = solve_equilibrium(params)
    is_competitive_eqm = check_equilibrium(outcome, params)
    if not is_competitive_eqm:
        raise ValueError("Equilibrium conditions not satisfied")
    else:
        print("Equilibrium conditions satisfied!")
        results = compute_results(outcome, params)
        if PrintBool:
            print("Reformed assets in eqm:")
            print(results.reformed_assets)
            print("Secondary traded assets in eqm:")
            print(results.secondary_trading)
            print("Market Capitalization in eqm:")
            print(results.market_capitalization)
            print("Risk-Adjusted Welfare in eqm:")
            print(results.risk_adjusted_welfare)
        return results

if __name__ == "__main__":
    params = ModelParams(Ig=30, In=30, Is=30, K=0.9, T=0.5, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                        sigma_c=1.0, sigma_d=1.0, sigma_cd=0.00,
                        Nc=50, Nd=50)
    results = run_model(params)





