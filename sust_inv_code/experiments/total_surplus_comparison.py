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
t_total_surplus = []

r_difference = []
r_difference_benchmark = []
c_difference = []
total_difference = []
benchmark_difference = []
a_mean_return = []
t_mean_return = []

for ns in Is_values:
    
    params = replace(base, Is=ns)
    p = params 

    eqm_alloc, eqm_transform, results_allocation, results_transformation = run_model(params)
    
    a = results_allocation
    ea = eqm_alloc
    a_total_surplus.append(a.total_surplus)
    a_mean_return.append(a.mean_return)
    
    t = results_transformation
    et = eqm_transform
    t_total_surplus.append(t.total_surplus)
    t_mean_return.append(t.mean_return)

    # Something Off Here
    r_diff = t.risk_adjusted_return - a.risk_adjusted_return
    r_difference.append(r_diff)

    c_diff = (t.reformed_assets * p.K + t.secondary_trading * p.T) - (a.reformed_assets * p.K + a.secondary_trading * p.T)
    total_diff = r_diff - c_diff

    c_difference.append(c_diff)
    total_difference.append(total_diff)
    benchmark_difference.append(t.total_surplus - a.total_surplus)

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





plt.plot(Is_values, a_total_surplus, label='Total Surplus (Allocation Only)')
plt.plot(Is_values, t_total_surplus, label='Total Surplus (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Total Surplus')
plt.title('Total Surplus v Is')
plt.legend()
plt.show()

plt.plot(Is_values, total_difference, label='Total Surplus Difference')
plt.plot(Is_values, benchmark_difference, label='Benchmark Total Surplus Difference', linestyle='dashed')
plt.xlabel('Is')
plt.ylabel('Total Surplus Difference')
plt.title('Total Surplus Difference v Is')
plt.legend()
plt.show()

plt.plot(Is_values, r_difference, label='Difference in Risk Adjusted Return')
plt.xlabel('Is')
plt.ylabel('Risk Adjusted Return Difference')
plt.title('Risk Adjusted Return Difference v Is')
plt.legend()
plt.show()

plt.plot(Is_values, c_difference, label='Difference in Cost of Reformed and Secondary Assets')
plt.xlabel('Is')
plt.ylabel('Cost Difference')
plt.title('Cost Difference v Is')
plt.legend()
plt.show()

plt.plot(Is_values, a_mean_return, label='Mean Return (Allocation Only)')
plt.plot(Is_values, t_mean_return, label='Mean Return (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Mean Return')
plt.title('Mean Return v Is')
plt.legend()
plt.show()


