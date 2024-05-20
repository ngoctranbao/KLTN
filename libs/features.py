# from libs.constant import *
from libs import constant, uniswap_graphql
from math import sqrt
from decimal import Decimal

def tx_key_word(token_index: int):
    eth_amount = ['amount1', 'amount0']
    eth_amountIn = ['amount1In', 'amount0In']
    eth_amountOut = ['amount1Out', 'amount0Out']
    token_amount = ['amount0', 'amount1']
    token_amountIn = ['amount0In', 'amount1In']
    token_amountOut = ['amount0Out', 'amount1Out']
    
    return (eth_amount[token_index], eth_amountIn[token_index], eth_amountOut[token_index], 
            token_amount[token_index], token_amountIn[token_index], token_amountOut[token_index])

def token_index(pair: object) -> int:
    if(pair['token0']['symbol'] == "WETH"):
        return 1
    else:
        return 0

def init_liquidity(mints: list, token_index: int) -> tuple[Decimal, Decimal]:
    eth_amount, eth_amountIn, eth_amountOut, token_amount, token_amountIn, token_amountOut = tx_key_word(token_index=token_index)    
    initial_liquidity_ETH = mints[0][eth_amount]
    initial_liquidity_token = mints[0][token_amount]
    return Decimal(initial_liquidity_ETH), Decimal(initial_liquidity_token)

def swap_io(token_index: int, swaps: list) -> tuple[int, int]:
    eth_amount, eth_amountIn, eth_amountOut, token_amount, token_amountIn, token_amountOut = tx_key_word(token_index=token_index)    
    swapIn = 0
    swapOut = 0
    for swap in swaps:
        if(swap[token_amountIn] == '0'):
            swapOut += 1
        else: 
            swapIn += 1
    return (swapIn, swapOut)

def last_timestamp(mints: list, burns: list, swaps: list) -> int:
    last_mint = mints[-1]['timestamp']
    last_burn = burns[-1]['timestamp'] if len(burns) > 0 else 0
    last_swap = swaps[-1]['timestamp'] if len(swaps) > 0 else 0
    
    return max(last_mint, max(last_burn, last_swap))

def init_timestamp(mints: list) -> int:
    return mints[0]['timestamp']

def tx_mean_period(txs: list, init_timestamp: int) -> float:
    cnt = len(txs)
    if(cnt == 0):
        return 0
    time = 0
    for mint in txs:
        time = time + (int(mint['timestamp']) - int(init_timestamp))
    return time / cnt

def lock_ratio(holders):
   for holder in holders:
      if(holder['address'] in constant.locker_address):
         return holder['share']
   return 0

def lp_distribution(holders):
    count = 0
    for holder in holders:
        if(holder['share'] < 0.01 ):
            break
        count = count + 1
    LP_avg = 100 / count if count != 0  else 0
    var = 0
    for i in range(count):
        var = var + (holders[i]['share'] - LP_avg) ** 2
    LP_stdev = sqrt(var)
    return LP_avg,LP_stdev

def creator_ratio(holders,creator_address):
   for holder in holders:
      if(holder['address'] == creator_address):
         return holder['share']
   return 0

def burn_ratio(holders):
   for holder in holders:
      if(holder['address'] in constant.burn_address):
         return holder['share']
   return 0

def tx_timestamp(transactions: list,index: int) -> int:
  try:
    return transactions[index]['timestamp']
  except:
    return '99999999999'

def check_rugpull(before_transaction_eth: Decimal, current_liquidity_eth: Decimal) -> bool:
    # Kiểm tra tỷ lệ và giá trị âm trong một điều kiện duy nhất
    if ( abs(current_liquidity_eth / before_transaction_eth) <= 0.01 and before_transaction_eth >= 0 or current_liquidity_eth >= 0 ):
        return True
    else:
        return False

# Maximal Extractable Value
def is_MEV(initial_liquidity_token: Decimal, swapIn_token: Decimal) -> bool:
    if(swapIn_token > initial_liquidity_token * 5):
        return False
    else:
        return True

def swap_token(swaps: list,j: int,token_index: int) -> Decimal:
    eth_amount, eth_amountIn, eth_amountOut, token_amount, token_amountIn, token_amountOut = tx_key_word(token_index=token_index)
    swap_amount = Decimal(swaps[j][token_amountIn])
    swap_amount = Decimal(swap_amount) - Decimal(swaps[j][token_amountOut])
    return swap_amount

def swap_txAmount(swaps: list,j: int,eth_amountIn: Decimal, eth_amountOut: Decimal) -> Decimal:
    if(swaps[j][eth_amountIn] == '0'):
        return Decimal(swaps[j][eth_amountOut]) * (-1)
    else:
        return Decimal(swaps[j][eth_amountIn])

def rugpull_timestamp(mints,swaps,burns,token_index):
    eth_amount, eth_amountIn, eth_amountOut, token_amount, token_amountIn, token_amountOut = tx_key_word(token_index=token_index)
    swap_count,burn_count = len(swaps), len(burns)
    current_liquidity_eth, initial_Liquidity_token = init_liquidity(mints,token_index)

    i,j,k = 1,0,0
    
    while True:
        next_timestamp = min(tx_timestamp(mints,i),tx_timestamp(burns,k))
        while(tx_timestamp(swaps,j) <= next_timestamp ):
            if(tx_timestamp(swaps,j) == '99999999999'):
                break

            before_tx_eth = current_liquidity_eth
            current_liquidity_eth = current_liquidity_eth + swap_txAmount(swaps,j,eth_amountIn,eth_amountOut)
            if( check_rugpull(before_tx_eth,current_liquidity_eth) ):
                if( is_MEV(initial_Liquidity_token,swap_token(swaps,j,token_index)) == False ):
                    return tx_timestamp(swaps,j), Decimal(current_liquidity_eth / before_tx_eth) -1, True, before_tx_eth,current_liquidity_eth,'swap',swaps[j]['id']      
            j = j+1
        if(next_timestamp == tx_timestamp(mints,i)):
            if(next_timestamp == '99999999999'):
                try:
                    if(swap_count == 0 and burn_count == 0):
                        return mints[-1]['timestamp'],0, False, 0,0,'',-1
                    if(swap_count == 0):
                        return max(mints[-1]['timestamp'],burns[-1]['timestamp']),0,False, 0,0,'',-1
                    if(burn_count == 0):
                        return max(mints[-1]['timestamp'],swaps[-1]['timestamp']),0,False, 0,0,'',-1
                    return max(mints[-1]['timestamp'],burns[-1]['timestamp'],swaps[-1]['timestamp']),0,False, 0,0,'',-1
                except:
                    return 'Error occur',100.0,False,1,1,'',-1
            before_tx_eth = current_liquidity_eth
            current_liquidity_eth = current_liquidity_eth + Decimal(mints[i][eth_amount])
            i = i+1
        else:
            before_tx_eth = current_liquidity_eth
            current_liquidity_eth = current_liquidity_eth - Decimal(burns[k][eth_amount])
            if(check_rugpull(before_tx_eth,current_liquidity_eth)):
                return tx_timestamp(burns,k), Decimal(current_liquidity_eth / before_tx_eth) -1, True, before_tx_eth,current_liquidity_eth,'burn',burns[k]['id']
            k = k+1
            
def check_rugpull_by_liquidity_snapshots(pair_id: str):
    snapshots = uniswap_graphql.liquidity_snapshots(pair_id=pair_id)
    token_id = token_index(snapshots[0]['pair'])
    before_price_usd = 0
    for snapshot in snapshots:
        current_price_usd = Decimal(snapshot[f'''token{token_id}PriceUSD'''])
        if(before_price_usd > 0 and current_price_usd >= 0 and current_price_usd/before_price_usd <= 0.01):
            return True, snapshot['timestamp']
        before_price_usd = current_price_usd
    return False, '0'