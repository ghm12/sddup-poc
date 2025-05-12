from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

import base64

class DataCipher:
    def __init__(self, key_path: str = "./sddup/data/symmetric_key.b64", iv_path: str = "./sddup/data/iv.b64"):
        with open(key_path, "rb") as file:
            self.key = base64.b64decode(file.read())

        with open(iv_path, "rb") as file:
            self.iv = base64.b64decode(file.read())

    def encrypt_data(self, data: str):
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        encryptor = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend()).encryptor()
        
        padded_data = padder.update(data.encode("UTF-8")) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        return encrypted_data

    def decrypt_data(self, data: str):
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decryptor = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend()).decryptor()
        
        padded_data = decryptor.update(data) + decryptor.finalize()
        decrypted_data = unpadder.update(padded_data) + unpadder.finalize()

        decrypted_data = decrypted_data.decode("UTF-8")

        return decrypted_data
