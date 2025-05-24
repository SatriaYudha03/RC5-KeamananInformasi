def to_binary_string(num):
   return format(num, '08b')

def key_expansion_and_xor(kunci_str, plaintext):
   k = [int(digit) for digit in str(kunci_str)]
   n = len(k)
   S = list(range(n))  # S = [0, 1, 2, ..., n-1]
   print("=== KEY EXPANSION ===")
   print(f"Kunci (digit): {k}")
   print(f"Initial S: {S}")

   j = 0
   # Tahap Key Expansion mirip KSA RC4
   for i in range(n):
      j = (j + S[i] + k[i]) % n
      S[i], S[j] = S[j], S[i]
      print(f"i = {i}, j = (j + S[{i}] + k[{i}]) % {n} = {j}")
      print(f"Swap S[{i}] <-> S[{j}] -> {S}")

   print(f"\nFinal S after key expansion: {S}")

   # Tahap XOR Key Stream (enkripsi pseudo-RC4)
   print("\n=== KEY STREAM GENERATION & XOR ENCRYPTION ===")
   i = 0
   j = 0
   ciphertext_bin = []
   keys_bin = []
   ciphertext_ascii = ""

   for idx, char in enumerate(plaintext):
      i = (i + 1) % n
      j = (j + S[i]) % n
      S[i], S[j] = S[j], S[i]

      t = (S[i] + S[j]) % n
      key_byte = S[t]

      key_val = 48 + key_byte
      key_bin = to_binary_string(key_val)
      char_bin = to_binary_string(ord(char))
      cipher_val = ord(char) ^ key_val
      cipher_bin = to_binary_string(cipher_val)
      cipher_char = chr(cipher_val)

      print(f"Plaintext[{idx}] = '{char}' -> ASCII: {ord(char)} -> BIN: {char_bin}")
      print(f"Key Byte = S[{t}] = {key_byte} -> BIN: {key_bin}")
      print(f"XOR Result: {cipher_bin} -> Char: '{cipher_char}'\n")

      keys_bin.append(key_bin)
      ciphertext_bin.append(cipher_bin)
      ciphertext_ascii += cipher_char

   print("=== HASIL ENKRIPSI AKHIR ===")
   print(f"Ciphertext (karakter): {ciphertext_ascii}\n")
   return keys_bin, ciphertext_bin, ciphertext_ascii

# Contoh penggunaan:
kunci = 252567
plaintext = "WIDODO"
keys_bin, ciphers_bin, cipher_ascii = key_expansion_and_xor(kunci, plaintext)

print("Kunci Biner:")
for i, kb in enumerate(keys_bin):
   print(f"K[{i}] = {kb}")

print("\nCiphertext Biner:")
for i, cb in enumerate(ciphers_bin):
   print(f"C[{i}] = {cb}")

print("\nCiphertext Karakter:")
print(f"Ciphertext: {cipher_ascii}")
