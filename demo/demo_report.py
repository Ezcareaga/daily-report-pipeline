#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script showing the report pipeline with SQLite.
No Oracle or external services required.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.excel import ExcelGenerator


def create_demo_database():
    """Create in-memory database with sample data."""
    print("Creating demo database...")
    
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            product TEXT,
            amount REAL,
            quantity INTEGER,
            sale_date DATE
        )
    """)
    
    demo_data = [
        (1, 'Laptop Dell XPS', 1299.99, 5, '2025-01-15'),
        (2, 'Mouse Logitech', 29.99, 15, '2025-01-15'),
        (3, 'Keyboard Mechanical', 89.99, 8, '2025-01-15'),
        (4, 'Monitor 27"', 349.99, 12, '2025-01-15'),
        (5, 'Webcam HD', 79.99, 20, '2025-01-15'),
        (6, 'Headset', 119.99, 10, '2025-01-15'),
        (7, 'USB Hub', 24.99, 25, '2025-01-15'),
        (8, 'Laptop Stand', 39.99, 18, '2025-01-15'),
    ]
    
    cursor.executemany(
        "INSERT INTO sales VALUES (?, ?, ?, ?, ?)",
        demo_data
    )
    
    conn.commit()
    print(f"[OK] Inserted {len(demo_data)} sample records")
    
    return conn


def generate_report():
    """Generate Excel report from database."""
    print("\n" + "="*60)
    print("DEMO: Automated Report Pipeline")
    print("="*60 + "\n")
    
    # Create database
    conn = create_demo_database()
    cursor = conn.cursor()
    
    # Query data
    print("\nQuerying sales data...")
    cursor.execute("""
        SELECT id, product, amount, quantity, sale_date
        FROM sales
        ORDER BY amount DESC
    """)
    
    data = cursor.fetchall()
    print(f"[OK] Retrieved {len(data)} records")
    
    # Calculate statistics
    total_revenue = sum(row[2] * row[3] for row in data)
    total_units = sum(row[3] for row in data)
    
    print(f"\nStatistics:")
    print(f"  Total Revenue: ${total_revenue:,.2f}")
    print(f"  Total Units: {total_units}")
    print(f"  Average Sale: ${total_revenue/len(data):,.2f}")
    
    # Generate Excel
    print(f"\nGenerating Excel report...")
    
    excel = ExcelGenerator()
    output = Path("demo/output/sales_report.xlsx")
    output.parent.mkdir(exist_ok=True)
    
    headers = ['ID', 'Product', 'Unit Price', 'Quantity', 'Date']
    excel.generate_excel(data, output, headers, sheet_name="Sales Report")
    
    print(f"[OK] Report generated: {output}")
    print(f"[INFO] File size: {output.stat().st_size:,} bytes")
    
    # Cleanup
    conn.close()
    
    print("\n" + "="*60)
    print("Demo completed successfully!")
    print("="*60)
    print(f"\nOutput file: {output.absolute()}")


if __name__ == "__main__":
    try:
        generate_report()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()