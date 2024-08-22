import csv
import pandas as pd
import argparse
from libs import uniswap_graphql

def scrape_pairs(source_file, destination_file):
    # Load the tokens DataFrame
    tokens = pd.read_csv(source_file)

    # Load existing IDs from the destination file into a set
    existing_ids = set()
    try:
        with open(destination_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            existing_ids = {row['id'] for row in reader}
    except FileNotFoundError:
        # If the file does not exist, we start with an empty set
        existing_ids = set()

    # Open the CSV file in append mode to write the new entries
    with open(destination_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'label'])
        
        # Iterate over the tokens DataFrame
        for index, token in tokens.iterrows():
            token_id = token["Id"]
            
            try:
                # Attempt to retrieve the pair information by token ID
                result = uniswap_graphql.pair_by_token(token_id)
                pair_id = result["id"]

                if pair_id in existing_ids:
                    print(f"Pair {pair_id} already exists. Skipping...")
                    continue
                
                pair_data = {'id': pair_id, 'label': False}
                
                # Append the result to the CSV file
                writer.writerow(pair_data)
                
                # Add the newly added ID to the set
                existing_ids.add(pair_id)
                
                print(f"Success for token {token_id}")
            except Exception as e:
                # Print the error message if an exception occurs
                print(f"Error processing token {token_id}: {e}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Scrape Uniswap pairs by token addresses.')
    parser.add_argument('-s', '--source', required=True, help='Path to the source token address file (CSV).')
    parser.add_argument('-d', '--destination', required=True, help='Path to the destination pair address file (CSV).')
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the scrape_pairs function with provided arguments
    scrape_pairs(args.source, args.destination)
