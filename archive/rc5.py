import base64
# from rc5_simple import rc5_key_schedule, rc5_encrypt, rc5_decrypt

# Ukuran satu word dalam bit, RC5 di sini menggunakan 32-bit word.
WORD_SIZE = 32

# Jumlah ronde yang digunakan dalam RC5, biasanya 12 atau 16.
ROUNDS = 12

# Nilai-nilai awal untuk P dan Q, yang merupakan konstanta dalam algoritma RC5.
# P dan Q adalah bilangan bulat yang digunakan dalam proses enkripsi dan dekripsi.
P = 0xB7E15163
Q = 0x9E3779B9

# Memutar bit angka val ke kiri sebanyak shift bit.
# Bit yang "keluar" sebelah kiri akan masuk kembali dari kanan.
# & 0xFFFFFFFF untuk memastikan hasil tetap dalam 32-bit (word size).
def rotate_left(val, shift):
   return ((val << shift) & 0xFFFFFFFF) | (val >> (32 - shift))

# Sama seperti sebelumnya tapi memutar bit angka val ke kanan sebanyak shift bit.
def rotate_right(val, shift):
   return (val >> shift) | ((val << (32 - shift)) & 0xFFFFFFFF)


# w = word size, r = number of rounds
def rc5_key_schedule(key, w=32, r=12):
   b = len(key) # Panjang Key dalam byte
   u = w // 8  # Ukuran word dalam byte (32 bit = 4 byte)
   c = (b + u - 1) // u # Jumlah word yang diperlukan dalam key
   L = [0] * c # Inisialisasi array L yang menampung key dalam bentuk word
   
   # Konversi key bytes ke word-word di list L
   for i in range(b):
      L[i // u] = (L[i // u] << 8) + key[i]
   # Byte key di-group menjadi word 32-bit dalam L.
   # i // u menghitung index word saat menggabungkan 4 byte per word.
   # L[i // u] << 8 menggeser 8 bit (1 byte) ke kiri, kemudian tambahkan byte baru.
   # Contoh: Jika key 8 byte: L[0] dan L[1] akan berisi dua word 32-bit.

   # S adalah array subkey hasil perluasan key yang akan dipakai di tiap putaran enkripsi/dekripsi.
   # t adalah total jumlah subkey, sebanyak 2 * (r + 1).
   # S diinisialisasi mulai dari P dan tiap elemen berikutnya S[i] = S[i-1] + Q modulo 32-bit.
   t = 2 * (r + 1)
   S = [0] * t
   S[0] = P
   for i in range(1, t):
      S[i] = (S[i - 1] + Q) & 0xFFFFFFFF


   # Mix key into S
   # Loop sebanyak 3 kali dari jumlah terbesar antara subkey t dan key word c.
   # A dan B adalah variabel sementara untuk mixing.
   # Subkey array S dan key array L dicampur dengan operasi rotasi dan penambahan (mod 32-bit).
   A = B = i = j = 0
   for _ in range(3 * max(t, c)):
      A = S[i] = ((S[i] + A + B) << 3 | (S[i] + A + B) >> (32 - 3)) & 0xFFFFFFFF
      B = L[j] = ((L[j] + A + B) << (A + B) % 32 | (L[j] + A + B) >> (32 - (A + B) % 32)) & 0xFFFFFFFF
      i = (i + 1) % t
      j = (j + 1) % c

   return S

# Fungsi ini melakukan enkripsi satu blok data 64-bit (8 byte) menggunakan algoritma RC5. Proses ini mengubah plaintext menjadi ciphertext.
def rc5_encrypt(plain_block, S):
   # Blok 8 byte (plain_block) dibagi menjadi dua bagian:
   # A berisi byte ke-0 sampai ke-3 (4 byte pertama)
   # B berisi byte ke-4 sampai ke-7 (4 byte kedua)
   # Keduanya diubah ke bilangan integer 32-bit (little endian).
   A = int.from_bytes(plain_block[:4], byteorder='little')
   B = int.from_bytes(plain_block[4:], byteorder='little')
   
   # Menambahkan subkey pertama ke masing-masing word (A dan B).
   # & 0xFFFFFFFF memastikan hasil tetap 32-bit.
   A = (A + S[0]) & 0xFFFFFFFF
   B = (B + S[1]) & 0xFFFFFFFF
   
   # Melakukan 12 putaran enkripsi (jika ROUNDS = 12).
   # RC5 dikenal dengan struktur yang sederhana tapi kuat berkat putaran ini.
   # Di setiap putaran, nilai A dan B akan saling memengaruhi satu sama lain, sehingga memberikan difusi (penyebaran perubahan bit).
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


def pad_data(data):
   while len(data) % 8 != 0:
      data += b'\x00'
   return data

def tampilkan_kunci_biner(key_bytes):
   print("\nIndex\tKunci\t\tBiner Kunci")
   for i, byte in enumerate(key_bytes):
      print(f"K[{i}]\t{byte:08b}")

def encrypt_text(plaintext, key):
   key_bytes = key.encode('utf-8')
   
   # Cetak representasi biner kunci
   tampilkan_kunci_biner(key_bytes)
   
   data = plaintext.encode('utf-8')
   data = pad_data(data)
   S = rc5_key_schedule(key_bytes)
   ciphertext = b''
   for i in range(0, len(data), 8):
      ciphertext += rc5_encrypt(data[i:i+8], S)
   # return base64.b64encode(ciphertext).decode('utf-8')
   return ciphertext

def decrypt_text(ciphertext_b64, key):
   key_bytes = key.encode('utf-8')
   S = rc5_key_schedule(key_bytes)
   ciphertext = base64.b64decode(ciphertext_b64)
   plaintext = b''
   for i in range(0, len(ciphertext), 8):
      plaintext += rc5_decrypt(ciphertext[i:i+8], S)
   return plaintext.rstrip(b'\x00').decode('utf-8')

def main():
   print("=== RC5 Encryption CLI App ===")
   choice = input("Pilih mode (1 = Enkripsi, 2 = Dekripsi): ").strip()

   if choice == '1':
      plaintext = input("Masukkan plaintext: ").strip()
      key = input("Masukkan key: ").strip()
      if not key:
         print("Key tidak boleh kosong.")
         return
      encrypted = encrypt_text(plaintext, key)
      # print("Hasil enkripsi (base64):", encrypted)
      print("Hasil enkripsi (base64):", base64.b64encode(encrypted).decode())
      print("Ciphertext (hex):", encrypted.hex())

   elif choice == '2':
      ciphertext = input("Masukkan ciphertext (base64): ").strip()
      key = input("Masukkan key: ").strip()
      if not key:
         print("Key tidak boleh kosong.")
         return
      try:
         decrypted = decrypt_text(ciphertext, key)
         print("Hasil dekripsi:", decrypted)
      except Exception as e:
         print(f"Terjadi kesalahan saat dekripsi: {e}")

   else:
      print("Pilihan tidak valid.")

if __name__ == "__main__":
   main()
