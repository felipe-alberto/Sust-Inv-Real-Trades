import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# Settings
# =========================================================
START_YEAR = 2012
END_YEAR = 2024

FLARING_FILE = "/Users/felipeverastegui/Desktop/sust-inv-real-trades/sust_inv_code/data/2012-2024-Flare-Volume-Estimates-by-individual-Flare-Location.xlsx"
HENRY_HUB_FILE = "/Users/felipeverastegui/Desktop/sust-inv-real-trades/sust_inv_code/data/AHHNGSP.csv"

# Approximate conversion:
# 1 bcm natural gas ≈ 35.3 million MMBtu
MMBTU_PER_BCM = 35.3e6


# =========================================================
# Load and aggregate yearly flaring volumes
# =========================================================
def load_yearly_flaring(path):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["bcm"] = pd.to_numeric(df["bcm"], errors="coerce")

    yearly = (
        df.groupby("Year", as_index=False)["bcm"]
        .sum()
        .sort_values("Year")
        .rename(columns={"Year": "year", "bcm": "flaring_bcm"})
    )

    yearly = yearly[(yearly["year"] >= START_YEAR) & (yearly["year"] <= END_YEAR)]
    return yearly


# =========================================================
# Load and aggregate yearly Henry Hub prices
# =========================================================
def load_yearly_henry_hub(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    df["observation_date"] = pd.to_datetime(df["observation_date"], errors="coerce")
    df["AHHNGSP"] = pd.to_numeric(df["AHHNGSP"], errors="coerce")

    df["year"] = df["observation_date"].dt.year

    yearly = (
        df.groupby("year", as_index=False)["AHHNGSP"]
        .mean()
        .rename(columns={"AHHNGSP": "henry_hub_usd_per_mmbtu"})
    )

    yearly = yearly[(yearly["year"] >= START_YEAR) & (yearly["year"] <= END_YEAR)]
    return yearly


# =========================================================
# Build merged dataset
# =========================================================
flaring_yearly = load_yearly_flaring(FLARING_FILE)
price_yearly = load_yearly_henry_hub(HENRY_HUB_FILE)

merged = pd.merge(flaring_yearly, price_yearly, on="year", how="inner").sort_values("year")

merged["foregone_revenue_usd"] = (
    merged["flaring_bcm"] * MMBTU_PER_BCM * merged["henry_hub_usd_per_mmbtu"]
)
merged["foregone_revenue_usd_billions"] = merged["foregone_revenue_usd"] / 1e9

print(merged)


# =========================================================
# Plot styling
# =========================================================
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

fig, axes = plt.subplots(
    3, 1,
    figsize=(8.2, 9.0),
    sharex=True,
    gridspec_kw={"hspace": 0.12}
)

line_width = 2.2
marker_size = 4.5

# =========================================================
# Color palette (muted, publication-style)
# =========================================================
color_flaring = "#2C3E50"   # deep blue
color_price   = "#3A7D44"   # muted green
color_revenue = "#8C2D19"   # dark red


# --- Panel 1: Flaring volume ---
axes[0].plot(
    merged["year"],
    merged["flaring_bcm"],
    linewidth=line_width,
    marker="o",
    markersize=marker_size,
    color=color_flaring
)
axes[0].set_ylabel("Flaring (bcm)")
axes[0].set_ylim(bottom=0)


# --- Panel 2: Henry Hub price ---
axes[1].plot(
    merged["year"],
    merged["henry_hub_usd_per_mmbtu"],
    linewidth=line_width,
    marker="o",
    markersize=marker_size,
    color=color_price
)
axes[1].set_ylabel("Price ($/MMBtu)")
axes[1].set_ylim(bottom=0)


# --- Panel 3: Foregone revenue ---
axes[2].plot(
    merged["year"],
    merged["foregone_revenue_usd_billions"],
    linewidth=line_width,
    marker="o",
    markersize=marker_size,
    color=color_revenue
)
axes[2].set_ylabel("Revenue (bn USD)")
axes[2].set_xlabel("Year")
axes[2].set_ylim(bottom=0)

# --- Shared styling across panels ---
for ax in axes:
    ax.grid(True, axis="y", alpha=0.18, linewidth=0.8)
    ax.grid(False, axis="x")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_linewidth(0.8)
    ax.spines["bottom"].set_linewidth(0.8)

    ax.tick_params(axis="both", which="major", length=4, width=0.8)

# x-axis ticks
axes[2].set_xticks(merged["year"])
axes[2].set_xticklabels(merged["year"].astype(int), rotation=0)

axes[0].text(0.01, 0.32, "(a) Flaring volume", transform=axes[0].transAxes)
axes[1].text(0.01, 0.92, "(b) Henry Hub price", transform=axes[1].transAxes)
axes[2].text(0.01, 0.92, "(c) Implied foregone revenue", transform=axes[2].transAxes)

# Optional overall title: leave blank for paper-style figure
# fig.suptitle("Flaring Volumes, Henry Hub Prices, and Implied Foregone Revenues", y=0.98)

plt.tight_layout()
plt.show()



# =========================================================
# Settings
# =========================================================
EMISSIONS_FILE = "/Users/felipeverastegui/Desktop/sust-inv-real-trades/sust_inv_code/data/annual-co2-flaring.csv"
START_YEAR = 2012
END_YEAR = 2024

# Simple first-pass assumption:
# SCC in USD per metric ton of CO2
SCC_USD_PER_TON_CO2 = 190

# Change this if your emissions variable has a different name
EMISSIONS_COL = "Annual CO₂ emissions from flaring"


# =========================================================
# Load data
# =========================================================
df = pd.read_csv(EMISSIONS_FILE)
df.columns = df.columns.str.strip()
print(df.columns.tolist())

# In case the CO2 column has encoding weirdness, print columns once:
print("Columns found:", df.columns.tolist())

# If needed, replace the line below with the exact column name from your file
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df[EMISSIONS_COL] = pd.to_numeric(df[EMISSIONS_COL], errors="coerce")

# Keep relevant years
df = df[(df["Year"] >= START_YEAR) & (df["Year"] <= END_YEAR)]

# =========================================================
# Aggregate to yearly global emissions
# =========================================================
yearly = (
    df.groupby("Year", as_index=False)[EMISSIONS_COL]
    .sum()
    .sort_values("Year")
    .rename(columns={
        "Year": "year",
        EMISSIONS_COL: "co2_flaring_tons"
    })
)

# =========================================================
# Compute social cost
# =========================================================
yearly["social_cost_usd"] = yearly["co2_flaring_tons"] * SCC_USD_PER_TON_CO2
yearly["social_cost_usd_billions"] = yearly["social_cost_usd"] / 1e9

print(yearly)

# Optional save
yearly.to_csv("yearly_social_cost_of_flaring.csv", index=False)

# =========================================================
# Plot
# =========================================================
plt.figure(figsize=(7.5, 4.5))

plt.plot(
    yearly["year"],
    yearly["social_cost_usd_billions"],
    linewidth=2.4,
    marker="o",
    markersize=4.5,
    color="#7A2E1C"
)

plt.xlabel("Year")
plt.ylabel("Social cost (bn USD)")
plt.ylim(bottom=0)

ax = plt.gca()
ax.grid(True, axis="y", alpha=0.18, linewidth=0.8)
ax.grid(False, axis="x")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.show()