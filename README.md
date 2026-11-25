# Ofgem energy price cap: unit rates and standing charges by region

Regional electricity (single rate and Economy 7) and gas rates under the Ofgem price cap,
**1 October 2026 – 31 March 2027**, for each of the 14 GB regions and 3 payment types
(Direct Debit, on receipt of bill / standard credit, prepayment).

## Files
| File | Contents |
|---|---|
| `data/electricity_rates.csv` | Single rate + Economy 7 |
| `data/gas_rates.csv` | Gas |
| `data/price_cap_rates_all.csv` / `.json` | Everything (238 rows) |
| `data/raw/` | Ofgem's downloaded CSVs |
| `scripts/build.py` | Regenerates everything from `data/raw/` |

Columns: `period_start, period_end, region, fuel, tariff, payment_type, standing_charge_p_per_day, unit_rate_p_per_kwh`

## Coverage
| Table | Oct–Dec 2026 | Jan–Mar 2027 |
|---|---|---|
| Electricity single rate (all 3 payment types) | yes | yes |
| Economy 7 – on receipt of bill, prepayment | yes | yes |
| Economy 7 – Direct Debit | yes (transcribed*) | **not yet added** |
| Gas (all 3 payment types) | yes | yes |

Ofgem's own CSV downloads are in `data/raw/` and are the source for everything except *.
\* Economy 7 Direct Debit Oct–Dec was transcribed from a third-party mirror; the other 8 tables' Oct–Dec
values were cross-checked against Ofgem's CSVs and matched exactly.
`data/gb_averages.csv` holds the Great Britain average rows from the same CSVs.

## Notes
- Units: pence per day (standing charge) and pence per kWh (unit rate), rounded to 2 d.p.
- Electricity has 0% VAT (1 Oct 2026 – 31 Mar 2027); gas includes 5% VAT.
- Economy 7 is a single combined unit rate (not separate day/night), as published by Ofgem.
- Source: Ofgem, https://www.ofgem.gov.uk/your-energy-supply/your-energy-bill/energy-price-cap-unit-rates-and-standing-charges
- Source CSVs downloaded from the Ofgem page (25 Nov 2026).
- Contains public sector information licensed under the Open Government Licence v3.0.
- The cap for Jan–Mar 2027 is due from Ofgem around 25 Nov 2026; add a new period by dropping in the new CSVs and updating `build.py`.
