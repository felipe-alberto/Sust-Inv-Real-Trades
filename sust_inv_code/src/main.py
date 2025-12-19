
# src/main.py
# TODO: 
# - Test options-trading regime, (interior) obligations-trading regime, zero obligations trading regime. 
# - Think about the max's
# - Should we output 0 or none when firm is non-active? 

from sust_inv_code.src.data_structures import ModelParams, FirmType, InvestorType
from sust_inv_code.src.data_structures import EquilibriumAllocationOnly, EquilibriumAllocationTransformation
from sust_inv_code.src.equilibrium import solve_equilibrium
from sust_inv_code.src.tests import check_eqm
from sust_inv_code.src.results import compute_results

def run_model(params: ModelParams):
    print("Starting model run.")
    EqmAlloc, EqmTransform = solve_equilibrium(params)
    is_competitive_eqm = check_eqm(EqmAlloc, params)
    if not is_competitive_eqm:
        raise ValueError("Equilibrium conditions not satisfied for allocation only.")
    else:
        print("Equilibrium conditions satisfied for allocation only.")
        results_allocation_only = compute_results(EqmAlloc, params)
    is_competitive_eqm = check_eqm(EqmTransform, params)
    if not is_competitive_eqm:
        raise ValueError("Equilibrium conditions not satisfied for transformation")
    else:
        print("Equilibrium conditions satisfied for allocation transformation")
        results_allocation_transformation = compute_results(EqmTransform, params)
    print("Model run complete.")
    return results_allocation_only, results_allocation_transformation

if __name__ == "__main__":
    corner_ob_params = ModelParams(Ig=30, In=30, Is=30, K=0.9, T=0.5, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                        sigma_c=1.0, sigma_d=1.0, sigma_cd=0.0,
                        Nc=50, Nd=50)
    
    options_params = ModelParams(Ig=30, In=30, Is=100, K=0.5, T=0.3, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                        sigma_c=1.0, sigma_d=1.0, sigma_cd=0.0,
                        Nc=100, Nd=50)


    interior_ob_params = ModelParams(Ig=30, In=30, Is=30, K=1.0, T=0.8, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                        sigma_c=1.0, sigma_d=1.0, sigma_cd=0.0,
                        Nc=50, Nd=50)
    
    zero_price_params = ModelParams(Ig=30, In=30, Is=30, K=0.5, T=0.3, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                    sigma_c=1.0, sigma_d=1.0, sigma_cd=0.0,
                    Nc=100, Nd=50)
        
    results_allocation, results_transformation = run_model(zero_price_params)
    # results_allocation, results_transformation = run_model(interior_ob_params)
    # results_allocation, results_transformation = run_model(corner_ob_params)

    # Pairwise Report
    print("-----------------------------------------")
    print("Market for Real Asset Allocation Only")
    print("Risk Adjusted Welfare: " + str(results_allocation.risk_adjusted_welfare))
    print("Reformed Assets: " + str(results_allocation.reformed_assets))
    print("Secondary Traded Assets: " + str(results_allocation.secondary_trading))
    print("Total Market Cap: " + str(results_allocation.market_capitalization))
    print("-----------------------------------------")
    print("Market for Real Asset Allocation and Transformation")
    print("Risk Adjusted Welfare: " + str(results_transformation.risk_adjusted_welfare))
    print("Reformed Assets: " + str(results_transformation.reformed_assets))
    print("Secondary Traded Assets: " + str(results_transformation.secondary_trading))
    print("Total Market Cap: " + str(results_transformation.market_capitalization))
    print("-----------------------------------------")
    print("Comparative Statics:")
    print("Welfare Improvement: " + str(
        (results_transformation.risk_adjusted_welfare - results_allocation.risk_adjusted_welfare)/results_allocation.risk_adjusted_welfare
        ))
    print("Increase in Reformed Assets: " + str(
        (results_transformation.reformed_assets - results_allocation.reformed_assets)/results_allocation.reformed_assets
        ))
    print("Increase in Secondary Traded Assets: " + str(
        (results_transformation.secondary_trading - results_allocation.secondary_trading)/results_allocation.secondary_trading
        ))
    print("Increase in Total Market Cap: " + str(
        (results_transformation.market_capitalization - results_allocation.market_capitalization)/results_allocation.market_capitalization
        ))
    print("-----------------------------------------")







