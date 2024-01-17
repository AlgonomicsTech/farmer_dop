#import Web3
from eth_account import Account
from mnemonic import Mnemonic
from loguru import logger as log


log.add("logger.log", format="{time:YYYY-MM-DD | HH:mm:ss.SSS} | {level} \t| {line}:{function} | {message}")
#w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/6621569178a54c9cbb4fe6b06ee98a00'))


def create_wallet():
    wallet = Account.create()
    private_key = wallet._private_key.hex()
    address = wallet.address

    mnemo = Mnemonic("english")
    seed_phrase = mnemo.generate(strength=128)


    with open('data/wallets.txt', 'a') as file:
        file.write(f'{seed_phrase}:{private_key}:{address}\n')
        log.success(f"{address} | created successfully")







