import pickle
from hashlib import sha256

from Cryptodome.Hash import RIPEMD160
from cryptography.hazmat.primitives import serialization

from localcrypto.constants import HEADER

def print_blockchain_comparison(mining_nodes):
    print('-'*100)
    print('Comparing blockchains...\n')

    blockchains = [node.main_blockchain for node in mining_nodes]
    
    shortest_blockchain_len = len(blockchains[0])
    for i, blockchain in enumerate(blockchains):
        print(f'blockchain{i} has {len(blockchain)} blocks')
        if len(blockchain) < shortest_blockchain_len:
            shortest_blockchain_len = len(blockchain)
    print('\n\n')

    for i in range(shortest_blockchain_len):
        txs_len = []
        nonces = []
        for blockchain in blockchains:
            txs_len.append(len(blockchain[i].transactions))
            nonces.append(blockchain[i].nonce)
        for k in range(len(txs_len)):
            print(f'block{i} in blockchain{k} has {txs_len[k]} transactions')
        print('-'*30)
        for k in range(len(nonces)):
            print(f'block{i} in blockchain{k} has a nonce of {nonces[k]}')
        print('\n\n')


def send(obj, client_socket):
    ''' Send pickled obj to client_socket '''
    msg = pickle.dumps(obj)
    msg_len = str(len(msg)).encode('utf-8')
    msg_len += b' ' * (HEADER - len(msg_len))
    client_socket.send(msg_len)
    client_socket.send(msg)

def receive_message(client_socket):
    msg_len = client_socket.recv(HEADER).decode('utf-8')
    msg_len = int(msg_len)
    msg = client_socket.recv(msg_len)
    return msg


def hash_pub_key(public_key):
    '''
    Generates and returns a hash of public_key. The 
    result of this hash is also called the "address".
    
    public_key : a EllipticCurvePublicKey object from the cryptography library
        A public key
        
    Returns RIPEMD160(SHA256(public_key)).
        dtype : bytes
    '''
    pub_key_hash = public_key.public_bytes(encoding=serialization.Encoding.X962, 
                                           format=serialization.PublicFormat.UncompressedPoint)
    pub_key_hash = sha256(pub_key_hash).digest()
    return RIPEMD160.new(pub_key_hash).hexdigest()

def serialize_pub_key(public_key):
    '''
    public_key : EllipticCurvePublicKey object from cryptography library
    '''
    return public_key.public_bytes(encoding=serialization.Encoding.DER,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo)

def deserialize_pub_key(public_key):
    '''
    public_key : EllipticCurvePublicKey object from cryptography library
    '''
    return serialization.load_der_public_key(data=public_key,
                                            backend=None)