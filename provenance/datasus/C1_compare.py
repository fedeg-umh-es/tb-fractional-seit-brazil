"""Reproduce the preregistered C1 monthly comparison without changing either input."""

import csv
import hashlib
import json
from datetime import date, datetime
from pathlib import Path

from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "provenance" / "datasus"
RAW = AUDIT / "raw" / "C1_datasus_tb_brazil_2001_2022.csv"
WORKBOOK = ROOT / "data" / "raw" / "tb_mes.xlsx"
EXPECTED_WORKBOOK_SHA256 = "93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b"
EXPECTED_RAW_SHA256 = "f9f801641d40c48330ee686af77bb3416044063f886a9306f480b89b4dd6f035"
MONTH_LABELS = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
EXPECTED_MONTHS = [f"{year:04d}-{month:02d}" for year in range(2001, 2023) for month in range(1, 13)]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tabnet_months():
    if sha256(RAW) != EXPECTED_RAW_SHA256:
        raise ValueError("C1 raw export SHA-256 differs from the access log")
    rows = list(csv.reader(RAW.open(encoding="latin-1", newline=""), delimiter=";"))
    if rows[0] != ["Ano Diagnóstico", *MONTH_LABELS, "Total"]:
        raise ValueError("Unexpected TabNet columns")
    if rows[-1] != ["&"]:
        raise ValueError("Expected TabNet trailing '&' marker is absent")
    if len(rows) != 25 or rows[-2][0] != "Total":
        raise ValueError("Unexpected TabNet year or total rows")
    values = {}
    for row in rows[1:-2]:
        if len(row) != 14 or not row[0].isdigit():
            raise ValueError(f"Malformed TabNet row: {row}")
        year = int(row[0])
        counts = [int(value) for value in row[1:13]]
        if sum(counts) != int(row[13]):
            raise ValueError(f"TabNet annual total differs for {year}")
        for month, count in enumerate(counts, 1):
            key = f"{year:04d}-{month:02d}"
            if key in values:
                raise ValueError(f"Duplicate TabNet month: {key}")
            values[key] = count
    if sum(values.values()) != int(rows[-2][-1]):
        raise ValueError("TabNet grand total differs from monthly sum")
    return values


def workbook_months():
    if sha256(WORKBOOK) != EXPECTED_WORKBOOK_SHA256:
        raise ValueError("Canonical workbook SHA-256 differs from the preregistration")
    book = load_workbook(WORKBOOK, read_only=True, data_only=True)
    try:
        sheet = book["dados"]
        cells = sheet.values
        header = next(cells)
        date_column, cases_column = header.index("data"), header.index("casos")
        values = {}
        for row in cells:
            observed_date, count = row[date_column], row[cases_column]
            if not isinstance(observed_date, (date, datetime)) or not isinstance(count, int):
                raise ValueError(f"Unexpected workbook date/count: {observed_date}, {count}")
            key = observed_date.strftime("%Y-%m")
            if key in values:
                raise ValueError(f"Duplicate workbook month: {key}")
            values[key] = count
        return values
    finally:
        book.close()


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["month", "casos_workbook", "casos_DATASUS", "difference_DATASUS_minus_workbook"])
        writer.writerows(rows)


def main():
    tabnet = tabnet_months()
    workbook = workbook_months()
    expected = set(EXPECTED_MONTHS)
    missing = sorted(expected - set(tabnet))
    extra = sorted(set(tabnet) - expected)
    if set(workbook) != expected:
        raise ValueError("Canonical workbook does not cover exactly the expected 264 months")
    comparison = [
        [month, workbook[month], tabnet[month], tabnet[month] - workbook[month]]
        for month in EXPECTED_MONTHS if month in tabnet
    ]
    mismatches = [row for row in comparison if row[3] != 0]
    metrics = {
        "ROWS_EXPECTED": len(EXPECTED_MONTHS),
        "ROWS_OBTAINED": len(tabnet),
        "MISSING_MONTHS": missing,
        "EXTRA_MONTHS": extra,
        "MISMATCH_MONTHS": len(mismatches),
        "MAX_ABS_DIFF": max((abs(row[3]) for row in comparison), default=0),
        "TOTAL_ABS_DIFF": sum(abs(row[3]) for row in comparison),
        "FIRST_MISMATCH": mismatches[0][0] if mismatches else None,
        "LAST_MISMATCH": mismatches[-1][0] if mismatches else None,
    }
    metrics["C1_RESULT"] = (
        "EXACT_MATCH" if metrics["MISMATCH_MONTHS"] == 0 and metrics["MAX_ABS_DIFF"] == 0
        and not missing and not extra and len(tabnet) == len(EXPECTED_MONTHS) else "NO_EXACT_MATCH"
    )
    write_csv(AUDIT / "C1_monthly_comparison.csv", comparison)
    write_csv(AUDIT / "C1_discrepant_months.csv", mismatches)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
