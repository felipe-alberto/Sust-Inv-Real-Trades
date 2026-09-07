# RECENT:
    # Split equilibrium solve into two functions but kept thin wrapper for upper routines.

# TODO:
    # - Carrying over from exp_baseline, focus on reporting structure for now.
    # - Nomenclature still bugging me. Case consistency etc. 
        # - Improved some nomenclature on allocation_only_corporate_choices. See if worth doing same for other functions.
    # - Consider whether the thin wrapper for equilibrium solve should be fully removed. 
    # - Consider whether equilibrium equations should be a different module for clarity.

# Project: Sustainable Investing Strategies For Real Asset Trades: Incentives to Own and Transform Pollutive Assets
# Author: Felipe Verastegui, PhD IEOR Columbia University
# Last Update: September 2026

# Equilibrium Computation

# ----- Imports ---------------------------------------------------------------

from sust_inv_code.src.data_structures import ModelParams
from sust_inv_code.src.data_structures import FirmType, InvestorType
from sust_inv_code.src.data_structures import EquilibriumAllocationOnly, EquilibriumAllocationTransformation

# ----- Subfunctions ---------------------------------------------------------

PrintBool = True

def detect_regime(params: ModelParams, pi_op: float, pi_ob: float):
    if pi_ob < 0 or pi_op > 0:
        print("Diagnosing Instance...")
        if pi_ob< 0:
            if pi_ob >= - params.T:
                print("(Interior) Obligations Trading Instance Detected")
                return "transformation_interior_obligations_trading"
            elif pi_ob < - params.T:
                print("(Corner) Obligations Trading Instance Detected")
                return("transformation_corner_obligations_trading")
        elif pi_op > 0:
            print("Options Trading Instance Detected")
            return("transformation_options_trading")
    else:
        print("Undiagnosed Instance Detected")
        print("pi_op: ", pi_op)
        print("pi_ob: ", pi_ob)
        return "transformation_undiagnosed"

# ----- Equilibrium Structure ---------------------------------------------------------

from sust_inv_code.src.equilibrium_structure import allocation_only_corporate_choices
from sust_inv_code.src.equilibrium_structure import allocation_only_share_prices
from sust_inv_code.src.equilibrium_structure import allocation_only_investor_positions

from sust_inv_code.src.equilibrium_structure import reform_exchange_compute_pi

from sust_inv_code.src.equilibrium_structure import corner_ob_trading_corporate_choices
from sust_inv_code.src.equilibrium_structure import corner_ob_trading_share_prices
from sust_inv_code.src.equilibrium_structure import corner_ob_trading_investor_positions

from sust_inv_code.src.equilibrium_structure import interior_ob_trading_corporate_choices
from sust_inv_code.src.equilibrium_structure import interior_ob_trading_share_prices
from sust_inv_code.src.equilibrium_structure import interior_ob_trading_investor_positions

from sust_inv_code.src.equilibrium_structure import options_trading_corporate_choices
from sust_inv_code.src.equilibrium_structure import options_trading_share_prices
from sust_inv_code.src.equilibrium_structure import options_trading_investor_positions

from sust_inv_code.src.equilibrium_structure import zero_price_corporate_choices
from sust_inv_code.src.equilibrium_structure import zero_price_share_prices
from sust_inv_code.src.equilibrium_structure import zero_price_investor_positions

# ----- Main solver ---------------------------------------------------------

def solve_equilibrium(params: ModelParams) -> tuple[EquilibriumAllocationOnly, EquilibriumAllocationTransformation]:

    EqmAlloc = solve_allocation_only_equilibrium(params)
    EqmTransform = solve_allocation_transformation_equilibrium(params)

    return EqmAlloc, EqmTransform

def solve_allocation_only_equilibrium(params: ModelParams) -> EquilibriumAllocationOnly: 
    
    N = allocation_only_corporate_choices(params)
    P = allocation_only_share_prices(params)
    X = allocation_only_investor_positions(params)

    active_firms_allocation_only = {FirmType.A, FirmType.U, FirmType.R, FirmType.S}
    active_links_allocation_only = {
                                    InvestorType.n: {FirmType.A, FirmType.U},
                                    InvestorType.g: {FirmType.A, FirmType.S},
                                    InvestorType.s: {FirmType.R},
    }   
    EqmAlloc = EquilibriumAllocationOnly(
        N=N,
        P=P,
        X=X,
        active_firms=active_firms_allocation_only,
        active_links=active_links_allocation_only,
        regime="allocation_only",
    )
    return EqmAlloc 

def solve_allocation_transformation_equilibrium(params: ModelParams) -> EquilibriumAllocationTransformation:
    pi_op, pi_ob = reform_exchange_compute_pi(params)
    regime = detect_regime(params, pi_op, pi_ob)
    if regime == "transformation_corner_obligations_trading":
        EquilibriumAllocationTransformation = solve_corner_obligations_equilibrium(params, pi_ob)
    elif regime == "transformation_interior_obligations_trading":
        EquilibriumAllocationTransformation = solve_interior_obligations_equilibrium(params, pi_ob)
    elif regime == "transformation_options_trading":
        EquilibriumAllocationTransformation = solve_options_trading_equilibrium(params, pi_op)
    elif regime == "transformation_undiagnosed":
        EquilibriumAllocationTransformation = solve_zero_price_equilibrium(params)
    return EquilibriumAllocationTransformation

# ----- Solver Helpers ---------------------------------------------------------

# def build_allocation_only_equilibrium(N, P, X):

def solve_corner_obligations_equilibrium(params: ModelParams, pi_ob: float) -> EquilibriumAllocationTransformation:
    regime = "transformation_corner_obligations_trading"
    pi = pi_ob
    N = corner_ob_trading_corporate_choices(params)
    P = corner_ob_trading_share_prices(params)
    X = corner_ob_trading_investor_positions(params)
    active_firms = {FirmType.A, 
                    FirmType.Aprime, 
                    FirmType.U, 
                    FirmType.R, 
                    FirmType.S, 
                    FirmType.Uprime}
    active_links = {
            InvestorType.n: {FirmType.A, FirmType.U},
            InvestorType.g: {FirmType.A, FirmType.S, FirmType.Uprime},
            InvestorType.s: {FirmType.Aprime, FirmType.R},
    }
    EqmTransform = EquilibriumAllocationTransformation(
    N=N,
    P=P,
    X=X,
    pi=pi,
    active_firms=active_firms,
    active_links=active_links,
    regime=regime
    )
    return EqmTransform

def solve_interior_obligations_equilibrium(params: ModelParams, pi_ob: float) -> EquilibriumAllocationTransformation:
    regime = "transformation_interior_obligations_trading"
    pi = pi_ob
    N = interior_ob_trading_corporate_choices(params, pi_ob)
    P = interior_ob_trading_share_prices(params, pi_ob)
    X = interior_ob_trading_investor_positions(params, pi_ob)
    active_firms = {FirmType.A, 
                    FirmType.Aprime, 
                    FirmType.U, 
                    FirmType.R, 
                    FirmType.Uprime}
    active_links = {
            InvestorType.n: {FirmType.A, FirmType.U},
            InvestorType.g: {FirmType.A, FirmType.Uprime},
            InvestorType.s: {FirmType.Aprime, FirmType.R},
        }
    EqmTransform = EquilibriumAllocationTransformation(
    N=N,
    P=P,
    X=X,
    pi=pi,
    active_firms=active_firms,
    active_links=active_links,
    regime=regime
    )
    return EqmTransform

def solve_options_trading_equilibrium(params: ModelParams, pi_op: float) -> EquilibriumAllocationTransformation:
    regime = "transformation_options_trading"
    pi = pi_op
    N = options_trading_corporate_choices(params, pi_op)
    P = options_trading_share_prices(params, pi_op)
    X = options_trading_investor_positions(params, pi_op)
    active_firms = {FirmType.A,
                    FirmType.Aprime, 
                    FirmType.R, 
                    FirmType.Uprime}
    active_links = {
            InvestorType.n: {FirmType.A, FirmType.Uprime},
            InvestorType.g: {FirmType.A, FirmType.Uprime},
            InvestorType.s: {FirmType.Aprime, FirmType.R},
        }
    EqmTransform = EquilibriumAllocationTransformation(
        N = N,
        P = P,
        X = X,
        pi = pi,
        regime = regime,
        active_firms = active_firms,
        active_links = active_links
    )
    return EqmTransform
    

def solve_zero_price_equilibrium(params: ModelParams) -> EquilibriumAllocationTransformation:
    regime = "transformation_zero_price"
    pi = 0.0 
    N = zero_price_corporate_choices(params)
    P = zero_price_share_prices(params)
    X = zero_price_investor_positions(params)
    active_firms = {FirmType.A,
                    FirmType.Aprime,
                    FirmType.R,
                    FirmType.Uprime,
                    FirmType.U}
    active_links = {
            InvestorType.n: {FirmType.A, FirmType.Uprime, FirmType.U},
            InvestorType.g: {FirmType.A, FirmType.Uprime},
            InvestorType.s: {FirmType.Aprime, FirmType.R},
        }

    EqmTransform = EquilibriumAllocationTransformation(
        N = N,
        P = P,
        X = X,
        pi = pi,
        regime = regime,
        active_firms = active_firms,
        active_links = active_links
        )
    return EqmTransform

    