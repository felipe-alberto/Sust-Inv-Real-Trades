# experiments/exp_sigma_sweep.py
import numpy as np
import matplotlib.pyplot as plt
from sust_inv_code.src.main import run_model
from sust_inv_code.src.data_structures import ModelParams
from dataclasses import replace

base = ModelParams(Ig=30, In=30, Is=30, K=0.9, T=0.5, tau=1.0, mu_c = 0.5, mu_d = 0.5,
                        sigma_c=1.0, sigma_d=1.0, sigma_cd=0.00,
                        Nc=50, Nd=50)

Is_values = np.linspace(30, 60, 100)
# pis = []
reformed_real_assets = []
secondary_traded_assets = []

for ns in Is_values:
    params = replace(base, Is=ns)
    results = run_model(params)
    reformed_real_assets.append(results.reformed_assets)
    secondary_traded_assets.append(results.secondary_trading)
    # pis.append(eq.pi)

plt.plot(Is_values, reformed_real_assets, label='Reformed Real Assets')
plt.plot(Is_values, secondary_traded_assets, label='Secondary Traded Assets')
plt.xlabel('Is values')
plt.ylabel('Assets')
plt.title('Assets vs Is values')
plt.legend()
plt.show()

