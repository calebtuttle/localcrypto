'''
A full node (a) stores a full blockchain, (b) mines blocks, (c) verifies 
and propogates blocks and transactions, and (d) can send transactions.
'''
import socket
import threading

from localcrypto.crypto_essentials import (Transaction, Block, CoinBase, MiningNode, Wallet, 
                                            net_wide_txs, net_wide_blocks, nodes, user_addresses)


IP_ADDRESS = socket.gethostbyname(socket.gethostname())

# TODO: allow user to specify which port this socket runs on
# print('Specify the port you would like this node to run on:')
# PORT = input()
# ADDR = (IP_ADDRESS, PORT)

# TODO: Thread for routing (i.e., propogating blocks and transactions, handling requests from other nodes)

# TODO: Thread for mining

# TODO: Thread for sending transactions

