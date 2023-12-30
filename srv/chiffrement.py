# Importe module

import socket
import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from env import *


def dechiffrement(data):

    """
    Cette fonction permet de déchiffrer avec l'algorithme d'asymétrie RSA (OAEP avec SHA-256)
    les données avec la clé privée.
    :param data: Prend les paramètres les données chiffrées qui sont reçus.
    :return:Les données déchiffrées.
    """

    private_key_path = 'siproject_private.pem'
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
