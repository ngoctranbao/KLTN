import csv
import pandas as pd
import argparse
from libs import uniswap_graphql

def scrape_pairs(source_file, destination_file):
    # Load the tokens DataFrame
    tokens = pd.read_csv(source_file)

    # Open the CSV file in write mode to write the header
    with open(destination_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'label'])
        writer.writeheader()

    # Iterate over the tokens DataFrame
    for index, token in tokens.iterrows():
        try:
            # Attempt to retrieve the pair information by token ID
            result = uniswap_graphql.pair_by_token(token["Id"])
            pair_data = {'id': result["id"], 'label': False}
            
            # Append the result to the CSV file
            with open(destination_file, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['id', 'label'])
                writer.writerow(pair_data)
            
            print(f"Success for token {token['Id']}")
        except Exception as e:
            # Print the error message if an exception occurs
            print(f"Error processing token {token['Id']}: {e}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Scrape Uniswap pairs by token addresses.')
    parser.add_argument('-s', '--source', required=True, help='Path to the source token address file (CSV).')
    parser.add_argument('-d', '--destination', required=True, help='Path to the destination pair address file (CSV).')
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the scrape_pairs function with provided arguments
    scrape_pairs(args.source, args.destination)
