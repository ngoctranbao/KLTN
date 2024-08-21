from libs import coinmarketcap
import pandas as pd

limit = 1000
start = 1
filtered_data = []

while True:
    response = coinmarketcap.get_cryptocurrencies(query={
        "start": start,
        "limit": limit,
        "convert": "USD",
        # "tag": "defi"
    })

    for coin in response["data"]:
        if coin["platform"] is not None and coin["platform"]["id"] == 1027:
            filtered_data.append({
                'Id': coin["platform"]["token_address"], 
                'label': False
            })
    
    start += limit
    
    if len(response["data"]) < limit:
        break

df = pd.DataFrame(filtered_data)

df.to_csv("./datasets/coinmarketcap_tokens.csv", index=False)

print(df)
