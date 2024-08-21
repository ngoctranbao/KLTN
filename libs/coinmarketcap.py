import requests

def send_request(url, headers, params=None, method='GET'):
    try:
        response = requests.request(method, url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return JSON response
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def get_cryptocurrencies(query):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        'accept': 'application/json',
        'X-CMC_PRO_API_KEY': 'c9f06853-5f96-4f85-8f90-cf4a0e4f7506'
    }
    params = query
    return send_request(url, headers, params=params)