import socket
import cryptography

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding



def dechiffrement(data):
    private_key_path = 'srv/siproject_private.pem'
    with open(private_key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    dec_data = private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return dec_data.decode('utf-8')

def chiffrement(data) :
    pub_public_key = "client/siproject.pem"

    with open(pub_public_key, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    d_enc = bytes(data, 'utf-8')
    enc_data = public_key.encrypt(
        d_enc,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return enc_data

data =chiffrement("ddddddddddddddddddddddddddddddddddddddddddddddddddddd")
print(data)
print(dechiffrement(data))