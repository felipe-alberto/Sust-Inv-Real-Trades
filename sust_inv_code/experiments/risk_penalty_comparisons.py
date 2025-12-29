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

a_investor_risk_penalty = []
t_investor_risk_penalty = []

a_clean_risk_penalty = []
t_clean_risk_penalty = []

a_dirty_risk_penalty = []
t_dirty_risk_penalty = []

a_risk_adjusted_return = []
t_risk_adjusted_return = []

risk_adjusted_return_diff = []
risk_penalty_diff = []

for ns in Is_values:
    
    params = replace(base, Is=ns)
    p = params 

    eqm_alloc, eqm_transform, results_allocation, results_transformation = run_model(params)
    
    a = results_allocation
    ea = eqm_alloc
    a_total_surplus.append(a.total_surplus)
    a_risk_adjusted_return.append(a.risk_adjusted_return)

    t = results_transformation
    et = eqm_transform
    t_total_surplus.append(t.total_surplus)
    t_risk_adjusted_return.append(t.risk_adjusted_return)

    risk_adjusted_return_diff.append(
        t.risk_adjusted_return - a.risk_adjusted_return
    )
    risk_penalty_diff.append(
        a.risk_penalty - t.risk_penalty
    )

    # Compute clean risk penalty
    # Hardcoding
    a_clean_risk_penalty.append(
        (p.tau / 2) * (
            p.sigma_c**2 * (
                p.In * (ea.X[InvestorType.n][FirmType.A])**2 
                + p.Ig* (ea.X[InvestorType.g][FirmType.A])**2 
                )
        )
    )  
    # Hardcoding
    t_clean_risk_penalty.append(
        (p.tau / 2) * (
            p.sigma_c**2 * (
                p.In * (et.X[InvestorType.n][FirmType.A])**2 
                + p.Ig* (et.X[InvestorType.g][FirmType.A])**2 
                + p.Is* (et.X[InvestorType.s][FirmType.Aprime])**2
                )
        )
    ) 
    # Compute dirty risk penalty
    # Hardcoding
    a_dirty_risk_penalty.append(
        (p.tau / 2) * (
            p.sigma_d**2 * (
                p.In * (ea.X[InvestorType.n][FirmType.U])**2 
                + p.Ig* (ea.X[InvestorType.g][FirmType.S])**2 
                + p.Is* (ea.X[InvestorType.s][FirmType.R])**2
                )
        )
    )
    # Hardcoding
    t_dirty_risk_penalty.append(
        (p.tau / 2) * (
            p.sigma_d**2 * (
                p.In * (et.X[InvestorType.n][FirmType.Uprime])**2 
                + p.Ig* (et.X[InvestorType.g][FirmType.Uprime])**2 
                + p.Is* (et.X[InvestorType.s][FirmType.R])**2
                )
        )
    )

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

plt.plot(Is_values, a_clean_risk_penalty, label='Clean Risk Penalty (Allocation Only)')
plt.plot(Is_values, t_clean_risk_penalty, label='Clean Risk Penalty (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Clean Risk Penalty')
plt.title('Clean Risk Penalty v Is')
plt.legend()
plt.show()

plt.plot(Is_values, a_dirty_risk_penalty, label='Dirty Risk Penalty (Allocation Only)')
plt.plot(Is_values, t_dirty_risk_penalty, label='Dirty Risk Penalty (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Dirty Risk Penalty')
plt.title('Dirty Risk Penalty v Is')
plt.legend()
plt.show()

plt.plot(Is_values, risk_penalty_diff, label='Risk Penalty Difference (Allocation Only - +Transformation)')
plt.plot(Is_values, risk_adjusted_return_diff, label='Risk Adjusted Return Difference (+Transformation - Allocation Only)')
plt.xlabel('Is')
plt.ylabel('Difference')
plt.title('Risk Penalty and Risk Adjusted Return Differences v Is')
plt.legend()
plt.show()