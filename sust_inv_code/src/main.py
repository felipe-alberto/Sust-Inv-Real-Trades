
# src/main.py
# TODO: Refactor allocation-only equilibrium into unified Equilibrium container.

from sust_inv_code.src.data_structures import ModelParams
from sust_inv_code.src.equilibrium import solve_equilibrium
from sust_inv_code.src.tests import check_eqm_allocation_only, check_eqm_corner_ob_trading, check_eqm_v2
from sust_inv_code.src.results import compute_results
from sust_inv_code.src.data_structures import FirmType, InvestorType
from sust_inv_code.src.equilibrium_state import EquilibriumAllocationOnly, EquilibriumAllocationTransformation

PrintBool = False

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

    NewEqmAlloc = EquilibriumAllocationOnly(
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
    
    e = eqm_corner_ob_trading
    N = {
        FirmType.A: e.NA,
        FirmType.Aprime: e.NAprime,
        FirmType.U: e.NU,
        FirmType.R: e.NR,
        FirmType.S: e.NS,
        FirmType.Uprime: e.NUprime,
    }
    P = {
        FirmType.A: e.PA,
        FirmType.Aprime:e.PAprime,
        FirmType.U: e.PU,
        FirmType.R: e.PR,
        FirmType.S: e.PS,
        FirmType.Uprime: e.PUprime,
    }

    X = {
        InvestorType.n: {
            FirmType.A: e.xnA,
            FirmType.U: e.xnU,
        },
        InvestorType.g: {
            FirmType.A: e.xgA,
            FirmType.S: e.xgS,
            FirmType.Uprime: e.xgUprime,
        },
        InvestorType.s: {
            FirmType.Aprime: e.xsAprime,
            FirmType.R: e.xsR,
        },
    }
    NewEqmTransform = EquilibriumAllocationTransformation(
        N=N,
        P=P,
        X=X,
        pi=e.pi,
        active_firms={FirmType.A, FirmType.Aprime, FirmType.U, FirmType.R, FirmType.S, FirmType.Uprime},
        active_links={
            InvestorType.n: {FirmType.A, FirmType.U},
            InvestorType.g: {FirmType.A, FirmType.S, FirmType.Uprime},
            InvestorType.s: {FirmType.Aprime, FirmType.R},
        },
        regime="transformation_corner_obs_trading",
    )
    
    # Check Allocation Only Equilibrium
    is_competitive_eqm = check_eqm_allocation_only(eqm_allocation_only, params)
    if not is_competitive_eqm:
        raise ValueError("Equilibrium conditions not satisfied")
    else:
        print("Equilibrium conditions satisfied for allocation only - OLD OBJECT!")
        results_allocation_only = compute_results(eqm_allocation_only, params)
    
    # Check Corner OB Trading Equilibrium
    is_competitive_eqm = check_eqm_corner_ob_trading(eqm_corner_ob_trading, params)
    if not is_competitive_eqm:
        raise ValueError("Equilibrium conditions not satisfied")
    else:
        print("Equilibrium conditions satisfied for corner OB trading - OLD OBJECT!")
    
    # Smoke Screen for New Allocation Equilibrium Object
    is_competitive_eqm = check_eqm_v2(NewEqmAlloc, params)
    if not is_competitive_eqm:
        raise ValueError("Equilibrium conditions not satisfied for NEW OBJECT")
    else:
        print("Equilibrium conditions satisfied for allocation only - NEW OBJECT!")

    # Smoke Screen for New Allocation Equilibrium Object
    is_competitive_eqm = check_eqm_v2(NewEqmTransform, params)
    if not is_competitive_eqm:
        raise ValueError("Equilibrium conditions not satisfied for NEW OBJECT")
    else:
        print("Equilibrium conditions satisfied for allocation only - NEW OBJECT!")

    return results_allocation_only

if __name__ == "__main__":
    params = ModelParams(Ig=30, In=30, Is=30, K=0.9, T=0.5, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                        sigma_c=1.0, sigma_d=1.0, sigma_cd=0.0,
                        Nc=50, Nd=50)
    results = run_model(params)





