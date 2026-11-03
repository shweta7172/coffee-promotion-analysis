# Do our coffee promotions actually pay off?

A pricing and promotion analysis for *Bean & Co.*, a fictional coffee brand with 4 products in 10 stores (52 weeks, 2025).

**Business question:** which discounts make money, which lose money, and what should the brand do next?

## Key findings

- **The 2025 promotion plan lost about €21,000 in profit** across 10 stores, compared with no promotions.
- **Only 10% off on Budget and Pods pays back** once the sales dip in the week after a promotion is counted.
- **30% discounts lose the most money** on every product, despite the biggest sales spikes.
- **Premium buyers barely react to price** (sensitivity ≈ 1 vs. ≈ 5 for Budget), so discounting Premium gives away margin.
- **20% off Budget looks profitable in the promo week (+12%) but is break-even over two weeks.** Judge promotions over two weeks, not one.
- A simple linear regression per product predicts weekly sales with about 10% error and cuts error by 50–67% versus a simple average (except Premium, where promotions barely matter).

**Recommendation:** keep 10% on Budget and Pods, stop 30% everywhere, stop discounting Premium. Test in 3 stores against 3 similar control stores for 3 months.

## Files

| File | What it is |
|---|---|
| `analysis.ipynb` | The full analysis, Steps 0–7 |
| `generate_data.py` | Creates the simulated data |
| `data/` | `products.csv`, `stores.csv`, `weekly_sales.csv` |
| `charts/` | Charts used in the presentation |

## How the data was simulated (know this before the interview)

The data is simulated on purpose, so the method can be checked against known truth.

1. **Price sensitivity per product:** a 10% discount lifts units by Budget +50%, Standard +35%, Premium +10%, Pods +45%. The analysis recovers these (5.0, 3.4, 1.0, 4.4).
2. **Week-after dip:** customers who stocked up buy less next week. The dip is 15% of the extra promo units for Budget and Pods, 10% for Standard, 0% for Premium.
3. **Seasonality:** winter +10%, summer −10%.
4. **Stores:** large stores sell about 1.6× small stores; each store has its own level (±10%).
5. **Noise:** about 8% random variation each week.
6. **Promotions:** chain-wide, 12 per product per year (4 each at 10/20/30%), never two weeks in a row.
7. **Data issues added on purpose:** 6 missing values and 3 duplicate rows, cleaned in Step 0.

Prices and costs: Budget €4.99 (cost €2.75), Standard €12.99 (€7.80), Premium €8.99 (€4.05), Pods €5.49 (€2.75).

## How to run

```bash
pip install pandas matplotlib scikit-learn jupyter
python generate_data.py     # optional, data is already included
jupyter notebook analysis.ipynb
```

## Limitations

Simulated, clean data, so real accuracy would be lower. With real data I would add competitor prices, holidays,
cannibalisation between own products, and store-level effects, and check sample sizes before deciding.
