from localcrypto.crypto_essentials import MiningNode, Wallet, Block, CoinBase


NODE1_PORT = 5048

wallet1 = Wallet()
wallet2 = Wallet()

tx1 = CoinBase().generate_tx([wallet2.address], [2])
tx2 = CoinBase().generate_tx([wallet1.address], [700])

genesis_block = Block(prev_block_hash=None, transactions=(tx1, tx2))

node1 = MiningNode(genesis_block=genesis_block, PORT=NODE1_PORT)

node1.run()