import requests

token_info_ethplorer_api_url = '''https://api.ethplorer.io/getAddressInfo/%s?apiKey=EK-4L18F-Y2jC1b7-9qC3N'''

holders_ethplorer_api_url = '''https://api.ethplorer.io/getTopTokenHolders/%s?apiKey=EK-4L18F-Y2jC1b7-9qC3N&limit=100'''

def token_info(token_id):
    response = requests.get(token_info_ethplorer_api_url % token_id)
    if(response.status_code == 200):
        return response.json()['tokenInfo']
    else:
      raise Exception('ETH plorer get failed. status code is {}.\n{}'.format(response.status_code,response.json()))

def holders(token_id):
    request_url = holders_ethplorer_api_url % token_id
    response = requests.get(request_url)
    if(response.status_code == 200):
        return response.json()["holders"]
    raise Exception('ETH plorer get failed. status code is {}.\n{}'.format(response.status_code,response.json()))
