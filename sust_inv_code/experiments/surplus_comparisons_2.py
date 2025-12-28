# experiments/exp_baseline.py
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import replace
from sust_inv_code.src.main import run_model
from sust_inv_code.src.data_structures import ModelParams, FirmType, InvestorType

    
interior_ob_params = ModelParams(Ig=30, In=30, Is=30, K=1.0, T=0.8, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                        sigma_c=1.0, sigma_d=1.0, sigma_cd=0.00,
                        Nc=50, Nd=50)

base = interior_ob_params

Is_values = np.linspace(30, 60, 100)

a_total_surplus = []
a_firm_surplus = []
a_investor_surplus = []
a_net_investor_surplus = []
a_investor_surplus_dict = []
a_investor_transfers = []

t_total_surplus = []
t_firm_surplus = []
t_investor_surplus = []
t_net_investor_surplus = []
t_investor_surplus_dict = []
t_investor_transfers = []

inequality_LHS = []
inequality_RHS = []
qclist = []
qdlist = []

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
    
    t = results_transformation
    et = eqm_transform
    t_total_surplus.append(t.total_surplus)
    t_firm_surplus.append(t.firm_surplus)
    t_investor_surplus.append(t.investor_surplus)
    t_net_investor_surplus.append(t.investor_surplus/params.I)
    t_investor_surplus_dict.append(t.investor_surplus_dict)
    t_investor_transfers.append(t.investor_transfers)

    p = params
    qD = p.Nd * ( p.Ig / p.I) * (p.T + t.pi)
    qC = p.Nc * (p.Is / p.I) * ((p.Nc / (p.Ig + p.In))*(p.sigma_c**2 / p.tau) - p.K - t.pi ) 
    qclist.append(qC)
    qdlist.append(qD)
    inequality_LHS.append(
         qC + qD
    )
    # inequality_LHS.append(
    #    p.Nc*(et.P[FirmType.A] - ea.P[FirmType.A]) + p.Nd*(et.P[FirmType.U] - ea.P[FirmType.U])
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






plt.plot(Is_values, a_total_surplus, label='Total Surplus (Allocation Only)')
plt.plot(Is_values, t_total_surplus, label='Total Surplus (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Total Surplus')
plt.title('Total Surplus v Is')
plt.legend()
plt.show()

plt.plot(Is_values, a_firm_surplus, label='Firm Surplus (Allocation Only)')
plt.plot(Is_values, t_firm_surplus, label='Firm Surplus (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Firm Surplus')
plt.title('Firm Surplus vs Is')
plt.legend()
plt.show()

plt.plot(Is_values, a_investor_surplus, label='Investor Surplus (Allocation Only)')
plt.plot(Is_values, t_investor_surplus, label='Investor Surplus (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Investor Surplus')
plt.title('Investor Surplus vs Is')
plt.legend()
plt.show()

"""
plt.plot(Is_values, a_net_investor_surplus, label='Net Investor Surplus (Allocation Only)')
plt.plot(Is_values, t_net_investor_surplus, label='Net Investor Surplus (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Net Investor Surplus')
plt.title('Net Investor Surplus vs Is')
plt.legend()
plt.show()

for it in InvestorType:
    print(it)
    plt.plot(Is_values, [isd[it] for isd in a_investor_surplus_dict], label=f'Investor {it} Surplus (Allocation Only)')
    plt.plot(Is_values, [isd[it] for isd in t_investor_surplus_dict], label=f'Investor {it} Surplus (+Transformation)')
    plt.xlabel('Is')
    plt.ylabel(f'Investor {it} Surplus')
    plt.title(f'Investor {it} Surplus vs Is')
    plt.legend()
    plt.show()

    if it == InvestorType.s:
        investor_count = base.Is
    if it == InvestorType.n:
        investor_count = base.In
    if it == InvestorType.g:
        investor_count = base.Ig
        
    plt.plot(Is_values, [isd[it] / investor_count for isd in a_investor_surplus_dict], label=f'Investor {it} Net Surplus (Allocation Only)')
    plt.plot(Is_values, [isd[it] / investor_count for isd in t_investor_surplus_dict], label=f'Investor {it} Net Surplus (+Transformation)')
    plt.xlabel('Is')
    plt.ylabel(f'Investor {it} Net Surplus')
    plt.title(f'Investor {it} Net Surplus vs Is')
    plt.legend()
    plt.show()

    """

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

print("qC")
print(qclist)
print("qD")
print(qdlist)
