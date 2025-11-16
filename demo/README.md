# Demo

Quick demonstration of the report pipeline without requiring Oracle or external services.

## Purpose

This demo shows the core functionality of the automated report pipeline using SQLite instead of Oracle, allowing quick evaluation without infrastructure setup.

## Requirements

- Python 3.8+
- openpyxl (included in main requirements.txt)

## Run Demo

From project root:
```bash
python demo/demo_report.py
```

## What It Does

1. Creates an in-memory SQLite database
2. Inserts 8 sample sales records
3. Queries the data
4. Calculates statistics (revenue, units, averages)
5. Generates a professional Excel report

## Output

- **File**: `demo/output/sales_report.xlsx`
- **Format**: Excel with headers and formatting
- **Data**: Sample sales transactions

## What This Demonstrates

- Excel generation with custom formatting
- Data extraction and processing
- Statistical calculations
- Professional output structure
- Clean architecture patterns

## Note

This demo uses SQLite for simplicity and portability. The production system:
- Uses Oracle database
- Processes thousands of records daily
- Includes email notifications
- Supports FTP transfers
- Has comprehensive error handling

## Example Output
```
DEMO: Automated Report Pipeline
============================================================

Creating demo database...
[OK] Inserted 8 sample records

Querying sales data...
[OK] Retrieved 8 records

Statistics:
  Total Revenue: $24,537.23
  Total Units: 113
  Average Sale: $3,067.15

Generating Excel report...
[OK] Report generated: demo/output/sales_report.xlsx
[INFO] File size: 5,234 bytes

============================================================
Demo completed successfully!
============================================================
```