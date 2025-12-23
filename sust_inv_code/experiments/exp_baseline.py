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
                    Nc=50, Nd=50)
    
options_params = ModelParams(Ig=30, In=30, Is=100, K=0.5, T=0.3, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                    sigma_c=1.0, sigma_d=1.0, sigma_cd=0.05,
                    Nc=100, Nd=50)

zero_price_params = ModelParams(Ig=30, In=30, Is=30, K=0.5, T=0.3, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                    sigma_c=1.0, sigma_d=1.0, sigma_cd=0.0,
                    Nc=100, Nd=50)


base = options_params

# Is_values = np.linspace(100, 150, 100)
Is_values = np.linspace(30, 60, 100)

a_reformed_real_assets = []
a_secondary_traded_assets = []
a_total_market_capitalization = []
a_risk_adjusted_welfare = []
a_normalized_risk_adjusted_welfare = []
a_n_welfare = []
a_g_welfare = []
a_s_welfare = []
a_firm_market_cap = []
a_clean_market_cap = []
a_dirty_market_cap = []

t_reformed_real_assets = []
t_secondary_traded_assets = []
t_total_market_capitalization = []
t_risk_adjusted_welfare = []
t_normalized_risk_adjusted_welfare = []
t_n_welfare = []
t_g_welfare = []
t_s_welfare = []
t_firm_market_cap = []
t_clean_market_cap = []
t_dirty_market_cap = []

for ns in Is_values:
    
    params = replace(base, Is=ns)
    
    results_allocation, results_transformation = run_model(params)
    
    a = results_allocation
    a_reformed_real_assets.append(a.reformed_assets)
    a_secondary_traded_assets.append(a.secondary_trading)
    a_total_market_capitalization.append(a.market_capitalization)
    a_risk_adjusted_welfare.append(a.risk_adjusted_welfare)
    a_normalized_risk_adjusted_welfare.append(a.risk_adjusted_welfare / (params.I))
    a_n_welfare.append(a.investor_welfare[InvestorType.n])
    a_g_welfare.append(a.investor_welfare[InvestorType.g])
    a_s_welfare.append(a.investor_welfare[InvestorType.s])
    a_firm_market_cap.append(a.firm_market_cap)
    a_clean_market_cap.append(a.clean_market_cap)
    a_dirty_market_cap.append(a.dirty_market_cap)
    
    t = results_transformation
    t_reformed_real_assets.append(t.reformed_assets)
    t_secondary_traded_assets.append(t.secondary_trading)
    t_total_market_capitalization.append(t.market_capitalization)
    t_risk_adjusted_welfare.append(t.risk_adjusted_welfare)
    t_normalized_risk_adjusted_welfare.append(t.risk_adjusted_welfare / (params.I))
    t_n_welfare.append(t.investor_welfare[InvestorType.n])
    t_g_welfare.append(t.investor_welfare[InvestorType.g])
    t_s_welfare.append(t.investor_welfare[InvestorType.s])
    t_firm_market_cap.append(t.firm_market_cap)
    t_clean_market_cap.append(t.clean_market_cap)
    t_dirty_market_cap.append(t.dirty_market_cap)

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
