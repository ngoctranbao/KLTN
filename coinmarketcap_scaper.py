from libs import coinmarketcap
import pandas as pd
response = coinmarketcap.get_cryptocurrencies(query = {
        "start": 1,
        "limit": 1000,
        "convert": "USD",
        "tag": "defi"
    })
filtered_data = []
for coin in response["data"]:
    if(coin["platform"] != None and coin["platform"]["id"] == 1027):
        filtered_data.append({
            'id': coin["platform"]["token_address"], 
            'label': True
            })
df = pd.DataFrame(filtered_data)
df.to_csv("./datasets/coinmarketcap_tokens.csv", index=False)
print(df)
