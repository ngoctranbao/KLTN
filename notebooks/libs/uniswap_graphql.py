import requests
import concurrent.futures
from libs import query_template

def send_request(query, var):
    response = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2', 
                            json={
                                "query": query,
                                "variables": var
                            })
    # Kiểm tra mã trạng thái của phản hồi
    if response.status_code != 200:
        raise Exception(f'''Request failed: {response.status_code}, {response.json()}''')

    # Parse JSON response
    json_response = response.json()

    # Kiểm tra nếu JSON response có chứa trường 'errors'
    if 'errors' in json_response:
        raise Exception(f'''GraphQL error: {json_response['errors']}''')
    return response.json()

def mints_transaction(pair_id: str, after: int = 0, before: int = 99999999999) -> list:
    var = {
        'pair': pair_id,
        'skip': 0,
        'first': 1000,
        "after": after,
        "before": before,
    }
    response = send_request(query=query_template.mints, var=var)
    mints = response['data']['mints']
    while(len(response['data']['mints']) == 1000):
        var['skip'] += 1000
        response = send_request(query=query_template.mints, var=var)
        mints.extend(response['data']['mints'])
        if(var['skip'] == 5000):
            break
    return mints

def burns_transaction(pair_id: str, after: int = 0, before: int = 99999999999) -> list:
    var = {
        'pair': pair_id,
        'skip': 0,
        'first': 1000,
        "after": after,
        "before": before,
    }
    response = send_request(query=query_template.burns, var=var)
    mints = response['data']['burns']
    while(len(response['data']['burns']) == 1000):
        var['skip'] += 1000
        response = send_request(query=query_template.burns, var=var)
        mints.extend(response['data']['burns'])
        if(var['skip'] == 5000):
            break
    return response['data']['burns']

def swaps_transaction(pair_id: str, after: int = 0, before: int = 99999999999) -> list:
    var = {
        'pair': pair_id,
        'skip': 0,
        'first': 1000,
        "after": after,
        "before": before,
    }
    response = send_request(query=query_template.swaps, var=var)
    swaps = response['data']['swaps']
    while(len(response['data']['swaps']) == 1000):
        var['skip'] += 1000
        response = send_request(query=query_template.swaps, var=var)
        swaps.extend(response['data']['swaps'])
        if(var['skip'] == 5000):
            break
    return swaps
    

def txs_by_pair_id(pair_id: str, after: int = 0, before: int = 99999999999):
    # Định nghĩa các hàm sẽ thực thi song song
    def fetch_swaps():
        return swaps_transaction(pair_id, after, before)
    
    def fetch_burns():
        return burns_transaction(pair_id, after, before)
    
    def fetch_mints():
        return mints_transaction(pair_id, after, before)
    
    # Sử dụng ThreadPoolExecutor để thực thi các hàm trên các thread khác nhau
    with concurrent.futures.ThreadPoolExecutor() as executor:
        swaps_future = executor.submit(fetch_swaps)
        burns_future = executor.submit(fetch_burns)
        mints_future = executor.submit(fetch_mints)
        
        # Lấy kết quả từ các future
        swaps = swaps_future.result()
        burns = burns_future.result()
        mints = mints_future.result()
    
    return mints, burns, swaps


def pair_by_token(token: str):
    response = send_request(query=query_template.pair_by_token, var={
        "tokens": [
            "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            token
        ]
    })
    if(len(response["data"]["pairs"]) == 0):
        raise Exception(f'''Not found pair with token_id = {token}''')
    return response["data"]["pairs"][0]

def pair_by_id(pair_id: str):
    response = send_request(query=query_template.pair_by_id, var={
        "pair": pair_id
    })
    pair = response["data"]["pair"]
    if(pair == None):
        raise Exception(f'''Not valid pair_address: {pair_id}''')
    return pair

def liquidity_snapshots(pair_id: str):
    response = send_request(query=query_template.liquidity_snapshots, var={
        "pair": pair_id
    })
    snapshots = response['data']['liquidityPositionSnapshots']
    if(len(snapshots) == 0):
        raise Exception(f'''Not valid pair_id: {pair_id}''')
    return response['data']['liquidityPositionSnapshots']