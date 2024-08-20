import csv
from libs import uniswap_graphql
import pandas as pd

# Load the tokens DataFrame
tokens = pd.read_csv("./datasets/tokens.csv")

# Define the output file path
output_file = "./datasets/new_pairs.csv"

# Open the CSV file in write mode to write the header
with open(output_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['id', 'label'])
    writer.writeheader()

# Iterate over the tokens DataFrame
for index, token in tokens.iterrows():
    try:
        # Attempt to retrieve the pair information by token ID
        result = uniswap_graphql.pair_by_token(token["Id"])
        pair_data = {'id': result["id"], 'label': False}
        
        # Append the result to the CSV file
        with open(output_file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'label'])
            writer.writerow(pair_data)
        
        print("Success")
    except Exception as e:
        # Print the error message if an exception occurs
        print(f"Error processing token {token['Id']}: {e}")
