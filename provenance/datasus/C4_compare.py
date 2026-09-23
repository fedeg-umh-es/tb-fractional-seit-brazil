"""Compare the fixed C4 TabNet output with the canonical monthly cases series."""

import csv
import hashlib
import json
from datetime import date, datetime
from pathlib import Path

from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "provenance" / "datasus"
RAW = AUDIT / "raw" / "C4_datasus_tb_brazil_2001_2022.csv"
WORKBOOK = ROOT / "data" / "raw" / "tb_mes.xlsx"
EXPECTED_WORKBOOK_SHA256 = "93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b"
EXPECTED_RAW_SHA256 = "f845d711265ac843d93e83060fe46df7617446c64fe06f055ee0e55348c62b90"
MONTH_LABELS = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
EXPECTED_MONTHS = [f"{year:04d}-{month:02d}" for year in range(2001, 2023) for month in range(1, 13)]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def count(cell):
    return 0 if cell == "-" else int(cell)


def tabnet_months():
    if sha256(RAW) != EXPECTED_RAW_SHA256:
        raise ValueError("C4 captured output SHA-256 differs from the access log")
    with RAW.open(encoding="latin-1", newline="") as handle:
        rows = list(csv.reader(handle, delimiter=";"))
    if rows[0] != ["Ano In. Tratamento", "Ign/Em Branco", *MONTH_LABELS, "Total"]:
        raise ValueError("Unexpected TabNet columns")
    if rows[-1] != ["&"] or rows[-2][0] != "Total":
        raise ValueError("Expected TabNet total and terminal marker are absent")
    dated = {}
    undated_year_total = 0
    source_sum = 0
    for row in rows[1:-2]:
        if len(row) != 15:
            raise ValueError(f"Malformed TabNet row: {row}")
        cells = [count(cell) for cell in row[1:14]]
        row_total = count(row[14])
        if sum(cells) != row_total:
            raise ValueError(f"TabNet row total differs for {row[0]}")
        source_sum += row_total
        if row[0] in {"Em Branco/ign", "<1975"}:
            undated_year_total += row_total
            continue
        if not row[0].isdigit():
            raise ValueError(f"Unexpected treatment-start year: {row[0]}")
        if cells[0] != 0:
            raise ValueError(f"Undated treatment-start month in dated year {row[0]}")
        year = int(row[0])
        for month, value in enumerate(cells[1:], 1):
            key = f"{year:04d}-{month:02d}"
            if key in dated:
                raise ValueError(f"Duplicate TabNet month: {key}")
            dated[key] = value
    if source_sum != count(rows[-2][-1]):
        raise ValueError("TabNet grand total differs from row totals")
    return dated, undated_year_total, source_sum


def workbook_months():
    if sha256(WORKBOOK) != EXPECTED_WORKBOOK_SHA256:
        raise ValueError("Canonical workbook SHA-256 differs from preregistration")
    book = load_workbook(WORKBOOK, read_only=True, data_only=True)
    try:
        sheet = book["dados"]
        cells = sheet.values
        header = next(cells)
        date_column, cases_column = header.index("data"), header.index("casos")
        values = {}
        for row in cells:
            observed_date, value = row[date_column], row[cases_column]
            if not isinstance(observed_date, (date, datetime)) or not isinstance(value, int):
                raise ValueError(f"Unexpected workbook date/count: {observed_date}, {value}")
            key = observed_date.strftime("%Y-%m")
            if key in values:
                raise ValueError(f"Duplicate workbook month: {key}")
            values[key] = value
        return values
    finally:
        book.close()


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["month", "casos_workbook", "casos_DATASUS", "difference_DATASUS_minus_workbook"])
        writer.writerows(rows)


def main():
    tabnet, undated_year_total, source_total = tabnet_months()
    workbook = workbook_months()
    expected = set(EXPECTED_MONTHS)
    if set(workbook) != expected:
        raise ValueError("Canonical workbook does not cover exactly the expected 264 months")
    missing = sorted(expected - set(tabnet))
    extra = sorted(set(tabnet) - expected)
    comparison = [
        [month, workbook[month], tabnet[month], tabnet[month] - workbook[month]]
        for month in EXPECTED_MONTHS if month in tabnet
    ]
    mismatches = [row for row in comparison if row[3] != 0]
    metrics = {
        "ROWS_EXPECTED": len(EXPECTED_MONTHS),
        "ROWS_OBTAINED": len(comparison),
        "MISSING_MONTHS": missing,
        "EXTRA_MONTHS": extra,
        "MISMATCH_MONTHS": len(mismatches),
        "MAX_ABS_DIFF": max((abs(row[3]) for row in comparison), default=0),
        "TOTAL_ABS_DIFF": sum(abs(row[3]) for row in comparison),
        "FIRST_MISMATCH": mismatches[0][0] if mismatches else None,
        "LAST_MISMATCH": mismatches[-1][0] if mismatches else None,
        "SOURCE_DATED_MONTHS": len(tabnet),
        "SOURCE_UNDATED_YEAR_TOTAL": undated_year_total,
        "SOURCE_GRAND_TOTAL": source_total,
        "TARGET_MONTHLY_TOTAL": sum(row[2] for row in comparison),
        "OUT_OF_WINDOW_DATED_TOTAL": sum(tabnet[month] for month in extra),
    }
    metrics["C4_RESULT"] = (
        "EXACT_MATCH" if not missing and len(comparison) == len(EXPECTED_MONTHS)
        and metrics["MISMATCH_MONTHS"] == 0 and metrics["MAX_ABS_DIFF"] == 0
        else "NO_EXACT_MATCH"
    )
    write_csv(AUDIT / "C4_monthly_comparison.csv", comparison)
    write_csv(AUDIT / "C4_discrepant_months.csv", mismatches)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
