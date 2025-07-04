import base64

# Konstanta untuk algoritma RC5
WORD_SIZE = 32
ROUNDS = 12
P = 0xB7E15163  # Konstanta P untuk inisialisasi S
Q = 0x9E3779B9  # Konstanta Q untuk inisialisasi S

# Fungsi untuk rotasi bitwise ke kiri
def rotate_left(val, shift):
    # Menggeser bit ke kiri dan memastikan hasilnya tetap dalam 32-bit
    # Menggunakan bitwise OR untuk menggabungkan bagian yang digeser dan bagian yang "melilit"
    return ((val << shift) & 0xFFFFFFFF) | (val >> (32 - shift))

# Fungsi untuk rotasi bitwise ke kanan
def rotate_right(val, shift):
    # Menggeser bit ke kanan dan memastikan hasilnya tetap dalam 32-bit
    # Menggunakan bitwise OR untuk menggabungkan bagian yang digeser dan bagian yang "melilit"
    return (val >> shift) | ((val << (32 - shift)) & 0xFFFFFFFF)

# Fungsi untuk membuat Key Schedule (S) dari kunci yang diberikan
def rc5_key_schedule(key, w=32, r=12):
    b = len(key)  # Panjang kunci dalam byte
    u = w // 8    # Ukuran word dalam byte (misal: 32 bit / 8 = 4 byte)
    c = (b + u - 1) // u # Jumlah word yang dibutuhkan untuk menyimpan kunci
    L = [0] * c   # Array L untuk menyimpan kunci dalam format word

    # Memuat kunci ke dalam array L
    for i in range(b):
        L[i // u] = (L[i // u] << 8) + key[i]

    t = 2 * (r + 1) # Ukuran array S (jumlah subkunci)
    S = [0] * t     # Array S untuk menyimpan subkunci

    # Inisialisasi array S dengan konstanta P dan Q
    S[0] = P
    for i in range(1, t):
        S[i] = (S[i - 1] + Q) & 0xFFFFFFFF # Penjumlahan modulo 2^32

    # Mencampur (mixing) L dan S untuk menghasilkan subkunci akhir
    A = B = i = j = 0
    for _ in range(3 * max(t, c)): # Melakukan iterasi 3 * max(t, c) kali
        A = S[i] = rotate_left((S[i] + A + B) & 0xFFFFFFFF, 3)
        B = L[j] = rotate_left((L[j] + A + B) & 0xFFFFFFFF, (A + B) % 32)
        i = (i + 1) % t
        j = (j + 1) % c
    return S

# Fungsi untuk mengenkripsi satu blok data (8 byte untuk WORD_SIZE=32)
def rc5_encrypt(plain_block, S):
    # Memisahkan blok plaintext menjadi dua word A dan B
    A = int.from_bytes(plain_block[:4], byteorder='little') # 4 byte pertama
    B = int.from_bytes(plain_block[4:], byteorder='little') # 4 byte kedua

    # Penambahan subkunci awal
    A = (A + S[0]) & 0xFFFFFFFF
    B = (B + S[1]) & 0xFFFFFFFF

    # Iterasi enkripsi sebanyak ROUNDS
    for i in range(1, ROUNDS + 1):
        A = (rotate_left((A ^ B), B % 32) + S[2 * i]) & 0xFFFFFFFF
        B = (rotate_left((B ^ A), A % 32) + S[2 * i + 1]) & 0xFFFFFFFF

    # Menggabungkan kembali word A dan B menjadi blok ciphertext
    return A.to_bytes(4, byteorder='little') + B.to_bytes(4, byteorder='little')

# Fungsi untuk mendekripsi satu blok data (8 byte untuk WORD_SIZE=32)
def rc5_decrypt(cipher_block, S):
    # Memisahkan blok ciphertext menjadi dua word A dan B
    A = int.from_bytes(cipher_block[:4], byteorder='little')
    B = int.from_bytes(cipher_block[4:], byteorder='little')

    # Iterasi dekripsi secara terbalik dari enkripsi
    for i in range(ROUNDS, 0, -1):
        B = rotate_right((B - S[2 * i + 1]) & 0xFFFFFFFF, A % 32) ^ A
        A = rotate_right((A - S[2 * i]) & 0xFFFFFFFF, B % 32) ^ B

    # Pengurangan subkunci awal (kebalikan dari penambahan)
    A = (A - S[0]) & 0xFFFFFFFF
    B = (B - S[1]) & 0xFFFFFFFF

    # Menggabungkan kembali word A dan B menjadi blok plaintext
    return A.to_bytes(4, byteorder='little') + B.to_bytes(4, byteorder='little')

# Fungsi untuk menambahkan padding pada data agar panjangnya kelipatan 8 byte
def pad_data(data):
    while len(data) % 8 != 0:
        data += b'\x00' # Menambahkan null byte
    return data

# Fungsi utama untuk mengenkripsi teks
def encrypt_text(plaintext, key):
    key_bytes = key.encode('utf-8') # Mengubah kunci menjadi byte
    data = pad_data(plaintext.encode('utf-8')) # Mengubah plaintext menjadi byte dan menambahkan padding
    S = rc5_key_schedule(key_bytes) # Membuat key schedule

    ciphertext = b''
    # Mengenkripsi data per blok 8 byte
    for i in range(0, len(data), 8):
        ciphertext += rc5_encrypt(data[i:i+8], S)

    # Mengkodekan ciphertext biner ke Base64 agar aman dikirim sebagai teks
    return base64.b64encode(ciphertext).decode('utf-8')

# Fungsi utama untuk mendekripsi teks
def decrypt_text(ciphertext_b64, key):
    key_bytes = key.encode('utf-8') # Mengubah kunci menjadi byte
    S = rc5_key_schedule(key_bytes) # Membuat key schedule

    ciphertext = base64.b64decode(ciphertext_b64) # Mendekode Base64 kembali ke biner
    plaintext = b''
    # Mendekripsi data per blok 8 byte
    for i in range(0, len(ciphertext), 8):
        plaintext += rc5_decrypt(ciphertext[i:i+8], S)

    # Menghapus null byte padding dan mendekode byte menjadi string UTF-8
    # Menggunakan rstrip(b'\x00') untuk menghapus padding
    return plaintext.rstrip(b'\x00').decode('utf-8')