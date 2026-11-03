"""
Generates the simulated dataset for the project
"Do our coffee promotions actually pay off?"

The data is SIMULATED for a fictional coffee brand ("Bean & Co.").
All built-in patterns are listed in ASSUMPTIONS below, so the analysis
can be checked against what we know is true.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

# ---------------------------------------------------------------
# ASSUMPTIONS (the "truth" hidden in the data)
# ---------------------------------------------------------------
# 1. Each product reacts differently to discounts (sensitivity):
#    a 10% discount lifts units by  sensitivity x 10%.
#    Budget 5.0 (+50%), Standard 3.5 (+35%), Premium 1.0 (+10%), Pods 4.5 (+45%).
# 2. Week after a promotion: customers stocked up, so sales dip.
#    The dip equals a share of the extra units sold in the promo week:
#    Budget 15%, Pods 15%, Standard 10%, Premium 0%.
# 3. Seasonality: winter (Dec-Feb) +10%, summer (Jun-Aug) -10%.
# 4. Large stores sell about 1.6x small stores; each store also has
#    its own small random level (+/- 10%).
# 5. Random week-to-week noise of about 8%.
# 6. Promotions run chain-wide (all stores same week), about 12 weeks
#    per product per year, never two weeks in a row.
# ---------------------------------------------------------------

products = pd.DataFrame({
    "product_id": ["P1", "P2", "P3", "P4"],
    "product_name": ["Everyday Ground 500g", "Classic Beans 1kg",
                     "Origin Premium 250g", "Coffee Pods 20-pack"],
    "segment": ["Budget", "Standard", "Premium", "Pods"],
    "regular_price": [4.99, 12.99, 8.99, 5.49],
    "unit_cost": [2.75, 7.80, 4.05, 2.75],
})
SENSITIVITY = {"P1": 5.0, "P2": 3.5, "P3": 1.0, "P4": 4.5}
DIP_SHARE = {"P1": 0.15, "P2": 0.10, "P3": 0.00, "P4": 0.15}
BASE_UNITS_SMALL = {"P1": 110, "P2": 40, "P3": 28, "P4": 65}

cities = ["Cologne", "Duesseldorf", "Bonn", "Essen", "Dortmund",
          "Aachen", "Muenster", "Bochum", "Wuppertal", "Leverkusen"]
sizes = ["Large", "Large", "Small", "Large", "Large",
         "Small", "Small", "Small", "Small", "Small"]
stores = pd.DataFrame({
    "store_id": [f"S{i:02d}" for i in range(1, 11)],
    "city": cities,
    "store_size": sizes,
})
store_level = dict(zip(stores.store_id, rng.uniform(0.9, 1.1, len(stores))))

weeks = pd.date_range("2025-01-06", periods=52, freq="W-MON")


def season_factor(month):
    if month in (12, 1, 2):
        return 1.10
    if month in (6, 7, 8):
        return 0.90
    return 1.00


# Promotion calendar per product: ~12 promo weeks, depths balanced, no back-to-back
calendar = {}
for pid in products.product_id:
    discount = np.zeros(52)
    candidates = list(rng.permutation(np.arange(1, 51)))
    chosen = []
    for w in candidates:
        if all(abs(w - c) > 1 for c in chosen):
            chosen.append(w)
        if len(chosen) == 12:
            break
    depths = rng.permutation([0.10] * 4 + [0.20] * 4 + [0.30] * 4)
    for w, d in zip(sorted(chosen), depths):
        discount[w] = d
    calendar[pid] = discount

rows = []
for _, p in products.iterrows():
    pid = p.product_id
    disc = calendar[pid]
    for _, s in stores.iterrows():
        size_mult = 1.6 if s.store_size == "Large" else 1.0
        base = BASE_UNITS_SMALL[pid] * size_mult * store_level[s.store_id]
        for i, wk in enumerate(weeks):
            normal_units = base * season_factor(wk.month)
            uplift = SENSITIVITY[pid] * disc[i]
            expected = normal_units * (1 + uplift)
            # dip in the week after a promotion
            if i > 0 and disc[i - 1] > 0:
                prev_extra = SENSITIVITY[pid] * disc[i - 1] * normal_units
                expected -= DIP_SHARE[pid] * prev_extra
            units = max(0, round(expected * rng.normal(1, 0.08)))
            rows.append({
                "week_start": wk.date(),
                "store_id": s.store_id,
                "product_id": pid,
                "discount_pct": int(round(disc[i] * 100)),
                "price_paid": round(p.regular_price * (1 - disc[i]), 2),
                "units_sold": units,
            })

sales = pd.DataFrame(rows)

# A few realistic data-quality issues for the data check (Step 0)
idx_missing = rng.choice(len(sales), 6, replace=False)
sales.loc[idx_missing, "units_sold"] = np.nan
dup = sales.sample(3, random_state=1)
sales = pd.concat([sales, dup]).sort_values(
    ["week_start", "store_id", "product_id"]).reset_index(drop=True)

products.to_csv("data/products.csv", index=False)
stores.to_csv("data/stores.csv", index=False)
sales.to_csv("data/weekly_sales.csv", index=False)
print(len(sales), "sales rows written")
