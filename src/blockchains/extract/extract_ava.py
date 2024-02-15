from utils.handler.time import convert_to_gmt_timestamp
from utils.handler.http import fetch_transactions


def extract(date):
    # Convert the date to GMT timestamp and define the end timestamp for one day later

    try:
        start_timestamp = convert_to_gmt_timestamp(date)
        end_timestamp = start_timestamp + 86400  # 24 hours later
        url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/x-chain/transactions"

        # Initialize variables
        trxs, emitted_utxos, consumed_utxos = [], [], []
        params, page_token, run = {"pageSize": 100}, None, True

        # Fetch transactions in a loop until conditions are met
        while run:
            # Update parameters with the pageToken for pagination
            if page_token:
                params["pageToken"] = page_token

            # Fetch transactions data
            res_data = fetch_transactions(url, params)
            transactions = res_data.get('transactions', [])

            # Process each transaction
            for tx in transactions:
                timestamp, txHash, blockHash, txType = int(tx.get("timestamp")), tx.get('txHash', ''), tx.get(
                    'blockHash', ''), tx.get('txType', '')

                # Break the loop if transaction timestamp is before the start timestamp
                if timestamp < start_timestamp:
                    run = False
                    break

                # Process transactions within the desired timeframe
                if timestamp < end_timestamp:
                    trxs.append(tx)  # Add transaction to the list

                    # Process and append emitted UTXOs
                    emitted_utxos += [
                        {**e_utxo, 'txHash': txHash, 'blockHash': blockHash, 'txType': txType}
                        for e_utxo in tx.get('emittedUtxos', [])
                    ]
        
                    # Process and append consumed UTXOs
                    consumed_utxos += [
                        {**c_utxo, 'txHash': txHash, 'blockHash': blockHash, 'txType': txType}
                        for c_utxo in tx.get('consumedUtxos', [])
                    ]

            # Update the page token for the next iteration, or stop if there are no more pages
            page_token = res_data.get('nextPageToken')
            if not page_token:
                run = False

        return trxs, emitted_utxos, consumed_utxos

    except Exception as e:
        raise Exception(e)
