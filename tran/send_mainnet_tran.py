from typing import Optional
from hexbytes import HexBytes
from web3 import Web3
from src.config import MNEMONIC
from src.config import private_key


def send_mainnet_tran(user_address):
    faucet_address = '0xf1782c522287b87Ce9c4545FeEA43DF26D28ef9E'  

    mainnet_rpc_url = "https://haqq-network.rpc.thirdweb.com"
    web3 = Web3(Web3.HTTPProvider(mainnet_rpc_url))
    
    web3.eth.account.enable_unaudited_hdwallet_features()
    account = web3.eth.account.from_mnemonic(MNEMONIC)

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
    from_address=faucet_address,
    to_address=user_address,
    amount=0.001,
    )

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return f'https://explorer.haqq.network/tx/{txn_hash.hex()}'