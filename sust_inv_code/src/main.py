
# src/main.py
# TODO: Refactor allocation-only equilibrium into unified Equilibrium container.

from sust_inv_code.src.data_structures import ModelParams
from sust_inv_code.src.equilibrium import solve_equilibrium
from sust_inv_code.src.tests import check_eqm_allocation_only, check_eqm_corner_ob_trading, check_eqm_allocation_only_v2
from sust_inv_code.src.results import compute_results
from sust_inv_code.src.data_structures import FirmType, InvestorType
from sust_inv_code.src.equilibrium_state import EquilibriumAllocationOnly

PrintBool = True

def run_model(params: ModelParams):
    
    eqm_allocation_only, eqm_corner_ob_trading = solve_equilibrium(params)

    # Thin wrapper for smoke test
    e = eqm_allocation_only
    N = {
        FirmType.A: e.NA,
        FirmType.U: e.NU,
        FirmType.R: e.NR,
        FirmType.S: e.NS
    }

    P = {
        FirmType.A: e.PA,
        FirmType.U: e.PU,
        FirmType.R: e.PR,
        FirmType.S: e.PS,
    }

    X = {
        InvestorType.n: {
            FirmType.A: e.xnA,
            FirmType.U: e.xnU,
        },
        InvestorType.g: {
            FirmType.A: e.xgA,
            FirmType.S: e.xgS,
        },
        InvestorType.s: {
            FirmType.R: e.xsR,
        },
    }

    NewEqm = EquilibriumAllocationOnly(
        N=N,
        P=P,
        X=X,
        active_firms={FirmType.A, FirmType.U, FirmType.R, FirmType.S},
        active_links={
            InvestorType.n: {FirmType.A, FirmType.U},
            InvestorType.g: {FirmType.A, FirmType.S},
            InvestorType.s: {FirmType.R},
        },
        regime="allocation_only",
    )
    
    # Check Allocation Only Equilibrium
    is_competitive_eqm = check_eqm_allocation_only(eqm_allocation_only, params)
    if not is_competitive_eqm:
        raise ValueError("Equilibrium conditions not satisfied")
    else:
        print("Equilibrium conditions satisfied for allocation only - OLD OBJECT!")
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
    
    # Smoke Screen for New Allocation Equilibrium Object
    is_competitive_eqm = check_eqm_allocation_only_v2(NewEqm, params)
    if not is_competitive_eqm:
        raise ValueError("Equilibrium conditions not satisfied for NEW OBJECT")
    else:
        print("Equilibrium conditions satisfied for allocation only - NEW OBJECT!")

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





