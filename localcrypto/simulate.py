'''
This module contains the threading classes used to simulate a cryptocurrency: 
Simulator, MiningNodeThread, BenignUser, and MaliciousUser.
'''

import threading
import random
import time

from localcrypto.crypto_essentials import Block, CoinBase, MiningNode, Wallet, net_wide_txs, net_wide_blocks, nodes, user_addresses
# from crypto_essentials import Transaction 
from localcrypto.utils import print_blockchain_comparison

class Simulator(threading.Thread):
    def __init__(self, runtime=10, num_mining_nodes=1, num_benign_users=2, num_malicious_users=0, 
                                benign_users_init_amount=[1, 2], malicious_users_init_amount=[]):
        '''
        benign_users_init_amount : list
            The ith element in this list indicates the number of crypto the ith benign user starts with
        malicious_users_init_amount : list
            The ith element in this list indicates the number of crypto the ith malicious user starts with
        '''
        threading.Thread.__init__(self)

        self.runtime = runtime
        self.num_mining_nodes = num_mining_nodes
        self.num_benign_users = num_benign_users
        self.num_malicious_users = num_malicious_users
        self.benign_users_init_amount = benign_users_init_amount
        self.malicious_users_init_amount = malicious_users_init_amount
        # TODO: Type check each element in benign_users_init_amount and in malicious_users_init_amount

    def new_benign_user(self, runtime, name='BenignUser', starting_amount=1):
        user = BenignUser(runtime=runtime)
        user.name = name
        user_addresses.append(user.wallet.address)
        tx = CoinBase().generate_transaction(recipient=user.wallet.address, amount=starting_amount)
        net_wide_txs.append(tx)
        return user

    def new_malicious_user(self, runtime, name='MaliciousUser', starting_amount=1):
        user = MaliciousUser(runtime=runtime)
        user.name = name
        user_addresses.append(user.wallet.address)
        tx = CoinBase().generate_transaction(recipient=user.wallet.address, amount=starting_amount)
        net_wide_txs.append(tx)
        return user

    def new_mining_node(self, runtime, genesis_block, name='MiningNode'):
        node = MiningNodeThread(genesis_block=genesis_block, runtime=runtime)
        node.name = name
        nodes.append(node)
        return node

    def run(self):
        benign_users = []
        for i in range(self.num_benign_users):
            starting_amount = self.benign_users_init_amount[i]
            user = self.new_benign_user(runtime=self.runtime, name=f'BenignUser{i}', starting_amount=starting_amount)
            benign_users.append(user)

        malicious_users = []
        for i in range(self.num_malicious_users):
            starting_amount = self.malicious_users_init_amount[i]
            user = self.new_malicious_user(runtime=self.runtime, name=f'MaliciousUser{i}', starting_amount=starting_amount)
            malicious_users.append(user)

        initial_txs = tuple(net_wide_txs)
        genesis_block = Block(None, initial_txs)

        mining_nodes = []
        for i in range(self.num_mining_nodes):
            node = self.new_mining_node(runtime=self.runtime, genesis_block=genesis_block, name=f'MiningNode{i}')
            mining_nodes.append(node)

        threads = benign_users + malicious_users + mining_nodes
        for t in threads:
            print(f'starting... {t}')
            t.start()
        for t in threads:
            t.join()

        print_blockchain_comparison(mining_nodes) # TODO: Test this


class MiningNodeThread(MiningNode, threading.Thread):
    def __init__(self, genesis_block, runtime=10):
        '''
        runtime : float
            The length of time (in seconds) during which the thread runs
        '''
        threading.Thread.__init__(self)
        MiningNode.__init__(self, genesis_block)
        self.runtime = runtime

    def receive_transactions(self):
        '''
        NOTE: This method is a placeholder for a potentially 
        better implementation.
        '''
        for tx in net_wide_txs:
            self.receive_transaction(tx)

    def receive_blocks(self):
        new_blocks = False
        for b in net_wide_blocks:
            if self.receive_block(b):
                new_blocks = True
        return new_blocks

    def run(self):
        finish_time = time.time() + self.runtime
        while time.time() < finish_time:
            self.receive_transactions()
            
            candidate_block = self.mine_block()
            # if candidate_block:
            #     self.propagate_block(candidate_block) # This is handled in mine_block()
            
            # Receive other nodes' candidate blocks
            new_blocks = self.receive_blocks()

            # Move any orphan blocks whose parents have been found
            # to main_blockchain or branch_blocks
            if new_blocks:
                self.migrate_orphans()

            # TODO: Check branch_blocks for a blockchain better than main_blockchain

            # Compare internal blockchain with other nodes' blockchains and
            # replace current blockchain if better blockchain is found
            best_blockchain = self.get_best_blockchain()
            if best_blockchain:
                # print(f'{self.name} replacing its main_blockchain at block{len(self.main_blockchain)-1}...')  # TODO: Delete this line
                self.main_blockchain = best_blockchain


class UserBase(threading.Thread):
    def __init__(self, runtime=10):
        '''
        runtime : float
            The length of time (in seconds) during which the thread runs
        '''
        threading.Thread.__init__(self)
        self.runtime = runtime
        self.wallet = Wallet()

    def get_random_recipient(self):
        ''' Return a random user address other than self.wallet.address '''
        self_index = user_addresses.index(self.wallet.address)
        potential_recipients = user_addresses[0:self_index] + user_addresses[self_index+1:]
        rand_index = random.randrange(len(potential_recipients))
        return potential_recipients[rand_index]
        
class BenignUser(UserBase):
    '''
    A benign user broadcasts honest transactions.
    '''
    def __init__(self, runtime):
        super().__init__(runtime=runtime)
        
    def run(self):
        '''
        Broadcast transactions.
        '''
        finish_time = time.time() + self.runtime
        while time.time() < finish_time:
            # Wait for there to be another user
            if len(user_addresses) < 2:
                continue

            unspent_txs = self.wallet.get_unspent_txs()
            if not unspent_txs:
                continue

            for tx in unspent_txs:
                amount = tx.amount
                recipient = self.get_random_recipient()
                
                new_tx = self.wallet.generate_tx(inpt_tx=tx, 
                                                 recipient=recipient, 
                                                 amount=amount)
                net_wide_txs.append(new_tx)
                
                # print(f'{self.name} broadcasting... {new_tx}')
            
            delay_seconds = random.randrange(0, 2)
            time.sleep(delay_seconds)

            
class MaliciousUser(UserBase):
    '''
    A malicious user broadcasts digitally signed transactions to other 
    users but sometimes tries to spend crypto it doesn't have.
    '''
    def __init__(self, runtime):
        super().__init__(runtime=runtime)
        
    def run(self):
        '''
        Broadcast transactions.
        '''
        finish_time = time.time() + self.runtime
        while time.time() < finish_time:
            # Wait for there to be another user
            if len(user_addresses) < 2:
                continue

            unspent_txs = self.wallet.get_unspent_txs()
            if not unspent_txs:
                continue

            for tx in unspent_txs:
                amount = tx.amount
                recipient = user_addresses[random.randrange(len(user_addresses))]
                
                if round(time.time()) % 3 == 0:
                    new_tx = self.wallet.generate_tx(inpt_tx=tx, 
                                                    recipient=recipient, 
                                                    amount=amount+1) # 
                else:
                    new_tx = self.wallet.generate_tx(inpt_tx=tx, 
                                                    recipient=recipient, 
                                                    amount=amount)
                net_wide_txs.append(new_tx)
                
                # print(f'malicious user broadcasting... transaction: {new_tx}')
            
            delay_seconds = random.randrange(0, 2)
            time.sleep(delay_seconds)
