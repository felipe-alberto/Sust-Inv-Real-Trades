# src/tests.py

import math
from sust_inv_code.src.types import FirmType, InvestorType

EQM_REL_TOL = 1e-9
EQM_ABS_TOL = 1e-12
QTY_TOL = 1e-8

def investor_population(investor: InvestorType, params) -> float:
    return {
        InvestorType.g: params.Ig,
        InvestorType.n: params.In,
        InvestorType.s: params.Is,
    }[investor]

def investor_market_clearing_for_firm(firm, eqm, params):
    return sum(
        investor_population(i, params) * eqm.X[i].get(firm, 0.0)
        for i, firm_set in eqm.active_links.items()
        if firm in firm_set
    )

def check_eqm_allocation_only(equilibrium_allocation_only, params):

    eqm, p = equilibrium_allocation_only, params
    # Firm corporate choice clearing 
    assert abs(eqm.NU + eqm.NR + eqm.NS - p.Nd) < QTY_TOL, \
        "D-Firm corporate choice does not clear"
    assert abs(eqm.NA - p.Nc) < QTY_TOL, \
        "C-Firm corporate choice does not clear"
    # No entry conditions
    assert math.isclose(
        eqm.PR - eqm.PU, p.K,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in reform share price does not equal reform cost"
    assert math.isclose(
        eqm.PS - eqm.PU, p.T,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in secondary trading share price does not equal transaction cost"
    # Investor allocation clearing
    assert math.isclose(
    eqm.xnU * p.In, eqm.NU, 
    rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL 
    ), "Unreformed firms investor allocation does not clear"
    assert math.isclose(
    eqm.xnA * p.In + eqm.xgA * p.Ig, eqm.NA,
    rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Acceptable firms investor allocation does not clear"
    assert math.isclose(
    eqm.xgS * p.Ig, eqm.NS,
    rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Secondary trading firms investor allocation does not clear"
    assert math.isclose(
        eqm.xsR * params.Is, eqm.NR,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Reformed firms investor allocation does not clear"
    return True

def check_eqm_corner_ob_trading(eqm_corner_ob_trading, params):
    eqm, p = eqm_corner_ob_trading, params
    # Firm corporate choice clearing 
    assert abs(eqm.NU + eqm.NR + eqm.NS + eqm.NUprime - p.Nd) < QTY_TOL, \
        "D-Firm corporate choice does not clear"
    assert abs(eqm.NA + eqm.NAprime - p.Nc) < QTY_TOL, \
        "C-Firm corporate choice does not clear"
    # No entry conditions
    assert math.isclose(
        eqm.PR - eqm.PU, p.K,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in reform share price does not equal reform cost"
    assert math.isclose(
        eqm.PS - eqm.PU, p.T,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in secondary trading share price does not equal transaction cost"
    assert math.isclose(
        eqm.PUprime - eqm.PU, p.T,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in obs-seller reformed share price does not equal transaction cost"
    assert math.isclose(
        eqm.PAprime, eqm.PA + (p.K - p.T),
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in Obligation Buyer Share Price Does Not Equal K - T"
    # Investor allocation clearing
    assert math.isclose(
    eqm.xnU * p.In, eqm.NU, 
    rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL 
    ), "Unreformed firms investor allocation does not clear"
    assert math.isclose(
    eqm.xnA * p.In + eqm.xgA * p.Ig, eqm.NA,
    rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Acceptable firms investor allocation does not clear"
    assert math.isclose(
    eqm.xgS * p.Ig, eqm.NS,
    rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Green firms investor allocation does not clear 1"
    assert math.isclose(
    eqm.xgUprime * p.Ig, eqm.NUprime,
    rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Green firms investor allocation does not clear 2"
    assert math.isclose(
        eqm.xsR * params.Is, eqm.NR,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Reformed firms investor allocation does not clear"
    assert math.isclose(
        eqm.xsAprime * params.Is, eqm.NAprime,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Obs-buyer firms investor allocation does not clear"
    return True

def no_entry_corner_obs_trading(NewEqm, params):
    eqm, p = NewEqm, params
    assert math.isclose(
        eqm.P[FirmType.R] - eqm.P[FirmType.U], p.K,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in reform share price does not equal reform cost"
    assert math.isclose(
        eqm.P[FirmType.S] - eqm.P[FirmType.U], p.T,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in secondary trading share price does not equal transaction cost"
    assert math.isclose(
        eqm.P[FirmType.Uprime] - eqm.P[FirmType.U], p.T,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in obs-seller reformed share price does not equal transaction cost"
    assert math.isclose(
        eqm.P[FirmType.Aprime], eqm.P[FirmType.A] + (p.K - p.T),
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in Obligation Buyer Share Price Does Not Equal K - T"


def no_entry_allocation_only(NewEqm, params):
    e, p = NewEqm, params
    assert math.isclose(
        e.P[FirmType.R] - e.P[FirmType.U], p.K,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in reform share price does not equal reform cost"
    assert math.isclose(
        e.P[FirmType.S] - e.P[FirmType.U], p.T,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in secondary trading share price does not equal transaction cost"


def check_eqm_v2(NewEqm, params):
    e, p = NewEqm, params

    # 1. Firm corporate choice clearing 
    d_firms = sum(e.N[f]
                    for f in {FirmType.U, FirmType.R, FirmType.S, FirmType.Uprime}
                        if f in e.active_firms)
    assert abs(d_firms- p.Nd) < QTY_TOL, \
        "D-Firm corporate choice does not clear"
    c_firms = sum(e.N[f]
                    for f in {FirmType.A, FirmType.Aprime}
                        if f in e.active_firms)
    assert abs(c_firms - p.Nc) < QTY_TOL, \
        "C-Firm corporate choice does not clear"
    
    # 2. No entry conditions
    if e.regime == "transformation_corner_obs_trading":
        no_entry_corner_obs_trading(NewEqm, params)
    if e.regime == "allocation_only":
        no_entry_allocation_only(NewEqm, params)

    # 3. Investor allocation clearing
    for f in e.active_firms:
        investor_demand = investor_market_clearing_for_firm(f, e, params)
        assert math.isclose(
            investor_demand,
            e.N[f],
            rel_tol=EQM_REL_TOL,
            abs_tol=EQM_ABS_TOL,
        ), f"{f.value} firms investor allocation does not clear - LOOP"
    
    # 4. If has reform exchange, check clearing
    if e.regime == "transformation_corner_obs_trading":
        assert math.isclose(
            e.N[FirmType.Uprime],
            e.N[FirmType.Aprime],
            rel_tol=EQM_REL_TOL,
            abs_tol=EQM_ABS_TOL,
        ), "Reform action market does not clear"

    return True
