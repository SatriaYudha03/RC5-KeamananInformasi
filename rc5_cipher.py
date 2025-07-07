import base64

# Konstanta untuk algoritma RC5
WORD_SIZE = 32
ROUNDS = 12
P = 0xB7E15163  # Konstanta P
Q = 0x9E3779B9  # Konstanta Q

# Rotasi bitwise ke kiri
def rotate_left(val, shift):
    return ((val << shift) & 0xFFFFFFFF) | (val >> (32 - shift))

# Rotasi bitwise ke kanan
def rotate_right(val, shift):
    return (val >> shift) | ((val << (32 - shift)) & 0xFFFFFFFF)

# Key Schedule
def rc5_key_schedule(key, w=32, r=12):
    b = len(key)
    u = w // 8
    c = (b + u - 1) // u
    L = [0] * c

    for i in range(b):
        L[i // u] = (L[i // u] << 8) + key[i]

    t = 2 * (r + 1)
    S = [0] * t
    S[0] = P
    for i in range(1, t):
        S[i] = (S[i - 1] + Q) & 0xFFFFFFFF

    A = B = i = j = 0
    for _ in range(3 * max(t, c)):
        A = S[i] = rotate_left((S[i] + A + B) & 0xFFFFFFFF, 3)
        B = L[j] = rotate_left((L[j] + A + B) & 0xFFFFFFFF, (A + B) % 32)
        i = (i + 1) % t
        j = (j + 1) % c

    return S

# Enkripsi blok 8 byte
def rc5_encrypt(plain_block, S):
    A = int.from_bytes(plain_block[:4], byteorder='little')
    B = int.from_bytes(plain_block[4:], byteorder='little')

    A = (A + S[0]) & 0xFFFFFFFF
    B = (B + S[1]) & 0xFFFFFFFF

    for i in range(1, ROUNDS + 1):
        A = (rotate_left(A ^ B, B % 32) + S[2 * i]) & 0xFFFFFFFF
        B = (rotate_left(B ^ A, A % 32) + S[2 * i + 1]) & 0xFFFFFFFF

    return A.to_bytes(4, 'little') + B.to_bytes(4, 'little')

# Dekripsi blok 8 byte
def rc5_decrypt(cipher_block, S):
    A = int.from_bytes(cipher_block[:4], byteorder='little')
    B = int.from_bytes(cipher_block[4:], byteorder='little')

    for i in range(ROUNDS, 0, -1):
        B = rotate_right((B - S[2 * i + 1]) & 0xFFFFFFFF, A % 32) ^ A
        A = rotate_right((A - S[2 * i]) & 0xFFFFFFFF, B % 32) ^ B

    A = (A - S[0]) & 0xFFFFFFFF
    B = (B - S[1]) & 0xFFFFFFFF

    return A.to_bytes(4, 'little') + B.to_bytes(4, 'little')

# Padding agar kelipatan 8 byte
def pad_data(data):
    while len(data) % 8 != 0:
        data += b'\x00'
    return data

# Enkripsi teks ke base64
def encrypt_text(plaintext, key):
    key_bytes = key.encode('utf-8')
    data = pad_data(plaintext.encode('utf-8'))
    S = rc5_key_schedule(key_bytes)

    ciphertext = b''
    for i in range(0, len(data), 8):
        ciphertext += rc5_encrypt(data[i:i+8], S)

    return base64.b64encode(ciphertext).decode('utf-8')

# Dekripsi base64 ke teks, fallback decode kalau UTF-8 gagal
def decrypt_text(ciphertext_b64, key):
    key_bytes = key.encode('utf-8')
    S = rc5_key_schedule(key_bytes)

    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = b''
    for i in range(0, len(ciphertext), 8):
        plaintext += rc5_decrypt(ciphertext[i:i+8], S)

    plaintext = plaintext.rstrip(b'\x00')

    try:
        return plaintext.decode('utf-8')
    except UnicodeDecodeError:
        return plaintext.decode('latin-1', errors='replace')
