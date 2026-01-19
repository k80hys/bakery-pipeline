"""
Upload all staging CSVs to Google Sheets automatically for Tableau Public dashboards.

Requirements:
- Install packages:
    pip install pandas gspread google-auth

- Place this script in your project folder.
- Make sure /staging-data/ contains:
    - all staging CSVs
    - credentials.json for your service account
- Make sure the service account email is shared with the Google Sheet "Cookie_Bakery"
"""

import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- Configuration ---
STAGING_DIR = 'staging-data'          # folder containing CSVs and credentials.json
GOOGLE_SHEET_NAME = 'Cookie_Bakery'   # your Google Sheet name

# --- Authenticate with Google Sheets API ---
creds_path = os.path.join(STAGING_DIR, 'credentials.json')
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
client = gspread.authorize(creds)

# --- Open the Google Sheet ---
try:
    sh = client.open(GOOGLE_SHEET_NAME)
    print(f'Connected to Google Sheet: "{GOOGLE_SHEET_NAME}"')
except gspread.SpreadsheetNotFound:
    sh = client.create(GOOGLE_SHEET_NAME)
    print(f'Created new Google Sheet: "{GOOGLE_SHEET_NAME}"')

# --- Loop through all CSVs in staging-data ---
for filename in os.listdir(STAGING_DIR):
    if filename.endswith('.csv'):
        csv_path = os.path.join(STAGING_DIR, filename)
        sheet_name = os.path.splitext(filename)[0]  # use CSV filename as sheet tab name
        df = pd.read_csv(csv_path)

        # Check if sheet exists; create if not
        try:
            worksheet = sh.worksheet(sheet_name)
            worksheet.clear()  # clear previous data
            print(f'Overwriting existing sheet tab: "{sheet_name}"')
        except gspread.WorksheetNotFound:
            # Make sure rows and cols are integers slightly bigger than df size
            worksheet = sh.add_worksheet(
                title=sheet_name, 
                rows=len(df)+10, 
                cols=len(df.columns)+5
            )
            print(f'Created new sheet tab: "{sheet_name}"')

        # Upload dataframe to sheet
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        print(f'Uploaded {filename} to Google Sheet tab "{sheet_name}"')