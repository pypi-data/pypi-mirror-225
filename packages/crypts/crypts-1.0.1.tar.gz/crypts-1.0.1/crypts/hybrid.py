from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

class HybridEncryptor:
    @staticmethod
    def key():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    @staticmethod
    def encrypt(data, public_key):
        symmetric_key = Fernet.generate_key()
        fernet = Fernet(symmetric_key)
        encrypted_data = fernet.encrypt(data.encode())
        
        encrypted_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return encrypted_key, encrypted_data
    
    @staticmethod
    def decrypt(encrypted_key, encrypted_data, private_key):
        decrypted_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        fernet = Fernet(decrypted_key)
        decrypted_data = fernet.decrypt(encrypted_data).decode("utf-8")
        
        return decrypted_data

if __name__ == "__main__":
    plaintext = "Hello, hybrid encryption!"
    
    private_key, public_key = HybridEncryptor.key()
    
    print('Public Key: '+str(public_key))
    print('Private Key: ' + str(private_key))

    encrypted_key, encrypted_data = HybridEncryptor.encrypt(plaintext, public_key)
    decrypted_data = HybridEncryptor.decrypt(encrypted_key, encrypted_data, private_key)
    
    print("Plaintext:", plaintext)
    print('Encrypted Key: '+str(encrypted_key))
    print('Encrypted Data: '+ str(encrypted_data))
    print("Decrypted Data:", decrypted_data)
