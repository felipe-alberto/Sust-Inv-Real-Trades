# TODO:
# 1. Clean the structure of this code so we can do more dev.
# 1.1 Check the current execution path while focusing on reporting routines. 
#   # NOTE: Some of the results included in this routine are:
        # - Total Surplus 
        # - Firm Surplus 
        # - Investor Surplus 
        # - Net Investor Surplus (revise and compare with prev.)
        # - Investor Surplus Dict (check dimensionality)
        # - Investor Transfers (check dimensionality)
            # NOTE: Other commented results (need to check consistency across different scenarios)
                # - Reformed Real Assets
                # - Secondary Traded Assets
                # - Total Market Capitalization
                # - Risk-Adjusted Return
                # - Normalized Risk-Adjusted Welfare
                # - Investor Welfare by Type
                # - Firm Market Capitalization
                # - Clean Market Capitalization
                # - Dirty Market Capitalization
                # - Firm Net Value
                # - Net Market Capitalization
    # NOTE: For all instances of the model we are solving (i) alloc and (ii) transform.
        # - I am sure there is a better nomenclature for this. 
# 2. Develop a module for policy equilibria (carbon-tax, ETS, etc.) and compare with baseline.
# 3. Change the variable names to reflect the new paper notation. 
# 4. Still using "IS_values" should be "IM_values". 

# experiments/exp_baseline.py

from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import replace

if __package__ in (None, ""):
    # Allow running this file directly: python sust_inv_code/experiments/exp_baseline.py run
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sust_inv_code.src.main import run_model
from sust_inv_code.src.data_structures import ModelParams, FirmType, InvestorType

# Data 

corner_ob_params = ModelParams(Iv=30, In=30, Im=30, K=0.9, T=0.5, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                    sigma_c=1.0, sigma_d=1.0, sigma_cd=0.0,
                    Nc=50, Nd=50)

interior_ob_params = ModelParams(Iv=30, In=30, Im=30, K=1.0, T=0.8, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                    sigma_c=1.0, sigma_d=1.0, sigma_cd=0.025,
                    Nc=50, Nd=25)
    
options_params = ModelParams(Iv=30, In=30, Im=100, K=0.5, T=0.3, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                        sigma_c=1.0, sigma_d=1.0, sigma_cd=0.05,
                        Nc=100, Nd=50)

zero_price_params = ModelParams(Iv=30, In=30, Im=30, K=0.5, T=0.3, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                    sigma_c=1.0, sigma_d=1.0, sigma_cd=0.0,
                    Nc=100, Nd=50)

base = options_params
Im_values = np.linspace(100, 150, 100)
# Im_values = np.linspace(30, 60, 100)

# This experiment iterates over Is_values. 
# Currently migrating to single DataFrame. Each row will represent a different
# Is value x regime. So, a unique result ID corresponds to a model (allocation or transformation)
# at a given Is value, could also do metric so that it's a long-form DataFrame. 
# I like that, let's do Is x Regime x Metric. I will begin with the following metrics:
# Total Surplus, Firm Surplus, Investor Surplus. 

def build_allocation_metrics(results_allocation):
    a = results_allocation
    return [
        ("Total Surplus", a.total_surplus),
        ("Firm Surplus", a.firm_surplus),
        ("Investor Surplus", a.investor_surplus),
    ]

def build_allocation_metrics_by_investor(results_allocation):
    a = results_allocation
    return [
        ("Investor Surplus", a.investor_surplus_dict),
        ("Investor Transfers", a.investor_transfers)
    ]

def build_transformation_metrics(results_transformation):
    t = results_transformation
    return [
        ("Total Surplus", t.total_surplus),
        ("Firm Surplus", t.firm_surplus),
        ("Investor Surplus", t.investor_surplus),
    ]

def build_transformation_metrics_by_investor(results_transformation):
    t = results_transformation
    return [
    ("Investor Surplus", t.investor_surplus_dict),
    ("Investor Transfers", t.investor_transfers)
    ]


def run_consistency_checks(results_allocation, results_transformation):
    
    # Need to understand what these tests were doing and why are they here.
    # Going over the logic now. We can potentially reconstruct, but looks like
    # it should be a separate function. 
     
    import math

    # This first test computes wheter the difference in investor surplus across the two model runs
    # is indeed consistent with the difference in risk_adjusted_return - market_cap, which is a decomposition
    # of investor surplus. Thus, this is a consistency test. For replication, we need to rebuild the 
    # numbers but I think we can pull them directly from the results object without messing with the 
    # results DataFrame. 
    assert math.isclose(
        results_transformation.investor_surplus - results_allocation.investor_surplus,
        (results_transformation.risk_adjusted_return - results_transformation.market_capitalization) 
        - (results_allocation.risk_adjusted_return - results_allocation.market_capitalization),
        rel_tol=1e-9,
        abs_tol=1e-12,
    ), "Investor Surplus does not equal Risk Adjusted Welfare minus Market Capitalization difference"

    assert math.isclose(
        results_allocation.market_capitalization,
        results_allocation.investor_transfers[InvestorType.n] 
        + results_allocation.investor_transfers[InvestorType.g] 
        + results_allocation.investor_transfers[InvestorType.s],
        rel_tol=1e-9,
        abs_tol=1e-12,
    ), "Allocation Only: Market capitalization does not equal total investor transfers"

    assert math.isclose(
        results_transformation.market_capitalization,
        results_transformation.investor_transfers[InvestorType.n] 
        + results_transformation.investor_transfers[InvestorType.g] 
        + results_transformation.investor_transfers[InvestorType.s],
        rel_tol=1e-9,
        abs_tol=1e-12,
    ), "+ Transformation: Market capitalization does not equal total investor transfers"

results_rows = []
for m in Im_values:

    params = replace(base, Im=m)
    eqm_alloc, eqm_transform, results_allocation, results_transformation = run_model(params)

    allocation_metrics = build_allocation_metrics(results_allocation)
    for metric_name, metric_value in allocation_metrics:
        results_rows.append({
            "Iter":m, 
            "Model":"Allocation Only", 
            "Metric": metric_name,
            "Metric Level": "Aggregate",
            "Entity Kind": "None",
            "Entity ID": "None",
            "Value": metric_value,
            })

    allocation_metrics_by_investor = build_allocation_metrics_by_investor(results_allocation)
    for metric_name, metric_dict in allocation_metrics_by_investor:
        for investor_type, value in metric_dict.items():
            results_rows.append({
                "Iter":m, 
                "Model":"Allocation Only", 
                "Metric": metric_name,
                "Metric Level": "By Investor",
                "Entity Kind": "Investor",
                "Entity ID": investor_type.name,
                "Value": value,
            })

    transformation_metrics = build_transformation_metrics(results_transformation)
    for metric_name, metric_value in transformation_metrics:
        results_rows.append({
            "Iter":m, 
            "Model":"+Transformation", 
            "Metric": metric_name,
            "Metric Level": "Aggregate",
            "Entity Kind": "None",
            "Entity ID": "None",
            "Value": metric_value})

    transformation_metrics_by_investor = build_transformation_metrics_by_investor(results_transformation)
    for metric_name, metric_dict in transformation_metrics_by_investor:
        for investor_type, value in metric_dict.items():
            results_rows.append({
                "Iter":m, 
                "Model":"+Transformation", 
                "Metric": metric_name,
                "Metric Level": "By Investor",
                "Entity Kind": "Investor",
                "Entity ID": investor_type.name,
                "Value": value,
            })
        
    # allocation_total_surplus.append(results_allocation.total_surplus)
    # allocation_firm_surplus.append(results_allocation.firm_surplus)
    # allocation_investor_surplus.append(results_allocation.investor_surplus)
    # allocation_net_investor_surplus.append(results_allocation.investor_surplus/params.I)
    # allocation_investor_surplus_dict.append(results_allocation.investor_surplus_dict)
    # allocation_investor_transfers.append(results_allocation.investor_transfers)
    
    # t_total_surplus.append(results_transformation.total_surplus)
    # t_firm_surplus.append(results_transformation.firm_surplus)
    # t_investor_surplus.append(results_transformation.investor_surplus)
    # t_net_investor_surplus.append(results_transformation.investor_surplus/params.I)
    # t_investor_surplus_dict.append(results_transformation.investor_surplus_dict)
    # t_investor_transfers.append(results_transformation.investor_transfers)

    """
    a_reformed_real_assets.append(results_allocation.reformed_assets)
    a_secondary_traded_assets.append(results_allocation.secondary_trading)
    a_total_market_capitalization.append(results_allocation.market_capitalization)
    a_risk_adjusted_return.append(results_allocation.risk_adjusted_return)
    a_normalized_risk_adjusted_welfare.append(results_allocation.risk_adjusted_return / (params.I))
    a_n_welfare.append(results_allocation.investor_risk_adjusted[InvestorType.n])
    a_g_welfare.append(results_allocation.investor_risk_adjusted[InvestorType.g])
    a_s_welfare.append(results_allocation.investor_risk_adjusted[InvestorType.s])
    a_firm_market_cap.append(results_allocation.firm_market_cap)
    a_clean_market_cap.append(results_allocation.clean_market_cap)
    a_dirty_market_cap.append(results_allocation.dirty_market_cap)
    a_firm_net_value.append(results_allocation.firm_net_value)
    a_net_market_cap.append(results_allocation.net_market_cap)
    
    t_reformed_real_assets.append(results_transformation.reformed_assets)
    t_secondary_traded_assets.append(results_transformation.secondary_trading)
    t_total_market_capitalization.append(results_transformation.market_capitalization)
    t_risk_adjusted_return.append(results_transformation.risk_adjusted_return)
    t_normalized_risk_adjusted_welfare.append(results_transformation.risk_adjusted_return / (params.I))
    t_n_welfare.append(results_transformation.investor_risk_adjusted[InvestorType.n])
    t_g_welfare.append(results_transformation.investor_risk_adjusted[InvestorType.g])
    t_s_welfare.append(results_transformation.investor_risk_adjusted[InvestorType.s])
    t_firm_market_cap.append(results_transformation.firm_market_cap)
    t_clean_market_cap.append(results_transformation.clean_market_cap)
    t_dirty_market_cap.append(results_transformation.dirty_market_cap)
    t_firm_net_value.append(results_transformation.firm_net_value)
    t_net_market_cap.append(results_transformation.net_market_cap)
    """

# Create DataFrame
RESULT_ROWS = results_rows
results_DF = pd.DataFrame.from_records(
    RESULT_ROWS,
    columns=["Iter", 
             "Model", 
             "Metric", 
             "Metric Level",
            "Entity Kind",
            "Entity ID",
             "Value"],
)


"""

plt.plot(Is_values, a_reformed_real_assets, label='Reformed Real Assets (Allocation Only)')
plt.plot(Is_values, a_secondary_traded_assets, label='Secondary Traded Assets (Allocation Only)')
plt.plot(Is_values, t_reformed_real_assets, label='Reformed Real Assets (+Transformation)')
plt.plot(Is_values, t_secondary_traded_assets, label='Secondary Traded Assets (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Assets')
plt.title('Assets vs Is')
plt.legend()
plt.show()

plt.plot(Is_values, a_total_market_capitalization, label='Total Market Capitalization (Allocation Only)')
plt.plot(Is_values, t_total_market_capitalization, label='Total Market Capitalization (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Market Capitalization')
plt.title('Market Capitalization vs Is')
plt.legend()
plt.show()

plt.plot(Is_values, a_risk_adjusted_welfare, label='Risk Adjusted Welfare (Allocation Only)')
plt.plot(Is_values, t_risk_adjusted_welfare, label='Risk Adjusted Welfare (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Risk Adjusted Welfare')
plt.title('Risk Adjusted Welfare vs Is')
plt.legend()
plt.show()

plt.plot(Is_values, a_normalized_risk_adjusted_welfare, label='Normalized Risk Adjusted Welfare')
plt.plot(Is_values, t_normalized_risk_adjusted_welfare, label='Normalized Risk Adjusted Welfare (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Normalized Risk Adjusted Welfare')
plt.title('Normalized Risk Adjusted Welfare vs Is')
plt.legend()
plt.show()

plt.plot(Is_values, a_n_welfare, label='Investor n Welfare (Allocation Only)')
plt.plot(Is_values, t_n_welfare, label='Investor n Welfare (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Investor n Welfare')
plt.title('Investor n Welfare vs Is')
plt.legend()
plt.show()

plt.plot(Is_values, a_g_welfare, label='Investor g Welfare (Allocation Only)')
plt.plot(Is_values, t_g_welfare, label='Investor g Welfare (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Investor g Welfare')
plt.title('Investor g Welfare vs Is')
plt.legend()
plt.show()

plt.plot(Is_values, a_s_welfare, label='Investor s Welfare (Allocation Only)')
plt.plot(Is_values, t_s_welfare, label='Investor s Welfare (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Investor s Welfare')
plt.title('Investor s Welfare vs Is')
plt.legend()
plt.show()

for f in FirmType:
    plt.plot(Is_values, [fm[f] for fm in a_firm_market_cap], label=f'Firm {f} Market Cap (Allocation Only)')
    plt.plot(Is_values, [fm[f] for fm in t_firm_market_cap], label=f'Firm {f} Market Cap (+Transformation)')
    plt.xlabel('Is')
    plt.ylabel(f'Firm {f} Market Cap')
    plt.title(f'Firm {f} Market Cap vs Is')
    plt.legend()
    plt.show()

plt.plot(Is_values, a_clean_market_cap, label='Clean Market Cap (Allocation Only)')
plt.plot(Is_values, t_clean_market_cap, label='Clean Market Cap (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Clean Market Cap')
plt.title('Clean Market Cap vs Is')
plt.legend()
plt.show()

plt.plot(Is_values, a_dirty_market_cap, label='Dirty Market Cap (Allocation Only)')
plt.plot(Is_values, t_dirty_market_cap, label='Dirty Market Cap (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Dirty Market Cap')
plt.title('Dirty Market Cap vs Is')
plt.legend()
plt.show()

for f in FirmType:
    plt.plot(Is_values, [fm[f] for fm in a_firm_net_value], label=f'Firm {f} Net Value (Allocation Only)')
    plt.plot(Is_values, [fm[f] for fm in t_firm_net_value], label=f'Firm {f} Net Value (+Transformation)')
    plt.xlabel('Is')
    plt.ylabel(f'Firm {f} Net Value')
    plt.title(f'Firm {f} Net Value vs Is')
    plt.legend()
    plt.show()


plt.plot(Is_values, a_net_market_cap, label='Net Normal Market Cap (Allocation Only)')
plt.plot(Is_values, t_net_market_cap, label='Net Normal Market Cap (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Net Normal Market Cap')
plt.title('Net Normal Market Cap vs Is')
plt.legend()
plt.show()
"""

# This is the last part of the routine, which currently takes care of plotting. I
# want to further develop the code to work using our results DataFrame. Then,
# for each plot, I will have to filter the DataFrame to reconstruct the 
# plotting data. This will be a more robust approach and will allow us to easily add new metrics.

# First Plot: Total Surplus Comparison Against Impact-Investor Population. 
allocation_total_surplus = results_DF[
    (results_DF['Model'] == 'Allocation Only') & 
    (results_DF['Metric'] == 'Total Surplus')]['Value'].values

transformation_total_surplus = results_DF[
    (results_DF['Model'] == '+Transformation') & 
    (results_DF['Metric'] == 'Total Surplus')]['Value'].values

plt.plot(Im_values, allocation_total_surplus, label='Total Surplus (Allocation Only)')
plt.plot(Im_values, transformation_total_surplus, label='Total Surplus (+Transformation)')
plt.xlabel('Im')
plt.ylabel('Total Surplus')
plt.title('Total Surplus v Im')
plt.legend()
plt.show()

# Second Plot: Firm Surplus Comparison Against Impact-Investor Population.
allocation_firm_surplus = results_DF[
    (results_DF['Model'] == 'Allocation Only') & 
    (results_DF['Metric'] == 'Firm Surplus')]['Value'].values

transformation_firm_surplus = results_DF[
    (results_DF['Model'] == '+Transformation') & 
    (results_DF['Metric'] == 'Firm Surplus')]['Value'].values

plt.plot(Im_values, allocation_firm_surplus, label='Firm Surplus (Allocation Only)')
plt.plot(Im_values, transformation_firm_surplus, label='Firm Surplus (+Transformation)')
plt.xlabel('Im')
plt.ylabel('Firm Surplus')
plt.title('Firm Surplus vs Im')
plt.legend()
plt.show()

# Third Plot: Investor Surplus Comparison Against Impact-Investor Population.

allocation_investor_surplus = results_DF[
    (results_DF['Model'] == 'Allocation Only') & 
    (results_DF['Metric'] == 'Investor Surplus') &
    (results_DF['Metric Level'] == 'Aggregate')]['Value'].values

transformation_investor_surplus = results_DF[
    (results_DF['Model'] == '+Transformation') & 
    (results_DF['Metric'] == 'Investor Surplus') &
    (results_DF['Metric Level'] == 'Aggregate')]['Value'].values

plt.plot(Im_values, allocation_investor_surplus, label='Investor Surplus (Allocation Only)')
plt.plot(Im_values, transformation_investor_surplus, label='Investor Surplus (+Transformation)')
plt.xlabel('Im')
plt.ylabel('Investor Surplus')
plt.title('Investor Surplus vs Im')
plt.legend()
plt.show()

# Fourth Plot: Net Investor Surplus Comparison Against Impact-Investor Population.

allocation_net_investor_surplus = results_DF[
    (results_DF['Model'] == 'Allocation Only') & 
    (results_DF['Metric'] == 'Investor Surplus') &
    (results_DF['Metric Level'] == 'Aggregate')]['Value'].values

transformation_net_investor_surplus = results_DF[
    (results_DF['Model'] == '+Transformation') & 
    (results_DF['Metric'] == 'Investor Surplus') &
    (results_DF['Metric Level'] == 'Aggregate')]['Value'].values

allocation_net_investor_surplus = allocation_net_investor_surplus / base.I
transformation_net_investor_surplus = transformation_net_investor_surplus / base.I

plt.plot(Im_values, allocation_net_investor_surplus, label='Net Investor Surplus (Allocation Only)')
plt.plot(Im_values, transformation_net_investor_surplus, label='Net Investor Surplus (+Transformation)')
plt.xlabel('Im')
plt.ylabel('Net Investor Surplus')
plt.title('Net Investor Surplus vs Im')
plt.legend()
plt.show()

"""
for f in FirmType:
    plt.plot(Is_values, [fm[f] for fm in a_firm_net_value], label=f'Firm {f} Net Value (Allocation Only)')
    plt.plot(Is_values, [fm[f] for fm in t_firm_net_value], label=f'Firm {f} Net Value (+Transformation)')
    plt.xlabel('Is')
    plt.ylabel(f'Firm {f} Net Value')
    plt.title(f'Firm {f} Net Value vs Is')
    plt.legend()
    plt.show()
"""

allocation_investor_surplus_dict = results_DF[
    (results_DF['Model'] == 'Allocation Only') & 
    (results_DF['Metric Level'] == 'By Investor') & 
    (results_DF['Metric'] == 'Investor Surplus')]

transformation_investor_surplus_dict = results_DF[
    (results_DF['Model'] == '+Transformation') & 
    (results_DF['Metric Level'] == 'By Investor') & 
    (results_DF['Metric'] == 'Investor Surplus')]

for it in InvestorType:
    print(it)
    it_surplus_allocation = allocation_investor_surplus_dict[
        allocation_investor_surplus_dict['Entity ID'] == it.name]['Value'].values
    it_surplus_transformation = transformation_investor_surplus_dict[
        transformation_investor_surplus_dict['Entity ID'] == it.name]['Value'].values
    plt.plot(Im_values, it_surplus_allocation, label=f'Investor {it} Surplus (Allocation Only)')
    plt.plot(Im_values, it_surplus_transformation, label=f'Investor {it} Surplus (+Transformation)')
    plt.xlabel('Im')
    plt.ylabel(f'Investor {it} Surplus')
    plt.title(f'Investor {it} Surplus vs Im')
    plt.legend()
    plt.show()

    
    if it == InvestorType.n:
        investor_count = base.In
    if it == InvestorType.v:
        investor_count = base.Iv
    if it == InvestorType.m:
            investor_count = base.Im
        
    plt.plot(Im_values, it_surplus_allocation/ investor_count, label=f'Investor {it} Net Surplus (Allocation Only)')
    plt.plot(Im_values, it_surplus_transformation / investor_count, label=f'Investor {it} Net Surplus (+Transformation)')
    plt.xlabel('Im')
    plt.ylabel(f'Investor {it} Net Surplus')
    plt.title(f'Investor {it} Net Surplus vs Im')
    plt.legend()
    plt.show()


