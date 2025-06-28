from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import matplotlib.pyplot as plt
import os
import random

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

def introduce_errors(ciphertext, num_blocks_to_corrupt):
    """Случайно искажает указанное количество блоков в зашифрованном тексте."""
    ct_bytes = bytearray(ciphertext)
    num_blocks = len(ct_bytes) // BLOCK_SIZE_BYTES
    
    num_blocks_to_corrupt = min(num_blocks_to_corrupt, num_blocks)
    
    block_indices = random.sample(range(num_blocks), num_blocks_to_corrupt)
    
    for i in block_indices:
        block_start = i * BLOCK_SIZE_BYTES
        # Повреждение одного байта в блоке с помощью XOR с 0xFF
        corrupt_position = random.randint(block_start, block_start + BLOCK_SIZE_BYTES - 1)
        ct_bytes[corrupt_position] ^= 0xFF
        
    return bytes(ct_bytes)

def count_damaged_blocks(original_pt, decrypted_pt):
    """Сравнивает исходный и расшифрованный открытый текст и подсчитывает поврежденные блоки."""
    damaged_count = 0
    min_len = min(len(original_pt), len(decrypted_pt))
    num_blocks = min_len // BLOCK_SIZE_BYTES
    
    for i in range(num_blocks):
        start = i * BLOCK_SIZE_BYTES
        end = start + BLOCK_SIZE_BYTES
        original_block = original_pt[start:end]
        decrypted_block = decrypted_pt[start:end]
        
        if original_block != decrypted_block:
            damaged_count += 1
            
    return damaged_count

def run_experiment():
    """Запускает полный эксперимент для всех режимов и строит графики результатов."""
    with open("input_pt.txt", "rb") as f:
        plaintext = f.read()

    mode_classes  = {
        "ECB": modes.ECB,
        "CBC": modes.CBC,
        "CFB": modes.CFB,
        "OFB": modes.OFB,
    }

    results = {name: [] for name in mode_classes }
    max_errors = 20
    for mode_name, mode_class in mode_classes.items():
        print(f"  Тестовый режим: {mode_name}")
        key = os.urandom(KEY_SIZE_BYTES)
        iv = os.urandom(IV_SIZE_BYTES)

        ciphertext = encrypt(mode_class, key, iv, plaintext)

        for n_errors in range(1, max_errors + 1):
            corrupted_ct = introduce_errors(ciphertext, n_errors)
            decrypted_pt = decrypt(mode_class, key, iv, corrupted_ct)
            
            encrypted_filename = f"decrypted_pt_{mode_name}.txt"
            with open(encrypted_filename, "wb") as f:
                f.write(decrypted_pt) 

            m_damaged = count_damaged_blocks(plaintext, decrypted_pt)
            results[mode_name].append((n_errors, m_damaged))

    plt.figure(figsize=(10, 8))
    
    for mode_name, data_points in results.items():
        n_values = [p[0] for p in data_points]
        m_values = [p[1] for p in data_points]
        plt.plot(n_values, m_values, marker='o', linestyle='-', label=mode_name)
        
    x_theory = list(range(1, max_errors + 1))
    y_theory_1 = x_theory
    y_theory_2 = [2 * x for x in x_theory]
    
    plt.plot(x_theory, y_theory_1, 'k--', label='Теория  M=N (ECB, OFB)')
    plt.plot(x_theory, y_theory_2, 'k:', label='Теория  M=2N (CBC, CFB)')

    plt.title('Распространение ошибок в режимах AES')
    plt.xlabel('Число повреждённых блоков шифртекста (N)')
    plt.ylabel('Число повреждённых блоков открытого текста (M)')
    plt.xticks(range(1, max_errors + 1))
    plt.yticks(range(0, (max_errors * 2) + 2, 2))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    output_filename = "error_propagation_graph.png"
    plt.savefig(output_filename)
    print(f"\nЭксперимент завершен. График сохранен как {output_filename}")
    plt.show()

if __name__ == "__main__":
    run_experiment()
