from crypto_utils import BLOCK_SIZE_BYTES
import random

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
