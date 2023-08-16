import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

from fabrique_nodes_core.db.pg_orm import DB
import base64


FABRIQUE_RSA_PASSWORD = os.getenv('FABRIQUE_RSA_PASSWORD', 'test_passw')
RSA_PASSWORD = FABRIQUE_RSA_PASSWORD.encode()


def generate_keys(password: bytes = RSA_PASSWORD):
    # Генерация пары ключей
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Сериализация публичного ключа
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Сериализация приватного ключа
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    )

    return public_pem, private_pem


def encrypt(public_key_pem: bytes, message: str):
    public_key = serialization.load_pem_public_key(
        public_key_pem,
        backend=default_backend()
    )

    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    encrypted = base64.b64encode(encrypted).decode()

    return encrypted


def decrypt(private_key_pem: bytes, encrypted: str, password: bytes = RSA_PASSWORD):
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=password,
        backend=default_backend()
    )

    encrypted = base64.b64decode(encrypted.encode())

    original_message = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return original_message.decode()


class Crypto:
    def __init__(self, user_id: str):
        self.db = DB()
        self.public_key_pem = b''
        self.private_key_pem = b''
        self.__init_keys(user_id)

    def write_new_keys(self, user_id):
        public_key_pem, private_key_pem = generate_keys()
        self.db.write_key_pems(user_id, public_key_pem.decode(), private_key_pem.decode())

    def __init_keys(self, user_id: str):
        if not self.db.pem_exists(user_id):
            self.write_new_keys(user_id)
        private_pem = self.db.get_private_pem(user_id)
        public_pem = self.db.get_public_pem(user_id)
        self.public_key_pem = public_pem.encode()
        self.private_key_pem = private_pem.encode()

    def encrypt(self, message: str) -> str:
        return encrypt(self.public_key_pem, message)

    def decrypt(self, encrypted_message: str) -> str:
        return decrypt(self.private_key_pem, encrypted_message)
