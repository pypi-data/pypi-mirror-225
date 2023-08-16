import os
from cryptography.fernet import Fernet
import base64 as b64

class xor:
    @classmethod
    def _apply_xor(cls, data, key):
        result = bytearray()
        key_index = 0
        
        for byte in data:
            xored_byte = byte ^ key[key_index]
            result.append(xored_byte)
            
            key_index = (key_index + 1) % len(key)
            
        return result
    
    @classmethod
    def key(cls, length):
        return os.urandom(length)

    @classmethod
    def encrypt(cls, plaintext, key):
        encrypted_data = cls._apply_xor(plaintext.encode(), key)
        return encrypted_data.hex()
    
    @classmethod
    def decrypt(cls, encrypted_data, key):
        encrypted_bytes = bytes.fromhex(encrypted_data)
        decrypted_data = cls._apply_xor(encrypted_bytes, key)
        return decrypted_data.decode("utf-8")

class fernet:
    @staticmethod
    def key():
        return Fernet.generate_key()

    @staticmethod
    def encrypt(plaintext, key):
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(plaintext.encode())
        return encrypted_data
    
    @staticmethod
    def decrypt(encrypted_data, key):
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data).decode("utf-8")
        return decrypted_data
    
class base64:
    @staticmethod
    def encode(text):
        return b64.b64encode(text.encode()).decode()
    
    @staticmethod
    def decode(text):
        return b64.b64decode(text).decode()

if __name__ == "__main__":
    plaintext = "Hello, XOR encryption!"
    encryption_key = xor.key(16)
    
    print('XOR Encryption Key: '+str(encryption_key))

    encrypted = xor.encrypt(plaintext, encryption_key)
    decrypted = xor.decrypt(encrypted, encryption_key)
    
    print("XOR Plaintext:", plaintext)
    print("XOR Encrypted:", encrypted)
    print("XOR Decrypted:", decrypted)

    plaintext = "Hello, Fernet encryption!"
    
    key = fernet.key()

    print('Fernet Key: ' + str(key))

    
    encrypted = fernet.encrypt(plaintext, key)
    decrypted = fernet.decrypt(encrypted, key)
    
    print("Fernet Plaintext:", plaintext)
    print("Fernet Encrypted:", encrypted)
    print("Fernet Decrypted:", decrypted)

    plaintext = 'Base64'

    print('Base64 Plain Text: ' + plaintext)
    print('Base64 Encrypted: '+base64.encode(plaintext))
    print('Base64 Decrypted: '+base64.decode(base64.encode(plaintext)))