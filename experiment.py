from cryptography.hazmat.primitives.ciphers import modes
from crypto_utils import encrypt, decrypt, KEY_SIZE_BYTES, IV_SIZE_BYTES
from error_utils import introduce_errors, count_damaged_blocks
from plot_utils import plot_results
import os

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

    plot_results(results, max_errors)
