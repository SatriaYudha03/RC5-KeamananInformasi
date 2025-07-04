import base64
from rc5_simple import rc5_key_schedule, rc5_encrypt, rc5_decrypt

def pad_data(data):
    while len(data) % 8 != 0:
        data += b'\x00'
    return data

def encrypt_text(plaintext, key):
    key_bytes = key.encode('utf-8')
    data = plaintext.encode('utf-8')
    data = pad_data(data)
    S = rc5_key_schedule(key_bytes)
    ciphertext = b''
    for i in range(0, len(data), 8):
        ciphertext += rc5_encrypt(data[i:i+8], S)
    return base64.b64encode(ciphertext).decode('utf-8')

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
        print("Hasil enkripsi (base64):", encrypted)

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
