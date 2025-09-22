from collections import defaultdict
import csv
import pandas as pd
import requests
from io import StringIO
from pathlib import Path
import sys
import re

# Ensure UTF-8 output for special characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1QPl_TQ0ZMyd_dBz9TNKEdUDNAm5vnPNvcI9jGFojiBs/export?format=csv&gid=1570614584"

def fetch_and_format_data():
    """Fetch data from Google Sheets and format as JavaScript arrays grouped by type"""
    
    try:
        # Fetch the CSV data
        response = requests.get(GOOGLE_SHEET_URL)
        response.raise_for_status()
        
        # Parse CSV data with proper encoding
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        
        # Group data by type
        grouped_data = df.groupby('Type')
        
        # Format as JavaScript arrays
        def format_js_array(arr, var_name):
            """Format a Python list as a JavaScript array"""
            # Escape quotes and handle None/NaN values while preserving Unicode
            formatted_items = []
            for item in arr:
                if pd.isna(item) or item is None:
                    formatted_items.append('""')
                else:
                    # Convert to string and handle Unicode properly
                    item_str = str(item)
                    # Only escape quotes and backslashes, preserve Unicode characters
                    escaped_item = item_str.replace('\\', '\\\\').replace('"', '\\"')
                    formatted_items.append(f'"{escaped_item}"')
            
            items_str = ', '.join(formatted_items)
            return f"const {var_name} = [{items_str}];"
        
        def clean_variable_name(type_name):
            """Convert type name to valid JavaScript variable name"""
            # Remove special characters and spaces, convert to camelCase
            clean_name = re.sub(r'[^a-zA-Z0-9]', '', str(type_name))
            return clean_name.lower()
        
        # Generate JavaScript code
        print("// Copy the following JavaScript code:")
        print("// Note: Special characters like 'Université Laval & Mila' are preserved")
        print()
        
        total_records = 0
        for type_name, group in grouped_data:
            var_prefix = clean_variable_name(type_name)
            names = group['Name'].tolist()
            
            print(f"// {type_name} ({len(names)} records)")
            print(format_js_array(names, f'{var_prefix}Names'))
            print()
            
            total_records += len(names)
        
        print(f"// Total records across all types: {total_records}")
        
    except Exception as e:
        print(f"Error fetching or processing data: {e}")

if __name__ == "__main__":
    fetch_and_format_data()

