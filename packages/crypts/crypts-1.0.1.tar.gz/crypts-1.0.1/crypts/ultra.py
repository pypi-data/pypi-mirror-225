from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import base64

def key():
    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Generate a random key for Fernet
    fernet_key = Fernet.generate_key()

    xor_key = b"secret_key"

    return {'private_key': private_key, 'public_key': public_key, 'fernet_key': fernet_key, 'xor_key': xor_key}

def encrypt(data, keys):
    public_key, fernet_key, xor_key = keys['public_key'], keys['fernet_key'], keys['xor_key']

    # Step 1: Base64 Encode
    encoded_data = base64.b64encode(data.encode('utf-8'))

    # Step 2: Fernet Encrypt
    f = Fernet(fernet_key)
    encrypted_data = f.encrypt(encoded_data)

    # Step 3: XOR Encrypt
    xor_encrypted_data = []
    for i, char in enumerate(encrypted_data):
        encrypted_char = char ^ xor_key[i % len(xor_key)]
        xor_encrypted_data.append(encrypted_char)

    # Step 4: RSA Encrypt
    rsa_encrypted_data = public_key.encrypt(
        bytes(xor_encrypted_data),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return rsa_encrypted_data.hex()

def decrypt(encrypted_data, keys):
    private_key, xor_key = keys['private_key'], keys['xor_key']
    
    encrypted_data = bytes.fromhex(encrypted_data)

    # Step 5: RSA Decrypt
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Step 4: XOR Decrypt
    xor_decrypted_data = []
    for i, char in enumerate(decrypted_data):
        decrypted_char = char ^ xor_key[i % len(xor_key)]
        xor_decrypted_data.append(decrypted_char)

    # Step 3: Fernet Decrypt
    fernet_key = keys['fernet_key']
    f = Fernet(fernet_key)
    decoded_data = f.decrypt(bytes(xor_decrypted_data))
    decoded_data = base64.b64decode(decoded_data).decode('utf-8')

    return decoded_data

# Example usage
data = "E"

# Get keys
keys = key()

# Encrypt data
encrypted_data = encrypt(data, keys)
print("Encrypted:", encrypted_data)

# Decrypt data
decrypted_data = decrypt(encrypted_data, keys)
print("Decrypted:", decrypted_data)
