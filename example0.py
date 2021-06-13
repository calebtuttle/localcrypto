'''
Example simulation. 
'''

from localcrypto.simulate import Simulator

simulator = Simulator(runtime=20, 
                      num_mining_nodes=2, 
                      num_benign_users=2, 
                      num_malicious_users=1, 
                      benign_users_init_amount=[1, 2],
                      malicious_users_init_amount=[7])
simulator.start()
simulator.join()