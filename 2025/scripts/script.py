import pandas as pd

def process_csv(input_file, output_file):
    """
    Process a CSV file by splitting the 'Name on badge' column into first and last names.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to the output CSV file
    """
    # Read the CSV file with UTF-8 encoding to handle special characters
    df = pd.read_csv(input_file, encoding='utf-8')
    
    # Split the name on the first space
    # Using str.split with n=1 to split only on the first space
    name_parts = df['Name on badge'].str.split(' ', n=1, expand=True)
    
    # Create new dataframe with the required columns
    processed_df = pd.DataFrame({
        'first name': name_parts[0],
        'last name': name_parts[1] if 1 in name_parts.columns else '',
        'affiliation': df['Affiliation']
    })
    
    # Handle cases where there's no space in the name (only first name)
    processed_df['last name'] = processed_df['last name'].fillna('')
    
    # Save to output file with UTF-8 encoding
    processed_df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Processed {input_file} -> {output_file}")
    print(f"Number of records: {len(processed_df)}")

def main():
    # Process normal.csv
    process_csv('normal.csv', 'normal_processed.csv')
    
    # Process reviewers.csv  
    process_csv('reviewers.csv', 'reviewers_processed.csv')
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()
