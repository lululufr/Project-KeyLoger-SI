import socket
import cryptography

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

private_key_file = '/chemin/vers/votre/private_key.pem'
public_key_file = '/chemin/vers/votre/public_key.pem'

#public_key = serialization.load_pem_public_key(pem_public_key, backend=default_backend())


def gen_keypair() :

    pr_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    pu_key = pr_key.public_key()
    return pu_key

def envoi_keypu(pu_key):

    pem = pu_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )



#def dechiffrement (data):
#
#    data_en_clair = pr_key.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
#    return data_en_clair

#with open('private_key.pem', 'wb') as private_key_file:
#    private_key_bytes = private_key.private_bytes(
#        encoding=serialization.Encoding.PEM,
#        format=serialization.PrivateFormat.PKCS8,
#        encryption_algorithm=serialization.NoEncryption()
#    )
#    private_key_file.write(private_key_bytes)