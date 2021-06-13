from cryptocurrency_simulator import Block, CoinBase, Wallet, MiningNode, MiningNodeThread

coinbase = CoinBase()
wallet1 = Wallet()
wallet2 = Wallet()
tx0 = coinbase.generate_transaction(recipient=wallet1.address, amount=5)
tx1 = coinbase.generate_transaction(recipient=wallet2.address, amount=7)
genesis_block = Block(prev_block_hash=None, transactions=(tx0, tx1))
mining_node1 = MiningNode(genesis_block=genesis_block)

tx2 = wallet1.new_transaction(inpt_tx=tx0, recipient=wallet2.address, amount=tx0.amount)
tx3 = wallet2.new_transaction(inpt_tx=tx1, recipient=wallet1.address, amount=tx1.amount)

mining_node1.receive_transaction(tx=tx2)
mining_node1.receive_transaction(tx=tx3)

new_block = mining_node1.mine_block()

print(mining_node1.main_blockchain)


# TODO: Test MiningNodeThread with implemented BenignUser class
node = MiningNodeThread(genesis_block, runtime=20)
node.start()
node.join()
print('node finished')