# Ukuran satu word dalam bit, RC5 di sini menggunakan 32-bit word.
WORD_SIZE = 32

# Jumlah ronde yang digunakan dalam RC5, biasanya 12 atau 16.
ROUNDS = 12

# Nilai-nilai awal untuk P dan Q, yang merupakan konstanta dalam algoritma RC5.
# P dan Q adalah bilangan bulat yang digunakan dalam proses enkripsi dan dekripsi.
P = 0xB7E15163
Q = 0x9E3779B9


def rotate_left(val, shift):
   return ((val << shift) & 0xFFFFFFFF) | (val >> (32 - shift))

def rotate_right(val, shift):
   return (val >> shift) | ((val << (32 - shift)) & 0xFFFFFFFF)

def rc5_key_schedule(key, w=32, r=12):
   # w = word size, r = number of rounds
   b = len(key)
   u = w // 8
   c = (b + u - 1) // u
   L = [0] * c

   # Convert key bytes to words in L
   for i in range(b):
      L[i // u] = (L[i // u] << 8) + key[i]

   # Constants
   P = 0xB7E15163
   Q = 0x9E3779B9

   t = 2 * (r + 1)
   S = [0] * t
   S[0] = P
   for i in range(1, t):
      S[i] = (S[i - 1] + Q) & 0xFFFFFFFF

   # Mix key into S
   A = B = i = j = 0
   for _ in range(3 * max(t, c)):
      A = S[i] = ((S[i] + A + B) << 3 | (S[i] + A + B) >> (32 - 3)) & 0xFFFFFFFF
      B = L[j] = ((L[j] + A + B) << (A + B) % 32 | (L[j] + A + B) >> (32 - (A + B) % 32)) & 0xFFFFFFFF
      i = (i + 1) % t
      j = (j + 1) % c

   return S

def rc5_encrypt(plain_block, S):
   A = int.from_bytes(plain_block[:4], byteorder='little')
   B = int.from_bytes(plain_block[4:], byteorder='little')
   A = (A + S[0]) & 0xFFFFFFFF
   B = (B + S[1]) & 0xFFFFFFFF
   for i in range(1, ROUNDS + 1):
      A = (rotate_left((A ^ B), B % 32) + S[2 * i]) & 0xFFFFFFFF
      B = (rotate_left((B ^ A), A % 32) + S[2 * i + 1]) & 0xFFFFFFFF
   return A.to_bytes(4, byteorder='little') + B.to_bytes(4, byteorder='little')

def rc5_decrypt(cipher_block, S):
   A = int.from_bytes(cipher_block[:4], byteorder='little')
   B = int.from_bytes(cipher_block[4:], byteorder='little')
   for i in range(ROUNDS, 0, -1):
      B = rotate_right((B - S[2 * i + 1]) & 0xFFFFFFFF, A % 32) ^ A
      A = rotate_right((A - S[2 * i]) & 0xFFFFFFFF, B % 32) ^ B
   A = (A - S[0]) & 0xFFFFFFFF
   B = (B - S[1]) & 0xFFFFFFFF
   return A.to_bytes(4, byteorder='little') + B.to_bytes(4, byteorder='little')
