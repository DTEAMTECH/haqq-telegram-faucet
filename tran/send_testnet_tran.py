from typing import Optional
from hexbytes import HexBytes
from web3 import Web3
from src.config import PRIVATE_KEY
from src.config import FAUCET_ADDRESS


def send_testnet_tran(user_address):
    testnet_rpc_url = "https://rpc.eth.testedge2.haqq.network"
    web3 = Web3(Web3.HTTPProvider(testnet_rpc_url))
    web3.eth.account.enable_unaudited_hdwallet_features()

    def build_txn(
    *,
    web3: Web3,
    from_address: str,  
    to_address: str, 
    amount: float, 
    ) -> dict[str, int | str]:
        
        gas_price = web3.eth.gas_price
        gas = 200_000  
        nonce = web3.eth.get_transaction_count(from_address)

        txn = {
        'chainId': web3.eth.chain_id,
        'from': from_address,
        'to': to_address,
        'value': int(Web3.to_wei(amount, 'ether')),
        'nonce': nonce, 
        'gasPrice': gas_price,
        'gas': gas,
        }

        return txn

    transaction = build_txn(
    web3=web3,
    from_address=FAUCET_ADDRESS,
    to_address=user_address,
    amount=0.001,
    )

    signed_txn = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return f'https://explorer.testedge2.haqq.network/tx/{txn_hash.hex()}'
