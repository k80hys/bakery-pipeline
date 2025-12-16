'''
Python script to determine the structure of the CSVs generated in the /source-data folder.
For each file:
1. Display column names, their data type, and number of rows
2. Show file encoding and delimiters used
3. Show 5 sample rows
4. Show basic statistics (mean, min, max) for numeric columns
5. Check for missing, NULL, NaN, -, and 0 values and display count per column
6. Check for duplicate rows and display count
'''

import pandas as pd
import os
import chardet

def inspect_csv(file_path):
    print(f"Inspecting file: {file_path}")
    
    # Determine file encoding and delimiter
    with open(file_path, 'rb') as f:
        rawdata = f.read(10000)
    result = chardet.detect(rawdata)
    encoding = result['encoding']
    
    with open(file_path, 'r', encoding=encoding) as f:
        sample = f.read(1024)
        delimiter = ',' if sample.count(',') > sample.count('\t') else '\t'
    
    # Load CSV
    df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)
    
    # Display column names, data types, and number of rows
    print("\nColumn Names and Data Types:")
    print(df.dtypes)
    print(f"\nNumber of Rows: {len(df)}")
    
    # Show 5 sample rows
    print("\nSample Rows:")
    print(df.head())
    
    # Basic statistics for numeric columns
    print("\nBasic Statistics for Numeric Columns:")
    print(df.describe())
    
    # Check for missing values
    print("\nMissing Values per Column:")
    missing_values = df.isnull().sum() + (df == '-').sum() + (df == 0).sum()
    print(missing_values[missing_values > 0])
    
    # Check for duplicate rows
    duplicate_count = df.duplicated().sum()
    print(f"\nNumber of Duplicate Rows: {duplicate_count}\n")

if __name__ == "__main__":
    source_data_folder = './source-data'
    
    # Create one consolidated inspection report
    with open('./source-data/consolidated_inspection_report.txt', 'w') as report_file:
        import sys
        original_stdout = sys.stdout
        
        for filename in os.listdir(source_data_folder):
            if filename.endswith('.csv'):
                file_path = os.path.join(source_data_folder, filename)
                
                # Print to console
                inspect_csv(file_path)
                print("=" * 80)  # Add separator between files
                
                # Write to consolidated report file
                sys.stdout = report_file
                inspect_csv(file_path)
                report_file.write("=" * 80 + "\n\n")  # Add separator between files in report
                sys.stdout = original_stdout    