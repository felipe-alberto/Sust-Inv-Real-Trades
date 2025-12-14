# src/tests.py

import math

EQM_REL_TOL = 1e-9
EQM_ABS_TOL = 1e-12
QTY_TOL = 1e-8

def check_equilibrium(outcome, params):
    
    # Firm corporate choice clearing 
    assert abs(outcome.NU + outcome.NR + outcome.NS - params.Nd) < QTY_TOL, \
        "D-Firm corporate choice does not clear"
    assert abs(outcome.NA - params.Nc) < QTY_TOL, \
        "C-Firm corporate choice does not clear"
    
    # No entry conditions
    assert math.isclose(
        outcome.PR - outcome.PU, params.K,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in reform share price does not equal reform cost"
    assert math.isclose(
        outcome.PS - outcome.PU, params.T,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Diff in secondary trading share price does not equal transaction cost"
    
    # Investor allocation clearing
    assert math.isclose(
    outcome.xnU * params.In, outcome.NU, 
    rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL 
    ), "Unreformed firms investor allocation does not clear"
    assert math.isclose(
    outcome.xnA * params.In + outcome.xgA * params.Ig, outcome.NA,
    rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Acceptable firms investor allocation does not clear"
    assert math.isclose(
    outcome.xgS * params.Ig, outcome.NS,
    rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Secondary trading firms investor allocation does not clear"
    assert math.isclose(
        outcome.xsR * params.Is, outcome.NR,
        rel_tol=EQM_REL_TOL, abs_tol=EQM_ABS_TOL
    ), "Reformed firms investor allocation does not clear"

    return True