# RC5 encryption in Python

w = 32                # word size in bits
r = 12                # number of rounds
b = 16                # number of bytes in key
c = 4                 # number of words in key (ceil(8*b/w))
t = 2 * (r + 1)       # size of table

modulo = 2 ** w       # for 32-bit words

# Left rotate
def rotate_left(x, y):
    return ((x << (y & (w - 1))) | (x >> (w - (y & (w - 1))))) % modulo

# Right rotate
def rotate_right(x, y):
    return ((x >> (y & (w - 1))) | (x << (w - (y & (w - 1))))) % modulo

# RC5 Key Expansion
def key_expansion(key):
    L = [0] * c
    for i in range(b - 1, -1, -1):
        L[i // 4] = (L[i // 4] << 8) + key[i]

    S = [0] * t
    P = 0xB7E15163
    Q = 0x9E3779B9

    S[0] = P
    for i in range(1, t):
        S[i] = (S[i - 1] + Q) % modulo

    A = B = i = j = 0
    for _ in range(3 * max(t, c)):
        A = S[i] = rotate_left((S[i] + A + B) % modulo, 3)
        B = L[j] = rotate_left((L[j] + A + B) % modulo, (A + B) % w)
        i = (i + 1) % t
        j = (j + 1) % c

    return S

# RC5 Encryption
def rc5_encrypt(plain, S):
    A, B = plain
    A = (A + S[0]) % modulo
    B = (B + S[1]) % modulo
    for i in range(1, r + 1):
        A = (rotate_left((A ^ B), B) + S[2 * i]) % modulo
        B = (rotate_left((B ^ A), A) + S[2 * i + 1]) % modulo
    return A, B

# RC5 Decryption
def rc5_decrypt(cipher, S):
    A, B = cipher
    for i in range(r, 0, -1):
        B = rotate_right((B - S[2 * i + 1]) % modulo, A) ^ A
        A = rotate_right((A - S[2 * i]) % modulo, B) ^ B
    B = (B - S[1]) % modulo
    A = (A - S[0]) % modulo
    return A, B

# Example usage
if __name__ == "__main__":
    # Key as byte array
    key = bytearray(b"SecretKeyForTest")  # 16 bytes

    # 64-bit block: A and B (each 32-bit unsigned int)
    plaintext = (0x89, 0x89ABCDEF)

    S = key_expansion(key)
    ciphertext = rc5_encrypt(plaintext, S)
    decrypted = rc5_decrypt(ciphertext, S)

    print("Plaintext :", [hex(x) for x in plaintext])
    print("Encrypted :", [hex(x) for x in ciphertext])
    print("Decrypted :", [hex(x) for x in decrypted])