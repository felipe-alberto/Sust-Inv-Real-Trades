
# src/main.py
# TODO: Refactor allocation-only equilibrium into unified Equilibrium container.

from sust_inv_code.src.data_structures import ModelParams
from sust_inv_code.src.equilibrium import solve_equilibrium
from sust_inv_code.src.tests import check_eqm
from sust_inv_code.src.results import compute_results
from sust_inv_code.src.data_structures import FirmType, InvestorType
from sust_inv_code.src.equilibrium_state import EquilibriumAllocationOnly, EquilibriumAllocationTransformation

PrintBool = False

def run_model(params: ModelParams):
    
    EqmAlloc, EqmTransform = solve_equilibrium(params)
    
    # Smoke Screen for New Allocation Equilibrium Object
    is_competitive_eqm = check_eqm(EqmAlloc, params)
    if not is_competitive_eqm:
        raise ValueError("Equilibrium conditions not satisfied for NEW OBJECT")
    else:
        print("Equilibrium conditions satisfied for allocation only")
        results_allocation_only = compute_results(EqmAlloc, params)
        print("Risk Adjusted Welfare: " + str(results_allocation_only.risk_adjusted_welfare))
        print("Reformed Assets: " + str(results_allocation_only.reformed_assets))
        print("Secondary Traded Assets: " + str(results_allocation_only.secondary_trading))
        print("Total Market Cap: " + str(results_allocation_only.market_capitalization))

    # Smoke Screen for New Allocation Equilibrium Object
    is_competitive_eqm = check_eqm(EqmTransform, params)
    if not is_competitive_eqm:
        raise ValueError("Equilibrium conditions not satisfied for NEW OBJECT")
    else:
        print("Equilibrium conditions satisfied for allocation transformation")
        results_allocation_transformation = compute_results(EqmTransform, params)
        print("Risk Adjusted Welfare: " + str(results_allocation_transformation.risk_adjusted_welfare))
        print("Reformed Assets: " + str(results_allocation_transformation.reformed_assets))
        print("Secondary Traded Assets: " + str(results_allocation_transformation.secondary_trading))
        print("Total Market Cap: " + str(results_allocation_transformation.market_capitalization))
    return results_allocation_only, results_allocation_transformation

if __name__ == "__main__":
    params = ModelParams(Ig=30, In=30, Is=30, K=0.9, T=0.5, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                        sigma_c=1.0, sigma_d=1.0, sigma_cd=0.0,
                        Nc=50, Nd=50)
    results = run_model(params)





