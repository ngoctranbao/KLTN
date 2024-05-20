from libs import uniswap_graphql, features, ethplorer
import json
timestamp_of_day = (7 * 24 * 60 * 60 * 1000)

def pair_data_7d(pair_id: str, label: bool = False, days: int = 7):
    print(f"Fetching pair data for pair_id: {pair_id}")
    pair = uniswap_graphql.pair_by_id(pair_id=pair_id)
    token_index = features.token_index(pair=pair)
    token_id = pair[f'''token{token_index}''']['id']
    
    print("Fetching transactions (mints, burns, swaps)...")
    mints, burns, swaps = uniswap_graphql.txs_by_pair_id(pair_id=pair_id)
    mint_cnt, burn_cnt, swap_cnt = len(mints), len(burns), len(swaps)
    init_timestamp = features.init_timestamp(mints=mints)
    rugpull_timestamp, rugpull_change, is_rugpull, before_rugpull_Eth, after_rugpull_Eth,rugpull_method,rugpull_txId = 0,0, False, 0,0,'',-1

    if(label == True):
        print("Checking for rugpull...")
        rugpull_timestamp, rugpull_change, is_rugpull, before_rugpull_Eth, after_rugpull_Eth,rugpull_method,rugpull_txId = features.rugpull_timestamp(mints=mints, swaps=swaps, burns=burns, token_index=token_index)
        mints, burns, swaps = uniswap_graphql.txs_by_pair_id(pair_id=pair_id, after=init_timestamp, before=min(rugpull_timestamp, timestamp_of_day * days))
        mint_cnt, burn_cnt, swap_cnt = len(mints), len(burns), len(swaps)
    
    print("Fetching token info...")
    info = ethplorer.token_info(token_id=token_id)
    token_creator = info['owner'] if 'owner' in info else ""
    
    print("Fetching LP holders...")
    lp_holders = ethplorer.holders(pair_id)
    token_holders = ethplorer.holders(token_id=token_id)
    
    print("Calculating features...")
    lp_lock_ratio = features.lock_ratio(holders=lp_holders)
    (lp_avg, lp_std) = features.lp_distribution(holders=lp_holders)
    token_burn_ratio = features.burn_ratio(holders=lp_holders) 
    lp_creator_holding_ratio = features.creator_ratio(holders=lp_holders, creator_address=token_creator) 
    token_creator_holding_ratio = features.creator_ratio(holders=token_holders, creator_address=token_creator)
    
    last_timestamp = features.last_timestamp(mints=mints, burns=burns, swaps=swaps)
    init_timestamp = features.init_timestamp(mints=mints)
    active_period = int(last_timestamp) - int(init_timestamp)
    swap_in, swap_out = features.swap_io(swaps=swaps, token_index=token_index)
    total_tx = mint_cnt + swap_cnt + burn_cnt
    mint_ratio = mint_cnt / total_tx
    swap_ratio = swap_cnt / total_tx
    burn_ratio = burn_cnt / total_tx
    mint_mean_period = int(features.tx_mean_period(txs=mints, init_timestamp=init_timestamp))
    swap_mean_period = int(features.tx_mean_period(txs=swaps, init_timestamp=init_timestamp))
    burn_mean_period = int(features.tx_mean_period(txs=burns, init_timestamp=init_timestamp))
    swap_in_per_week = swap_in /((int(active_period) / (60* 60 * 24 * 7)) + 1) if int(active_period) != 0 else 0
    swap_out_per_week = swap_out /((int(active_period) / (60* 60 * 24 * 7)) + 1) if int(active_period) != 0 else 0
    mint_count_per_week = mint_cnt / ((int(active_period) / (60* 60 * 24 * 7)) + 1) if int(active_period) != 0 else 0
    burn_count_per_week = burn_cnt / ((int(active_period) / (60* 60 * 24 * 7)) + 1) if int(active_period) != 0 else 0
    
    print("Fetching data success!")
    raw_data = data = {
        'id': pair_id,
        'label': label,
        'mint_count_per_week': mint_count_per_week,
        'burn_count_per_week': burn_count_per_week,
        'mint_ratio': mint_ratio,
        'burn_ratio': burn_ratio,
        'swap_ratio': swap_ratio,
        'mint_mean_period': mint_mean_period / active_period if int(active_period) != 0 else 0,
        'swap_mean_period': swap_mean_period / active_period if int(active_period) != 0 else 0,
        'burn_mean_period': burn_mean_period / active_period if int(active_period) != 0 else 0,
        'swap_in_per_week': swap_in_per_week,
        'swap_out_per_week': swap_out_per_week,
        'swap_rate': swap_in / (swap_out + 1),
        'lp_avg': lp_avg,
        'lp_std': lp_std,
        'lp_creator_holding_ratio': lp_creator_holding_ratio,
        'lp_lock_ratio': lp_lock_ratio,
        'token_burn_ratio': token_burn_ratio,
        'token_creator_holding_ratio': token_creator_holding_ratio,
        'number_of_token_creation_of_creator': 1
    }
    return raw_data\
        
        
def pair_data_wod(pair_id: str, label: bool = False):
    print(f"Fetching pair data for pair_id: {pair_id}")
    pair = uniswap_graphql.pair_by_id(pair_id=pair_id)
    token_index = features.token_index(pair=pair)
    token_id = pair[f'''token{token_index}''']['id']
    
    print("Fetching transactions (mints, burns, swaps)...")
    mints, burns, swaps = uniswap_graphql.txs_by_pair_id(pair_id=pair_id)
    mint_cnt, burn_cnt, swap_cnt = len(mints), len(burns), len(swaps)
    init_timestamp = features.init_timestamp(mints=mints)
    rugpull_timestamp, rugpull_change, is_rugpull, before_rugpull_Eth, after_rugpull_Eth,rugpull_method,rugpull_txId = 0,0, False, 0,0,'',-1
    if(label == True):
        print("Checking for rugpull...")
        rugpull_timestamp, rugpull_change, is_rugpull, before_rugpull_Eth, after_rugpull_Eth,rugpull_method,rugpull_txId = features.rugpull_timestamp(mints=mints, swaps=swaps, burns=burns, token_index=token_index)
        mints, burns, swaps = uniswap_graphql.txs_by_pair_id(pair_id=pair_id, after=init_timestamp, before=rugpull_timestamp)
        mint_cnt, burn_cnt, swap_cnt = len(mints), len(burns), len(swaps)
    
    print("Fetching token info...")
    info = ethplorer.token_info(token_id=token_id)
    token_creator = info['owner'] if 'owner' in info else ""
    
    print("Fetching LP holders...")
    lp_holders = ethplorer.holders(pair_id)
    token_holders = ethplorer.holders(token_id=token_id)
    
    
    print("Calculating features...")
    lp_lock_ratio = features.lock_ratio(holders=lp_holders)
    (lp_avg, lp_std) = features.lp_distribution(holders=lp_holders)
    token_burn_ratio = features.burn_ratio(holders=lp_holders) 
    lp_creator_holding_ratio = features.creator_ratio(holders=lp_holders, creator_address=token_creator) 
    token_creator_holding_ratio = features.creator_ratio(holders=token_holders, creator_address=token_creator)
    
    last_timestamp = features.last_timestamp(mints=mints, burns=burns, swaps=swaps)
    init_timestamp = features.init_timestamp(mints=mints)
    active_period = int(last_timestamp) - int(init_timestamp)
    swap_in, swap_out = features.swap_io(swaps=swaps, token_index=token_index)
    total_tx = mint_cnt + swap_cnt + burn_cnt
    mint_ratio = mint_cnt / total_tx
    swap_ratio = swap_cnt / total_tx
    burn_ratio = burn_cnt / total_tx
    mint_mean_period = int(features.tx_mean_period(txs=mints, init_timestamp=init_timestamp))
    swap_mean_period = int(features.tx_mean_period(txs=swaps, init_timestamp=init_timestamp))
    burn_mean_period = int(features.tx_mean_period(txs=burns, init_timestamp=init_timestamp))
    swap_in_per_week = swap_in /((int(active_period) / (60* 60 * 24 * 7)) + 1) if int(active_period) != 0 else 0
    swap_out_per_week = swap_out /((int(active_period) / (60* 60 * 24 * 7)) + 1) if int(active_period) != 0 else 0
    mint_count_per_week = mint_cnt / ((int(active_period) / (60* 60 * 24 * 7)) + 1) if int(active_period) != 0 else 0
    burn_count_per_week = burn_cnt / ((int(active_period) / (60* 60 * 24 * 7)) + 1) if int(active_period) != 0 else 0
    
    print("Fetching data success!")
    raw_data = data = {
        'id': pair_id,
        'label': label,
        'mint_count_per_week': mint_count_per_week,
        'burn_count_per_week': burn_count_per_week,
        'mint_ratio': mint_ratio,
        'burn_ratio': burn_ratio,
        'swap_ratio': swap_ratio,
        'mint_mean_period': mint_mean_period / active_period if int(active_period) != 0 else 0,
        'swap_mean_period': swap_mean_period / active_period if int(active_period) != 0 else 0,
        'burn_mean_period': burn_mean_period / active_period if int(active_period) != 0 else 0,
        'swap_in_per_week': swap_in_per_week,
        'swap_out_per_week': swap_out_per_week,
        'swap_rate': swap_in / (swap_out + 1),
        'lp_avg': lp_avg,
        'lp_std': lp_std,
        'lp_creator_holding_ratio': lp_creator_holding_ratio,
        'lp_lock_ratio': lp_lock_ratio,
        'token_burn_ratio': token_burn_ratio,
        'token_creator_holding_ratio': token_creator_holding_ratio,
        'number_of_token_creation_of_creator': 1
    }
    print(json.dumps(data, indent=1))
    return raw_data
