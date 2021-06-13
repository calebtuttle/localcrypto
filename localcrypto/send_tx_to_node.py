import socket

from localcrypto.crypto_essentials import MiningNode, Wallet, Block, CoinBase
from localcrypto import utils

NODE1_PORT = 5048

USER_PORT = 5050

wallet1 = Wallet()
wallet2 = Wallet()

tx1 = CoinBase().generate_tx([wallet2.address], [2])
tx2 = CoinBase().generate_tx([wallet1.address], [700])

tx3 = CoinBase().generate_tx([wallet1.address], [800])

genesis_block = Block(prev_block_hash=None, transactions=(tx1, tx2))


# connect to node
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostbyname(socket.gethostname()), NODE1_PORT))

utils.send(tx3, client_socket)

print('Press the return key to exit program')
input()