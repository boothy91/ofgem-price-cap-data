# Ofgem energy price cap: unit rates and standing charges by region

Regional electricity (single rate and Economy 7) and gas rates under the Ofgem price cap,
**1 October 2026 – 31 March 2027**, for each of the 14 GB regions and 3 payment types
(Direct Debit, on receipt of bill / standard credit, prepayment).

## Files
| File | Contents |
|---|---|
| `data/electricity_rates.csv` | Single rate + Economy 7 |
| `data/gas_rates.csv` | Gas |
| `data/price_cap_rates_all.csv` / `.json` | Everything (252 rows) |
| `data/raw/` | Ofgem's downloaded CSVs |
| `scripts/build.py` | Regenerates everything from `data/raw/` |

Columns: `period_start, period_end, region, fuel, tariff, payment_type, standing_charge_p_per_day, unit_rate_p_per_kwh`

## Coverage
Complete: all 9 Ofgem tables (electricity single rate, Economy 7, gas × Direct Debit, on receipt of bill, prepayment)
for 14 regions, Oct–Dec 2026 and Jan–Mar 2027. Everything comes from Ofgem's own CSV downloads in `data/raw/`.
`data/gb_averages.csv` holds the Great Britain average rows.

## Notes
- Units: pence per day (standing charge) and pence per kWh (unit rate), rounded to 2 d.p.
- Electricity has 0% VAT (1 Oct 2026 – 31 Mar 2027); gas includes 5% VAT.
- Economy 7 is a single combined unit rate (not separate day/night), as published by Ofgem.
- Source: Ofgem, https://www.ofgem.gov.uk/your-energy-supply/your-energy-bill/energy-price-cap-unit-rates-and-standing-charges
- Source CSVs downloaded from the Ofgem page (25 Nov 2026).
- Contains public sector information licensed under the Open Government Licence v3.0.
- The cap for Jan–Mar 2027 is due from Ofgem around 25 Nov 2026; add a new period by dropping in the new CSVs and updating `build.py`.
