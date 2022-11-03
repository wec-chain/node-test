from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests


def postTransaction(sender, receiver, amount, type):
    transaction = sender.createTransaction(
        receiver.publicKeyString(), amount, type)
    url = "http://localhost:5000/transaction"
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)


if __name__ == '__main__':

    maksim = Wallet()
    artem = Wallet()
    artem.fromKey('keys/stakerPrivateKey.pem')
    exchange = Wallet()

    #forger: genesis
    postTransaction(exchange, artem, 100, 'EXCHANGE')
    postTransaction(exchange, maksim, 100, 'EXCHANGE')
    postTransaction(exchange, maksim, 10, 'EXCHANGE')

    # forger: probably artem
    postTransaction(artem, artem, 25, 'STAKE')
    postTransaction(artem, maksim, 1, 'TRANSFER')
    postTransaction(maksim, artem, 30, 'TRANSFER')
