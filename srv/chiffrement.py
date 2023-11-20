import socket
import cryptography

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

private_key_file = '/chemin/vers/votre/private_key.pem'
public_key_file = '/chemin/vers/votre/public_key.pem'

#public_key = serialization.load_pem_public_key(pem_public_key, backend=default_backend())


def gen_keypair():
    pr_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    pu_key = pr_key.public_key()

    return pu_key,pr_key


pu, pr = gen_keypair()

print(pu)
print(pr)

def envoi_keypu(pu):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((, 12345))
    server_socket.listen(1)

    print("En attente de connexion...")
    conn, addr = server_socket.accept()
    print("Connexion établie avec", addr)

    pem = pu.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    conn.sendall(pem)

#def dechiffrement (data):
#
#    data_en_clair = pr_key.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
#    return data_en_clair

