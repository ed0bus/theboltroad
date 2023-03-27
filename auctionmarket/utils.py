from web3 import Web3
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# connect to an alchemy node
def sendTransaction(message):
    alchemy_url = os.environ["WEB3_ALCHEMY_PROJECT"]
    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    address = "0x13Bbd129539e8a6610069423fed067b2534E723e"
    privateKey = os.environ["PRIVATE_KEY"]
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, "ether")
    signedTx = w3.eth.account.signTransaction(
        dict(
            nonce=nonce,
            gasPrice=gasPrice,
            gas=2000000,
            to="0x4Ca744cE314014C632C613A98c0B20511c08C0dc",
            value=value,
            data=message.encode("utf-8"),
        ),
        privateKey,
    )

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId
