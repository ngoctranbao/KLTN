swaps = '''
query Swaps($pair: String!, $first: Int, $skip: Int) {
    swaps(
        orderBy: timestamp
        orderDirection: asc
        first: $first
        skip: $skip
        where: { pair: $pair }
    ) {
        id
        pair {
            id
            token0 {
                symbol
            }
            token1 {
                symbol
            }
        }
        timestamp
        sender  
        from
        amount0In
        amount1In
        amount0Out
        amount1Out
        to
        logIndex
        amountUSD
    }
}
'''

burns = '''
query Burns($pair: String!, $first: Int, $skip: Int) {
    burns(
        orderBy: timestamp
        orderDirection: asc
        first: $first
        skip: $skip
        where: { pair: $pair }
    ) {
        id
        pair {
            id
            token0 {
                symbol
            }
            token1 {
                symbol
            }
        }
        timestamp
        liquidity
        sender
        amount0
        amount1
        to
        logIndex
        amountUSD
        needsComplete
        feeTo
        feeLiquidity
    }
}
'''

mints = '''
query Mints($pair: String!, $first: Int, $skip: Int) {
    mints(
        orderBy: timestamp
        orderDirection: asc
        first: $first
        skip: $skip
        where: { pair: $pair }
    ) {
        id
        pair {
            id
            token0 {
                symbol
            }
            token1 {
                symbol
            }
        }
        timestamp
        to
        liquidity
        sender
        amount0
        amount1
        logIndex
        amountUSD
        feeTo
        feeLiquidity
    }
}
'''

pair_by_id = '''
query ($pair: ID!){
    pair(id: $pair) {
        token0 {
            symbol
            id
        }
        token1 {
            symbol
            id
        }
        id
        reserve0
        reserve1
        totalSupply
        reserveETH
        reserveUSD
        trackedReserveETH
        token0Price
        token1Price
        volumeToken0
        volumeToken1
        volumeUSD
        untrackedVolumeUSD
        txCount
        createdAtTimestamp
        createdAtBlockNumber
        liquidityProviderCount
    }
}
'''

liquidity_snapshots = '''
query ($pair: String) {
    liquidityPositionSnapshots(
        where: { pair: $pair }
        orderBy: timestamp
        orderDirection: asc
        first: 1000
    ) {
        id
        pair {
            token0 {
                symbol
                id
            }
            id
            token1 {
                symbol
                id
            }
        }
        timestamp
        block
        token0PriceUSD
        token1PriceUSD
        reserve0
        reserve1
        reserveUSD
        liquidityTokenTotalSupply
        liquidityTokenBalance
    }
}
'''

pair_by_token = '''
query ($tokens: [String!]) {
    pairs(where: { 
        token0_in: $tokens,
        token1_in: $tokens
    }) {
        token0 {
            symbol
            id
        }
        token1 {
            symbol
            id
        }
        id
        reserve0
        reserve1
        totalSupply
        reserveETH
        reserveUSD
        trackedReserveETH
        token0Price
        token1Price
        volumeToken0
        volumeToken1
        volumeUSD
        untrackedVolumeUSD
        txCount
        createdAtTimestamp
        createdAtBlockNumber
        liquidityProviderCount
    }
}
'''