# src/tests.py

import math

EQM_REL_TOL = 1e-9
EQM_ABS_TOL = 1e-12
QTY_TOL = 1e-8

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
    print("FLAG")
    print(eqm.PAprime, eqm.PA, p.K, p.T)
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
    eqm.xgG * p.Ig, eqm.NS + eqm.NUprime,
    rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Green firms investor allocation does not clear"
    assert math.isclose(
        eqm.xsR * params.Is, eqm.NR,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Reformed firms investor allocation does not clear"
    assert math.isclose(
        eqm.xsAprime * params.Is, eqm.NAprime,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Obs-buyer firms investor allocation does not clear"
    return True