
def check_equilibrium(outcome, params):
    assert abs(outcome.NU + outcome.NR + outcome.NS - params.Nd) < 1e-8
    assert abs(outcome.NA - params.Nc) < 1e-8
    return True

