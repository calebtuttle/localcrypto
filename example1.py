'''
Example simulation. Runs for 10 seconds.
'''

from localcrypto.crypto_essentials import (Transaction, Block, CoinBase, MiningNode, Wallet,
                                net_wide_txs, net_wide_blocks, nodes, user_addresses)
from localcrypto.simulate import MiningNodeThread, BenignUser, MaliciousUser


coinbase = CoinBase()

runtime = 20

user0 = BenignUser(runtime=runtime)
user0.name = 'BenignUser0'
user_addresses.append(user0.wallet.address)
tx0 = coinbase.generate_transaction(recipient=user0.wallet.address, amount=1)
net_wide_txs.append(tx0)
print(f'{user0.name} broadcasting... {tx0}')

user1 = BenignUser(runtime=runtime)
user1.name = 'BenignUser1'
user_addresses.append(user1.wallet.address)
tx1 = coinbase.generate_transaction(recipient=user1.wallet.address, amount=2)
net_wide_txs.append(tx1)
print(f'{user1.name} broadcasting... {tx1}')

user2 = MaliciousUser(runtime=runtime)
user2.name = 'MaliciousUser0'
user_addresses.append(user2.wallet.address)
tx2 = coinbase.generate_transaction(recipient=user2.wallet.address, amount=3)
net_wide_txs.append(tx2)
print(f'{user2.name} broadcasting... {tx2}')

user3 = BenignUser(runtime=runtime)
user3.name = 'BenignUser3'
user_addresses.append(user3.wallet.address)
tx3 = coinbase.generate_transaction(recipient=user3.wallet.address, amount=6)
net_wide_txs.append(tx3)
print(f'{user3.name} broadcasting... {tx3}')

genesis_block = Block(None, (tx0, tx1, tx2, tx3))

mining_node0 = MiningNodeThread(genesis_block=genesis_block, runtime=runtime)
mining_node0.name = 'MiningNode0'
nodes.append(mining_node0)

mining_node1 = MiningNodeThread(genesis_block=genesis_block, runtime=runtime)
mining_node1.name = 'MiningNode1'
nodes.append(mining_node1)

user0.start()
user1.start()
user2.start()
user3.start()
mining_node0.start()
mining_node1.start()

user0.join()
user1.join()
user2.join()
user3.join()
mining_node0.join()
mining_node1.join()

# Print identifying info and all transactions from mining_node0's main blockchain
print('-'*100)
print("mining_node0's blockchain...\n")
for b in mining_node0.main_blockchain:
    print(f'Block: {b}\n')
    for t in b.transactions:
        t.pretty_print()
        print()
    print()

# Print a comparison of the blockchains.
# Blockchains should be of equal length. Equal nonce values 
# indicate that a block is identical on each node's blockchain.
print('-'*100)
print('Comparing blocks...\n')
blockchain0 = mining_node0.main_blockchain
blockchain1 = mining_node1.main_blockchain
print(f'len(blockchain0): {len(blockchain0)}. len(blockchain1): {len(blockchain1)}')
for b0, b1 in zip(blockchain0, blockchain1):
    if b0.nonce != b1.nonce:
        print(f'b0.nonce != b1.nonce for blocks: {b0}\n{b1}')
    txs0 = b0.transactions
    txs1 = b1.transactions
    print(f'len(txs0): {len(txs0)}. len(txs1): {len(txs1)}')
    txs_same = [tx0 == tx1 for tx0, tx1 in zip(txs0, txs1)]
    print(txs_same)
    print()