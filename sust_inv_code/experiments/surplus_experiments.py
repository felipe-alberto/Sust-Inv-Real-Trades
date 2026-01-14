# experiments/exp_baseline.py
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import replace
from sust_inv_code.src.main import run_model
from sust_inv_code.src.data_structures import ModelParams, FirmType, InvestorType

    
options_params = ModelParams(Ig=30, In=30, Is=100, K=0.5, T=0.3, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                        sigma_c=1.0, sigma_d=1.0, sigma_cd=0.00,
                        Nc=100, Nd=50)

base = options_params

Is_values = np.linspace(100, 150, 100)

a_total_surplus = []
a_firm_surplus = []
a_investor_surplus = []
a_net_investor_surplus = []
a_investor_surplus_dict = []
a_investor_transfers = []
a_firm_costs = []
a_market_cap = []
a_clean_cap = []
a_dirty_cap = []
a_clean_cost = []
a_dirty_cost = []

t_total_surplus = []
t_firm_surplus = []
t_investor_surplus = []
t_net_investor_surplus = []
t_investor_surplus_dict = []
t_investor_transfers = []
t_firm_costs = []
t_market_cap = []
t_clean_cap = []
t_dirty_cap = []
t_clean_cost = []
t_dirty_cost = []

cost_diff = []
market_cap_diff = []
clean_cap_diff = []
dirty_cap_diff = []
clean_cost_diff = []
dirty_cost_diff = []

inequality_LHS = []
inequality_RHS = []

for ns in Is_values:
    
    params = replace(base, Is=ns)
    
    eqm_alloc, eqm_transform, results_allocation, results_transformation = run_model(params)
    
    a = results_allocation
    ea = eqm_alloc
    a_total_surplus.append(a.total_surplus)
    a_firm_surplus.append(a.firm_surplus)
    a_investor_surplus.append(a.investor_surplus)
    a_net_investor_surplus.append(a.investor_surplus/params.I)
    a_investor_surplus_dict.append(a.investor_surplus_dict)
    a_investor_transfers.append(a.investor_transfers)
    a_firm_costs.append(a.reformed_assets * params.K + a.secondary_trading * params.T)
    a_market_cap.append(a.market_capitalization)
    a_clean_cap.append(a.clean_market_cap)
    a_dirty_cap.append(a.dirty_market_cap)
    a_clean_cost.append(0)
    a_dirty_cost.append(ea.N[FirmType.R]*params.K + ea.N[FirmType.S] * params.T)
    
    t = results_transformation
    et = eqm_transform
    t_total_surplus.append(t.total_surplus)
    t_firm_surplus.append(t.firm_surplus)
    t_investor_surplus.append(t.investor_surplus)
    t_net_investor_surplus.append(t.investor_surplus/params.I)
    t_investor_surplus_dict.append(t.investor_surplus_dict)
    t_investor_transfers.append(t.investor_transfers)
    t_firm_costs.append(t.reformed_assets * params.K + t.secondary_trading * params.T)
    t_market_cap.append(t.market_capitalization)
    t_clean_cap.append(t.clean_market_cap)
    t_dirty_cap.append(t.dirty_market_cap)
    t_clean_cost.append(et.N[FirmType.Uprime]*params.K)
    t_dirty_cost.append(et.N[FirmType.R]*params.K)

    cost_diff.append(t_firm_costs[-1] - a_firm_costs[-1])
    market_cap_diff.append(t_market_cap[-1] - a_market_cap[-1])
    clean_cap_diff.append(t_clean_cap[-1] - a_clean_cap[-1])
    clean_cost_diff.append(t_clean_cost[-1] - a_clean_cost[-1])
    dirty_cap_diff.append(t_dirty_cap[-1] - a_dirty_cap[-1])
    dirty_cost_diff.append(t_dirty_cost[-1] - a_dirty_cost[-1])
    
    p = params
    qD = (p.Nd * ( (p.Ig + p.In) * t.pi + p.Ig * p.T)) / p.I
    qC = (p.Nc * ( p.Is * ( p.K + t.pi - (p.Nc / (p.Ig + p.In)) * ( p.sigma_c**2 / p.tau)))) / p.I

    inequality_LHS.append(
        qD - qC
    )
    # inequality_LHS.append(
    #    p.Nc*(et.P[FirmType.A] - ea.P[FirmType.A]) + p.Nd*(et.P[FirmType.R] - ea.P[FirmType.U] - p.K)
    #)
    inequality_RHS.append(
        t.firm_surplus - a.firm_surplus
    )
    # Checks

    import math

    assert math.isclose(
        t.investor_surplus - a.investor_surplus,
        (t.risk_adjusted_return - t.market_capitalization) - (a.risk_adjusted_return - a.market_capitalization),
        rel_tol=1e-9,
        abs_tol=1e-12,
    ), "Investor Surplus does not equal Risk Adjusted Welfare minus Market Capitalization difference"

    assert math.isclose(
        a.market_capitalization,
        a.investor_transfers[InvestorType.n] + a.investor_transfers[InvestorType.g] + a.investor_transfers[InvestorType.s],
        rel_tol=1e-9,
        abs_tol=1e-12,
    ), "Allocation Only: Market capitalization does not equal total investor transfers"

    assert math.isclose(
        t.market_capitalization,
        t.investor_transfers[InvestorType.n] + t.investor_transfers[InvestorType.g] + t.investor_transfers[InvestorType.s],
        rel_tol=1e-9,
        abs_tol=1e-12,
    ), "+ Transformation: Market capitalization does not equal total investor transfers"


"""
# 1. Total Surplus Goes Up
plt.plot(Is_values, a_total_surplus, label='Total Surplus (Allocation Only)')
plt.plot(Is_values, t_total_surplus, label='Total Surplus (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Total Surplus')
plt.title('Total Surplus v Is')
plt.legend()
plt.show()

# 2. Firm Surplus Goes Up
plt.plot(Is_values, a_firm_surplus, label='Firm Surplus (Allocation Only)')
plt.plot(Is_values, t_firm_surplus, label='Firm Surplus (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Firm Surplus')
plt.title('Firm Surplus vs Is')
plt.legend()
plt.show()

# 2.1.1 Firm's Costs Go Up
plt.plot(Is_values, a_firm_costs, label='Firm Costs (Allocation Only)')
plt.plot(Is_values, t_firm_costs, label='Firm Costs (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Firm Costs')
plt.title('Firm Costs vs Is')
plt.legend()
plt.show()

# 2.1.2 Total Market Value Goes Up
plt.plot(Is_values, a_market_cap, label='Firm Market Cap (Allocation Only)')
plt.plot(Is_values, t_market_cap, label='Firm Market Cap (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Market Cap')
plt.title('Market Cap vs Is')
plt.legend()
plt.show()

# 2.1.3 Total Market Value Incr More Than Costs
plt.plot(Is_values, cost_diff, label='Cost Diff')
plt.plot(Is_values, market_cap_diff, label='Market Cap Diff')
plt.xlabel('Is')
plt.ylabel('Diffs')
plt.title('Diffs vs Is')
plt.legend()
plt.show()

# 2.2.1 Clean Firm's Total Market Value Goes Up 
plt.plot(Is_values, a_clean_cap, label='Clean Market Cap (Allocation Only)')
plt.plot(Is_values, t_clean_cap, label='Clean Market Cap (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Clean Cap')
plt.title('Clean Cap vs Is')
plt.legend()
plt.show()

# 2.2.2 Clean Firm's Total Cost
plt.plot(Is_values, a_clean_cost, label='Clean Cost (Allocation Only)')
plt.plot(Is_values, t_clean_cost, label='Clean Cost (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Clean Cost')
plt.title('Clean Cost vs Is')
plt.legend()
plt.show()


# 2.2.3 Dirty Firm's Total Market Value Goes Up 
plt.plot(Is_values, a_dirty_cap, label='Dirty Market Cap (Allocation Only)')
plt.plot(Is_values, t_dirty_cap, label='Dirty Market Cap (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Dirty Cap')
plt.title('Dirty Cap vs Is')
plt.legend()
plt.show()

# 2.2.3 Dirty Firm's Total Cost
plt.plot(Is_values, a_dirty_cost, label='Dirty Cost (Allocation Only)')
plt.plot(Is_values, t_dirty_cost, label='Dirty Cost (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Dirty Cost')
plt.title('Dirty Cost vs Is')
plt.legend()
plt.show()

# 2.2.4 Clean Cap Diff and Cost Diff
plt.plot(Is_values, clean_cap_diff, label='Clean Cap Diff')
plt.plot(Is_values, clean_cost_diff, label='Clean Cost Diff')
plt.xlabel('Is')
plt.ylabel('Diff')
plt.title('Diff vs Is')
plt.legend()
plt.show()

# 2.2.5 Dirty Cap Diff and Cost Diff
plt.plot(Is_values, dirty_cap_diff, label='Dirty Cap Diff')
plt.plot(Is_values, dirty_cost_diff, label='Dirty Cost Diff')
plt.xlabel('Is')
plt.ylabel('Diff')
plt.title('Diff vs Is')
plt.legend()
plt.show()
"""

"""

plt.plot(Is_values, a_investor_surplus, label='Investor Surplus (Allocation Only)')
plt.plot(Is_values, t_investor_surplus, label='Investor Surplus (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Investor Surplus')
plt.title('Investor Surplus vs Is')
plt.legend()
plt.show()

plt.plot(Is_values, inequality_LHS, label='Inequality LHS')
plt.plot(Is_values, inequality_RHS, label='Inequality RHS')
plt.xlabel('Is')
plt.ylabel('Inequality Sides')
plt.title('Inequality Sides vs Is')
plt.legend()
plt.show()

print("LHS")
print(inequality_LHS)
print("RHS")
print(inequality_RHS)

"""

