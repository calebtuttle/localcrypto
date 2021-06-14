import pickle
from hashlib import sha256

from Cryptodome.Hash import RIPEMD160
from cryptography.hazmat.primitives import serialization

from localcrypto.constants import HEADER


################### Miscellaneous network functions ###################
 
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


################### Miscellaneous public key functions ###################

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
