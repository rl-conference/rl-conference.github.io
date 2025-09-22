from collections import defaultdict
import csv
import pandas as pd
import requests
from io import StringIO
from pathlib import Path

# Configuration
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1QPl_TQ0ZMyd_dBz9TNKEdUDNAm5vnPNvcI9jGFojiBs/export?format=csv&gid=1570614584"


# Configuration
GOOGLE_SHEET_URL_2 = "https://docs.google.com/spreadsheets/d/1QPl_TQ0ZMyd_dBz9TNKEdUDNAm5vnPNvcI9jGFojiBs/export?format=csv&gid=0"

def split_name(full_name):
    """Split a full name into first and last name"""
    if not full_name or pd.isna(full_name):
        return "", ""
    
    # Clean the name (strip whitespace)
    full_name = str(full_name).strip()
    
    # Split by whitespace
    name_parts = full_name.split()
    
    if len(name_parts) == 0:
        return "", ""
    elif len(name_parts) == 1:
        # Only one name provided, treat as first name
        return name_parts[0], ""
    elif len(name_parts) == 2:
        # First and last name
        return name_parts[0], name_parts[1]
    else:
        # Multiple names - first name is first part, last name is last part
        # Middle names are included with first name
        first_name = " ".join(name_parts[:-1])
        last_name = name_parts[-1]
        return first_name, last_name

def fetch_reviewer_data():
    """Fetch reviewer data from Google Sheet and extract into lists"""
    try:
        # Fetch the CSV data from Google Sheets
        response = requests.get(GOOGLE_SHEET_URL)
        response.raise_for_status()
        
        # Ensure proper encoding
        response.encoding = 'utf-8'
        
        # Read CSV data into pandas DataFrame
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, encoding='utf-8')
        
        # Extract the three columns into Python lists
        names = df['Name'].tolist()
        emails = df['Email'].tolist()
        types = df['Type'].tolist()
        
        # Split names into first and last names
        first_names = []
        last_names = []
        
        for name in names:
            first, last = split_name(name)
            first_names.append(first)
            last_names.append(last)
        
        # Print the lengths
        print(f"Reviewer sheet - Number of names: {len(names)}")
        print(f"Reviewer sheet - Number of first names: {len(first_names)}")
        print(f"Reviewer sheet - Number of last names: {len(last_names)}")
        print(f"Reviewer sheet - Number of emails: {len(emails)}")
        print(f"Reviewer sheet - Number of types: {len(types)}")
        
        return names, first_names, last_names, emails, types
        
    except Exception as e:
        print(f"Error fetching reviewer data: {e}")
        return [], [], [], [], []

def fetch_registration_data():
    """Fetch registration data from second Google Sheet"""
    try:
        # Fetch the CSV data from Google Sheets
        response = requests.get(GOOGLE_SHEET_URL_2)
        response.raise_for_status()
        
        # Ensure proper encoding
        response.encoding = 'utf-8'
        
        # Read CSV data into pandas DataFrame
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, encoding='utf-8')
        
        # Extract the columns into Python lists
        emails = df['Email'].tolist()
        names = df['Name'].tolist()
        affiliations = df['Affiliation'].tolist()
        dates = df['Date of registration'].tolist()
        
        # Split names into first and last names
        first_names = []
        last_names = []
        
        for name in names:
            first, last = split_name(name)
            first_names.append(first)
            last_names.append(last)
        
        # Print the lengths
        print(f"\nRegistration sheet - Number of names: {len(names)}")
        print(f"Registration sheet - Number of first names: {len(first_names)}")
        print(f"Registration sheet - Number of last names: {len(last_names)}")
        print(f"Registration sheet - Number of emails: {len(emails)}")
        print(f"Registration sheet - Number of affiliations: {len(affiliations)}")
        print(f"Registration sheet - Number of dates: {len(dates)}")
        
        return emails, names, first_names, last_names, affiliations, dates
        
    except Exception as e:
        print(f"Error fetching registration data: {e}")
        return [], [], [], [], [], []

def cross_reference_lists(reviewer_data, registration_data):
    """Cross-reference reviewer and registration data to find matches"""
    rev_names, rev_first_names, rev_last_names, rev_emails, rev_types = reviewer_data
    reg_emails, reg_names, reg_first_names, reg_last_names, reg_affiliations, reg_dates = registration_data
    
    full_matches = []  # Both first and last name match
    last_name_matches = []  # Only last name matches
    
    # Create dictionaries for reviewer names for efficient lookup
    reviewer_full_names = {}  # (first, last) -> list of reviewer info
    reviewer_last_names = {}  # last_name -> list of reviewer info
    
    for i in range(len(rev_first_names)):
        # Create full name combination for exact matching
        full_name_key = (rev_first_names[i].lower().strip(), rev_last_names[i].lower().strip())
        reviewer_info = {
            'name': rev_names[i],
            'first_name': rev_first_names[i],
            'last_name': rev_last_names[i],
            'email': rev_emails[i],
            'type': rev_types[i]
        }
        
        if full_name_key not in reviewer_full_names:
            reviewer_full_names[full_name_key] = []
        reviewer_full_names[full_name_key].append(reviewer_info)
        
        # Add last name for last-name-only matching
        if rev_last_names[i].strip():
            last_name_key = rev_last_names[i].lower().strip()
            if last_name_key not in reviewer_last_names:
                reviewer_last_names[last_name_key] = []
            reviewer_last_names[last_name_key].append(reviewer_info)
    
    # Check each registration entry
    for i in range(len(reg_names)):
        reg_first = reg_first_names[i].lower().strip()
        reg_last = reg_last_names[i].lower().strip()
        
        # Check for full name match (both first and last name)
        full_name_key = (reg_first, reg_last)
        if full_name_key in reviewer_full_names:
            for reviewer_info in reviewer_full_names[full_name_key]:
                match_data = {
                    'email': reg_emails[i],
                    'name': reg_names[i],
                    'first_name': reg_first_names[i],
                    'last_name': reg_last_names[i],
                    'affiliation': reg_affiliations[i],
                    'date': reg_dates[i],
                    'reviewer_name': reviewer_info['name'],
                    'reviewer_first_name': reviewer_info['first_name'],
                    'reviewer_last_name': reviewer_info['last_name'],
                    'reviewer_email': reviewer_info['email'],
                    'reviewer_type': reviewer_info['type']
                }
                full_matches.append(match_data)
        # Check for last name only match (and make sure it's not already a full match)
        elif reg_last and reg_last in reviewer_last_names:
            for reviewer_info in reviewer_last_names[reg_last]:
                match_data = {
                    'email': reg_emails[i],
                    'name': reg_names[i],
                    'first_name': reg_first_names[i],
                    'last_name': reg_last_names[i],
                    'affiliation': reg_affiliations[i],
                    'date': reg_dates[i],
                    'reviewer_name': reviewer_info['name'],
                    'reviewer_first_name': reviewer_info['first_name'],
                    'reviewer_last_name': reviewer_info['last_name'],
                    'reviewer_email': reviewer_info['email'],
                    'reviewer_type': reviewer_info['type']
                }
                last_name_matches.append(match_data)
    
    return full_matches, last_name_matches

if __name__ == "__main__":
    # Fetch data from both sheets
    print("Fetching reviewer data...")
    reviewer_data = fetch_reviewer_data()
    
    print("\nFetching registration data...")
    registration_data = fetch_registration_data()
    
    # Cross-reference the data
    print("\nCross-referencing data...")
    full_matches, last_name_matches = cross_reference_lists(reviewer_data, registration_data)
    
    # Display results
    print(f"\n=== RESULTS ===")
    print(f"Full matches (first + last name): {len(full_matches)}")
    print(f"Last name only matches: {len(last_name_matches)}")
    
    print("\n=== FULL MATCHES ===")
    for i, match in enumerate(full_matches, 1):
        print(f"{i}. Registration: {match['name']} | Reviewer: {match['reviewer_name']}")
        print(f"   Email: {match['email']}")
        print(f"   Affiliation: {match['affiliation']}")
        print(f"   Registration Date: {match['date']}")
        print()
    
    print("\n=== LAST NAME ONLY MATCHES ===")
    for i, match in enumerate(last_name_matches, 1):
        print(f"{i}. Registration: {match['name']} | Reviewer: {match['reviewer_name']}")
        print(f"   Email: {match['email']}")
        print(f"   Affiliation: {match['affiliation']}")
        print(f"   Registration Date: {match['date']}")
        print()
    
    # Write CSV files with proper UTF-8 encoding

    # Write full matches to "full matches.csv"
    with open("full matches.csv", "w", newline='', encoding="utf-8") as f_full:
        writer = csv.writer(f_full)
        writer.writerow(["email", "reviewer_name", "registration_name", "affiliation"])
        for match in full_matches:
            writer.writerow([match["email"], match["reviewer_name"], match["name"], match["affiliation"]])

    # Write partial matches to "partial matches.csv"
    with open("partial matches.csv", "w", newline='', encoding="utf-8") as f_partial:
        writer = csv.writer(f_partial)
        writer.writerow(["email", "reviewer_name", "registration_name", "affiliation"])
        for match in last_name_matches:
            writer.writerow([match["email"], match["reviewer_name"], match["name"], match["affiliation"]])

    # For partial matches, store names from both lists (reviewer and registration)
    # We'll add columns for both names: reviewer_name, registration_name
    with open("partial matches with both names.csv", "w", newline='', encoding="utf-8") as f_partial_both:
        writer = csv.writer(f_partial_both)
        writer.writerow(["email", "reviewer_name", "registration_name", "affiliation"])
        for match in last_name_matches:
            # Now we have both reviewer and registration names properly stored
            reviewer_name = match.get("reviewer_name", "")
            registration_name = match.get("name", "")  # This is the registration name
            writer.writerow([match["email"], reviewer_name, registration_name, match["affiliation"]])
       