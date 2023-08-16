from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class RSAEncryptor:
    @staticmethod
    def key():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    @staticmethod
    def encrypt(plaintext, public_key):
        encrypted_data = public_key.encrypt(
            plaintext.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_data
    
    @staticmethod
    def decrypt(encrypted_data, private_key):
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data.decode("utf-8")

if __name__ == "__main__":
    plaintext = "Hello, RSA encryption!"
    
    private_key, public_key = RSAEncryptor.key()
    
    print('Private Key: '+str(private_key))
    print('Public Key: ' + str(public_key))

    encrypted = RSAEncryptor.encrypt(plaintext, public_key)
    decrypted = RSAEncryptor.decrypt(encrypted, private_key)
    
    print("Plaintext:", plaintext)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
