# experiments/exp_baseline.py
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import replace
from sust_inv_code.src.main import run_model
from sust_inv_code.src.data_structures import ModelParams, FirmType, InvestorType

corner_ob_params = ModelParams(Ig=30, In=30, Is=30, K=0.9, T=0.5, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                    sigma_c=1.0, sigma_d=1.0, sigma_cd=0.0,
                    Nc=50, Nd=50)

interior_ob_params = ModelParams(Ig=30, In=30, Is=30, K=1.0, T=0.8, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                    sigma_c=1.0, sigma_d=1.0, sigma_cd=0.025,
                    Nc=50, Nd=25)
    
options_params = ModelParams(Ig=30, In=30, Is=100, K=0.5, T=0.3, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                        sigma_c=1.0, sigma_d=1.0, sigma_cd=0.05,
                        Nc=100, Nd=50)

zero_price_params = ModelParams(Ig=30, In=30, Is=30, K=0.5, T=0.3, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                    sigma_c=1.0, sigma_d=1.0, sigma_cd=0.0,
                    Nc=100, Nd=50)


base = options_params

Is_values = np.linspace(100, 150, 100)
# Is_values = np.linspace(30, 60, 100)

"""
a_reformed_real_assets = []
a_secondary_traded_assets = []
a_total_market_capitalization = []
a_risk_adjusted_return = []
a_normalized_risk_adjusted_welfare = []
a_n_welfare = []
a_g_welfare = []
a_s_welfare = []
a_firm_market_cap = []
a_clean_market_cap = []
a_dirty_market_cap = []
a_firm_net_value = []
a_net_market_cap = []
"""
a_total_surplus = []
a_firm_surplus = []
a_investor_surplus = []
a_net_investor_surplus = []
a_investor_surplus_dict = []
a_investor_transfers = []

"""
t_reformed_real_assets = []
t_secondary_traded_assets = []
t_total_market_capitalization = []
t_risk_adjusted_return = []
t_normalized_risk_adjusted_welfare = []
t_n_welfare = []
t_g_welfare = []
t_s_welfare = []
t_firm_market_cap = []
t_clean_market_cap = []
t_dirty_market_cap = []
t_firm_net_value = []
t_net_market_cap = []
"""
t_total_surplus = []
t_firm_surplus = []
t_investor_surplus = []
t_net_investor_surplus = []
t_investor_surplus_dict = []
t_investor_transfers = []

for ns in Is_values:
    
    params = replace(base, Is=ns)
    
    results_allocation, results_transformation = run_model(params)
    
    a = results_allocation
    """
    a_reformed_real_assets.append(a.reformed_assets)
    a_secondary_traded_assets.append(a.secondary_trading)
    a_total_market_capitalization.append(a.market_capitalization)
    a_risk_adjusted_return.append(a.risk_adjusted_return)
    a_normalized_risk_adjusted_welfare.append(a.risk_adjusted_return / (params.I))
    a_n_welfare.append(a.investor_risk_adjusted[InvestorType.n])
    a_g_welfare.append(a.investor_risk_adjusted[InvestorType.g])
    a_s_welfare.append(a.investor_risk_adjusted[InvestorType.s])
    a_firm_market_cap.append(a.firm_market_cap)
    a_clean_market_cap.append(a.clean_market_cap)
    a_dirty_market_cap.append(a.dirty_market_cap)
    a_firm_net_value.append(a.firm_net_value)
    a_net_market_cap.append(a.net_market_cap)
    """
    a_total_surplus.append(a.total_surplus)
    a_firm_surplus.append(a.firm_surplus)
    a_investor_surplus.append(a.investor_surplus)
    a_net_investor_surplus.append(a.investor_surplus/params.I)
    a_investor_surplus_dict.append(a.investor_surplus_dict)
    a_investor_transfers.append(a.investor_transfers)
    
    t = results_transformation
    """
    t_reformed_real_assets.append(t.reformed_assets)
    t_secondary_traded_assets.append(t.secondary_trading)
    t_total_market_capitalization.append(t.market_capitalization)
    t_risk_adjusted_return.append(t.risk_adjusted_return)
    t_normalized_risk_adjusted_welfare.append(t.risk_adjusted_return / (params.I))
    t_n_welfare.append(a.investor_risk_adjusted[InvestorType.n])
    t_g_welfare.append(a.investor_risk_adjusted[InvestorType.g])
    t_s_welfare.append(a.investor_risk_adjusted[InvestorType.s])
    t_firm_market_cap.append(t.firm_market_cap)
    t_clean_market_cap.append(t.clean_market_cap)
    t_dirty_market_cap.append(t.dirty_market_cap)
    t_firm_net_value.append(t.firm_net_value)
    t_net_market_cap.append(t.net_market_cap)
    """
    t_total_surplus.append(t.total_surplus)
    t_firm_surplus.append(t.firm_surplus)
    t_investor_surplus.append(t.investor_surplus)
    t_net_investor_surplus.append(t.investor_surplus/params.I)
    t_investor_surplus_dict.append(t.investor_surplus_dict)
    t_investor_transfers.append(t.investor_transfers)

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

plt.plot(Is_values, a_net_investor_surplus, label='Net Investor Surplus (Allocation Only)')
plt.plot(Is_values, t_net_investor_surplus, label='Net Investor Surplus (+Transformation)')
plt.xlabel('Is')
plt.ylabel('Net Investor Surplus')
plt.title('Net Investor Surplus vs Is')
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


