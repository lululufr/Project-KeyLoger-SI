from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

from env import *


def chiffrement(data):
    """
    Cette fonction permet de chiffrer avec l'algorithme d'asymétrie RSA (OAEP avec SHA-256)
    les données avec la clé publique.
    :param data: Prend les paramètres les données des données qui seront envoyées par la fonction send.
    :return:Les données chiffrées.

    """

    pub_public_key = KEY

    # with open(pub_public_key, 'rb') as key_file:
    #    datakey = key_file.read()

    public_key = serialization.load_pem_public_key(
        bytes(pub_public_key, "UTF-8"),
        backend=default_backend()
    )
    d_enc = data.encode('utf-8')
    enc_data = public_key.encrypt(
        d_enc,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return enc_data
