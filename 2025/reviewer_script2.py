from collections import defaultdict
import pandas as pd
import requests
from io import StringIO
from pathlib import Path

# Configuration
ALL_ATTENDEES_SHEET = "https://docs.google.com/spreadsheets/d/1QPl_TQ0ZMyd_dBz9TNKEdUDNAm5vnPNvcI9jGFojiBs/export?format=csv&gid=0"
REVIEWER_AND_ATTENDEE_SHEET = "https://docs.google.com/spreadsheets/d/1QPl_TQ0ZMyd_dBz9TNKEdUDNAm5vnPNvcI9jGFojiBs/export?format=csv&gid=1736598300"

def read_google_sheet(url):
    """Read a Google Sheet from URL and return as DataFrame"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Explicitly set encoding to UTF-8 to handle special characters
        response.encoding = 'utf-8'
        df = pd.read_csv(StringIO(response.text))
        return df
    except Exception as e:
        print(f"Error reading sheet from {url}: {e}")
        return None

def main():
    print("Reading all attendees sheet...")
    all_attendees_df = read_google_sheet(ALL_ATTENDEES_SHEET)
    
    print("Reading reviewers and attendees sheet...")
    reviewers_df = read_google_sheet(REVIEWER_AND_ATTENDEE_SHEET)
    
    if all_attendees_df is None or reviewers_df is None:
        print("Failed to read one or both sheets")
        return
    
    print(f"Total attendees: {len(all_attendees_df)}")
    print(f"Total reviewers: {len(reviewers_df)}")
    
    # Use email as the key for comparison
    reviewer_emails = set(reviewers_df['Email'].str.lower().str.strip())
    
    # Filter out reviewers from all attendees
    normies_df = all_attendees_df[~all_attendees_df['Email'].str.lower().str.strip().isin(reviewer_emails)]
    
    print(f"Attendees who are NOT reviewers: {len(normies_df)}")
    
    # Save to CSV
    normies_df.to_csv('normies.csv', index=False)
    print("Results saved to 'normies.csv'")
    
    # Show first few rows for verification
    print("\nFirst 5 rows of normies.csv:")
    print(normies_df.head())

if __name__ == "__main__":
    main()

