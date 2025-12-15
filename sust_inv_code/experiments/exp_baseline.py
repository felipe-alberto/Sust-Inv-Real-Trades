# experiments/exp_sigma_sweep.py
import numpy as np
import matplotlib.pyplot as plt
from sust_inv_code.src.main import run_model
from sust_inv_code.src.data_structures import ModelParams
from dataclasses import replace

base = ModelParams(Ig=30, In=30, Is=30, K=0.9, T=0.5, tau=1.0, mu_c = 5.0, mu_d = 5.0,
                        sigma_c=1.0, sigma_d=1.0, sigma_cd=0.00,
                        Nc=50, Nd=50)

Is_values = np.linspace(30, 60, 100)
# pis = []
reformed_real_assets = []
secondary_traded_assets = []
total_market_capitalization = []
risk_adjusted_welfare = []
normalized_risk_adjusted_welfare = []

for ns in Is_values:
    params = replace(base, Is=ns)
    results = run_model(params)
    reformed_real_assets.append(results.reformed_assets)
    secondary_traded_assets.append(results.secondary_trading)
    total_market_capitalization.append(results.market_capitalization)
    risk_adjusted_welfare.append(results.risk_adjusted_welfare)
    normalized_risk_adjusted_welfare.append(results.risk_adjusted_welfare / (params.Ig + params.In + params.Is))
    # pis.append(eq.pi)

plt.plot(Is_values, reformed_real_assets, label='Reformed Real Assets')
plt.plot(Is_values, secondary_traded_assets, label='Secondary Traded Assets')
plt.xlabel('Is values')
plt.ylabel('Assets')
plt.title('Assets vs Is values')
plt.legend()
plt.show()

plt.plot(Is_values, total_market_capitalization, label='Total Market Capitalization')
plt.xlabel('Is values')
plt.ylabel('Market Capitalization')
plt.title('Market Capitalization vs Is values')
plt.legend()
plt.show()

plt.plot(Is_values, risk_adjusted_welfare, label='Risk Adjusted Welfare')
plt.xlabel('Is values')
plt.ylabel('Risk Adjusted Welfare')
plt.title('Risk Adjusted Welfare vs Is values')
plt.legend()
plt.show()

plt.plot(Is_values, normalized_risk_adjusted_welfare, label='Normalized Risk Adjusted Welfare')
plt.xlabel('Is values')
plt.ylabel('Normalized Risk Adjusted Welfare')
plt.title('Normalized Risk Adjusted Welfare vs Is values')
plt.legend()
plt.show()


