# Ofgem energy price cap: unit rates and standing charges by region

Regional electricity (single rate and Economy 7) and gas rates under the Ofgem price cap,
**1 October – 31 December 2026**, for each of the 14 GB regions and 3 payment types
(Direct Debit, on receipt of bill / standard credit, prepayment).

## Files
| File | Contents |
|---|---|
| `data/electricity_rates.csv` | Single rate + Economy 7 (84 rows) |
| `data/gas_rates.csv` | Gas (42 rows) |
| `data/price_cap_rates_all.csv` / `.json` | Everything (126 rows) |
| `scripts/build.py` | Regenerates all of the above |

Columns: `period_start, period_end, region, fuel, tariff, payment_type, standing_charge_p_per_day, unit_rate_p_per_kwh`

## Notes
- Units: pence per day (standing charge) and pence per kWh (unit rate), rounded to 2 d.p.
- Electricity has 0% VAT (1 Oct 2026 – 31 Mar 2027); gas includes 5% VAT.
- Economy 7 is a single combined unit rate (not separate day/night), as published by Ofgem.
- Source: Ofgem, https://www.ofgem.gov.uk/your-energy-supply/your-energy-bill/energy-price-cap-unit-rates-and-standing-charges
- The Ofgem page renders its tables with JavaScript, so values were transcribed from a
  third-party mirror of Ofgem's tables (EnergySwitch). **Verify against Ofgem's downloadable tables before relying on them.**
- Contains public sector information licensed under the Open Government Licence v3.0.
- The cap for Jan–Mar 2027 is due from Ofgem around 25 Nov 2026; add a new period by editing `scripts/build.py`.
