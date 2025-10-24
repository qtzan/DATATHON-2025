#!/usr/bin/env python3
"""
Convert Excel files to CSV for easier reading
"""

import pandas as pd
import os

def convert_excel_to_csv():
    """Convert all Excel files to CSV format"""
    
    excel_files = [
        'BOLT UBC First Byte - Stadium Operations.xlsx',
        'BOLT UBC First Byte - Merchandise Sales.xlsx', 
        'BOLT UBC First Byte - Fanbase Engagement.xlsx'
    ]
    
    for excel_file in excel_files:
        if os.path.exists(excel_file):
            print(f"Converting {excel_file}...")
            
            # Read Excel file
            df = pd.read_excel(excel_file)
            
            # Create CSV filename
            csv_file = excel_file.replace('.xlsx', '.csv')
            
            # Save as CSV
            df.to_csv(csv_file, index=False)
            print(f"  → Saved as {csv_file}")
            print(f"  → Shape: {df.shape}")
            print(f"  → Columns: {list(df.columns)}")
            print()
        else:
            print(f"File not found: {excel_file}")

if __name__ == "__main__":
    convert_excel_to_csv()
