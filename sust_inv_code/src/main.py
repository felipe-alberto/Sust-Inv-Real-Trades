
# src/main.py
# TODO: Debug market cap and risk adjusted welfare. 

from sust_inv_code.src.data_structures import ModelParams
from sust_inv_code.src.equilibrium import solve_equilibrium
from sust_inv_code.src.tests import check_eqm_allocation_only, check_eqm_corner_ob_trading
from sust_inv_code.src.results import compute_results

PrintBool = True

def run_model(params: ModelParams):
    
    eqm_allocation_only, eqm_corner_ob_trading = solve_equilibrium(params)
    
    # Check Allocation Only Equilibrium
    is_competitive_eqm = check_eqm_allocation_only(eqm_allocation_only, params)
    if not is_competitive_eqm:
        raise ValueError("Equilibrium conditions not satisfied")
    else:
        print("Equilibrium conditions satisfied for allocation only!")
        results_allocation_only = compute_results(eqm_allocation_only, params)
        if PrintBool:
            r = results_allocation_only
            print("Reformed assets in eqm:")
            print(r.reformed_assets)
            print("Secondary traded assets in eqm:")
            print(r.secondary_trading)
            print("Market Capitalization in eqm:")
            print(r.market_capitalization)
            print("Risk-Adjusted Welfare in eqm:")
            print(r.risk_adjusted_welfare)
    
    # Check Corner OB Trading Equilibrium
    is_competitive_eqm = check_eqm_corner_ob_trading(eqm_corner_ob_trading, params)
    if not is_competitive_eqm:
        raise ValueError("Equilibrium conditions not satisfied")
    else:
        print("Equilibrium conditions satisfied for corner OB trading!")
        directly_reformed_assets = eqm_corner_ob_trading.NR
        secondary_trading = eqm_corner_ob_trading.NS
        indirectly_reformed_assets = eqm_corner_ob_trading.NUprime
        reformed_assets = directly_reformed_assets + indirectly_reformed_assets
    print(reformed_assets, r.reformed_assets)
    print(secondary_trading, r.secondary_trading)
    return results_allocation_only

if __name__ == "__main__":
    params = ModelParams(Ig=30, In=30, Is=30, K=0.9, T=0.5, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                        sigma_c=1.0, sigma_d=1.0, sigma_cd=0.0,
                        Nc=50, Nd=50)
    results = run_model(params)





