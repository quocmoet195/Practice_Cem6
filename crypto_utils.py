from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

KEY_SIZE_BYTES = 16
BLOCK_SIZE_BYTES = 16
IV_SIZE_BYTES = 16

def encrypt(mode_class, key, iv, plaintext):  
    """Шифрует открытый текст с использованием AES-128 в указанном режиме."""
    if mode_class == modes.ECB:
        cipher = Cipher(algorithms.AES(key), mode_class())
    else:
        cipher = Cipher(algorithms.AES(key), mode_class(iv))
    
    encryptor = cipher.encryptor()
    
    # Дополнить открытый текст так, чтобы он был кратен размеру блока
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext

def decrypt(mode_class, key, iv, ciphertext):
    """Расшифровывает зашифрованный текст с использованием AES-128 в указанном режиме."""
    if mode_class == modes.ECB:
        cipher = Cipher(algorithms.AES(key), mode_class())
    else:
        cipher = Cipher(algorithms.AES(key), mode_class(iv))
    
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    try:
        plaintext = unpadder.update(decrypted_padded) + unpadder.finalize()
    except ValueError:
        plaintext = decrypted_padded
        
    return plaintext
