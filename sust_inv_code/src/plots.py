import matplotlib.pyplot as plt
from src.data_structures import ModelParams
from src.equilibrium import solve_equilibrium

def plot_equilibrium_vs_sigma(params: ModelParams, sigmas):
    outcomes = []
    for s in sigmas:
        p = params.replace(sigma_cd=s)
        outcomes.append(solve_equilibrium(p).pi)

    plt.plot(sigmas, outcomes)
    plt.xlabel("σ_cd")
    plt.ylabel("π*")
    plt.savefig("output/figures/equilibrium_vs_sigma.png")