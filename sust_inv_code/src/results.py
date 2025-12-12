from sust_inv_code.src.data_structures import ModelParams, EquilibriumOutcome, ModelResults

def compute_results(outcome, params):
    
    reformed_assets = outcome.NR
    secondary_trading = outcome.NS

    return ModelResults(
        risk_adjusted_welfare=0,
        reformed_assets=reformed_assets,
        secondary_trading=secondary_trading,
        market_capitalization=0
        )