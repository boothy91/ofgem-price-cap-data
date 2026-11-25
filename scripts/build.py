"""Builds CSV/JSON from the tables below. Values in pence (sc = p/day, rate = p/kWh)."""
import csv, json
PERIOD = ("2026-10-01", "2026-12-31")
REGIONS = ["North Western England","North Eastern England","Yorkshire","Northern Scotland",
 "Southern England","Southern Scotland","Merseyside and Northern Wales","London",
 "South Eastern England","Eastern England","East Midlands","West Midlands",
 "South Western England","Southern Wales"]
# per region: (DD sc, DD rate, standard-credit sc, rate, prepayment sc, rate)
SINGLE = """45.68 26.49 53.73 27.98 45.68 25.68
61.58 25.46 70.61 26.89 61.58 24.68
61.67 25.60 70.67 27.05 61.67 24.82
55.14 26.35 63.67 27.83 55.14 25.54
47.81 26.47 56.41 27.95 47.81 25.66
61.41 26.11 70.19 27.58 61.41 25.31
67.66 27.86 76.72 29.43 67.66 27.01
42.92 26.60 50.51 28.09 42.92 25.78
52.32 26.88 61.19 28.39 52.32 26.06
51.84 26.61 60.62 28.11 51.84 25.80
51.45 25.36 60.05 26.78 51.45 24.58
57.23 25.60 65.99 27.04 57.23 24.82
55.58 26.58 64.55 28.08 55.58 25.77
55.41 26.55 63.93 28.05 55.41 25.74"""
E7 = """45.13 24.99 53.67 26.39 45.13 24.23
60.98 24.12 70.52 25.47 60.98 23.38
61.13 24.33 70.58 25.69 61.13 23.59
55.55 24.93 63.59 26.33 55.55 24.17
47.75 25.03 56.35 26.43 47.75 24.27
61.72 24.70 70.11 26.08 61.72 23.95
67.02 26.28 76.64 27.74 67.02 25.48
42.57 25.08 50.45 26.48 42.57 24.32
52.48 25.36 61.12 26.78 52.48 24.59
51.95 25.17 60.55 26.57 51.95 24.40
51.02 24.05 59.97 25.39 51.02 23.32
56.89 24.32 65.91 25.68 56.89 23.58
55.80 25.10 64.48 26.50 55.80 24.33
54.64 25.14 63.85 26.54 54.64 24.37"""
GAS = """29.81 7.86 37.50 8.29 29.81 7.58
29.79 7.92 37.50 8.35 29.79 7.66
29.77 7.90 37.50 8.32 29.77 7.61
29.87 7.87 37.50 8.29 29.87 7.57
29.16 8.17 37.48 8.61 29.16 7.94
29.89 7.87 37.50 8.29 29.89 7.57
30.08 7.91 37.50 8.33 30.08 7.62
30.20 8.15 37.49 8.58 30.20 7.90
29.26 8.05 37.49 8.48 29.26 7.78
29.34 7.91 37.50 8.34 29.34 7.68
29.41 7.82 37.50 8.24 29.41 7.54
29.71 7.90 37.50 8.33 29.71 7.64
29.31 8.12 37.49 8.55 29.31 7.89
29.96 8.09 37.49 8.52 29.96 7.80"""
PAY = ["Direct Debit", "On receipt of bill (standard credit)", "Prepayment"]
rows = []
for fuel, tariff, block in [("electricity","Single rate",SINGLE),("electricity","Economy 7 (multi-rate)",E7),("gas","Gas",GAS)]:
    lines = block.splitlines(); assert len(lines) == 14
    for region, line in zip(REGIONS, lines):
        v = [float(x) for x in line.split()]
        for i, pay in enumerate(PAY):
            rows.append(dict(period_start=PERIOD[0], period_end=PERIOD[1], region=region, fuel=fuel,
                tariff=tariff, payment_type=pay, standing_charge_p_per_day=v[2*i], unit_rate_p_per_kwh=v[2*i+1]))
# --- Jan-Mar 2027 (published by Ofgem 25 Nov 2026) ---
# Columns: Oct-Dec SC, Jan-Mar SC, Oct-Dec rate, Jan-Mar rate. Only tables supplied so far are included.
JAN_PERIOD = ("2027-01-01", "2027-03-31")
JAN_SINGLE_DD = """45.68 45.62 26.49 32.85
61.58 61.51 25.46 31.69
61.67 61.59 25.60 32.11
55.14 55.07 26.35 32.40
47.81 47.74 26.47 32.78
61.41 61.33 26.11 32.57
67.66 67.59 27.86 34.44
42.92 42.88 26.60 33.08
52.32 52.25 26.88 33.29
51.84 51.76 26.61 33.05
51.45 51.38 25.36 31.65
57.23 57.16 25.60 32.00
55.58 55.51 26.58 32.86
55.41 55.35 26.55 32.92"""
base = {(r["region"], r["fuel"], r["tariff"], r["payment_type"]): r for r in rows}
for region, line in zip(REGIONS, JAN_SINGLE_DD.splitlines()):
    sc0, sc1, ur0, ur1 = [float(x) for x in line.split()]
    o = base[(region, "electricity", "Single rate", "Direct Debit")]
    # cross-check: Oct-Dec figures in Ofgem's new table must match the earlier transcription
    assert (o["standing_charge_p_per_day"], o["unit_rate_p_per_kwh"]) == (sc0, ur0), region
    rows.append(dict(period_start=JAN_PERIOD[0], period_end=JAN_PERIOD[1], region=region, fuel="electricity",
        tariff="Single rate", payment_type="Direct Debit", standing_charge_p_per_day=sc1, unit_rate_p_per_kwh=ur1))
# --- Merge Ofgem's downloaded CSVs from data/raw/ (authoritative; cross-checked against transcription) ---
import glob, os, re
PAYMAP = [("direct_debit","Direct Debit"),("standard_credit","On receipt of bill (standard credit)"),("prepayment","Prepayment")]
key = lambda r: (r["period_start"], r["region"], r["fuel"], r["tariff"], r["payment_type"])
idx = {key(r): r for r in rows}
gb = []
num = lambda t: float(re.match(r"\s*([\d.]+)", t).group(1))
for path in sorted(glob.glob("data/raw/*.csv")):
    name = os.path.basename(path).lower()
    fuel = "electricity" if "electricity" in name else "gas"
    tariff = "Gas" if fuel == "gas" else ("Economy 7 (multi-rate)" if "multi-rate" in name else "Single rate")
    pay = next(p for k, p in PAYMAP if k in name.replace("direct_debit","direct_debit"))
    with open(path, newline="", encoding="utf-8-sig") as f:
        for rec in csv.reader(f):
            if rec[0] == "Region": continue
            sc0, sc1, ur0, ur1 = (num(x) for x in rec[1:5])
            if rec[0] == "Great Britain average":
                for per, sc, ur in ((PERIOD, sc0, ur0), (JAN_PERIOD, sc1, ur1)):
                    gb.append(dict(period_start=per[0], period_end=per[1], fuel=fuel, tariff=tariff, payment_type=pay,
                                   standing_charge_p_per_day=sc, unit_rate_p_per_kwh=ur))
                continue
            for per, sc, ur in ((PERIOD, sc0, ur0), (JAN_PERIOD, sc1, ur1)):
                new = dict(period_start=per[0], period_end=per[1], region=rec[0], fuel=fuel, tariff=tariff,
                           payment_type=pay, standing_charge_p_per_day=sc, unit_rate_p_per_kwh=ur)
                old = idx.get(key(new))
                if old:  # cross-check earlier transcription against Ofgem's own file
                    assert (old["standing_charge_p_per_day"], old["unit_rate_p_per_kwh"]) == (sc, ur), (name, rec[0], per)
                else:
                    rows.append(new); idx[key(new)] = new
assert len(rows) == 14*3*3*2 - 14, len(rows)   # all but Economy 7 / Direct Debit / Jan-Mar 2027
rows.sort(key=lambda r: (r["period_start"], r["fuel"], r["tariff"], r["payment_type"], REGIONS.index(r["region"])))
def write(name, rs):
    with open(f"data/{name}.csv","w",newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rs[0])); w.writeheader(); w.writerows(rs)
write("price_cap_rates_all", rows)
write("electricity_rates", [r for r in rows if r["fuel"]=="electricity"])
write("gas_rates", [r for r in rows if r["fuel"]=="gas"])
import csv as _c
with open("data/gb_averages.csv","w",newline="") as f:
    w=_c.DictWriter(f,fieldnames=list(gb[0])); w.writeheader(); w.writerows(gb)
json.dump(rows, open("data/price_cap_rates_all.json","w"), indent=2)
print(len(rows), "rows")
