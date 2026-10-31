import random
import sys

IP = [58,50,42,34,26,18,10,2, 60,52,44,36,28,20,12,4,
      62,54,46,38,30,22,14,6, 64,56,48,40,32,24,16,8,
      57,49,41,33,25,17,9,1,  59,51,43,35,27,19,11,3,
      61,53,45,37,29,21,13,5, 63,55,47,39,31,23,15,7]
FP = [40,8,48,16,56,24,64,32, 39,7,47,15,55,23,63,31,
      38,6,46,14,54,22,62,30, 37,5,45,13,53,21,61,29,
      36,4,44,12,52,20,60,28, 35,3,43,11,51,19,59,27,
      34,2,42,10,50,18,58,26, 33,1,41,9,49,17,57,25]
E = [32,1,2,3,4,5, 4,5,6,7,8,9, 8,9,10,11,12,13, 12,13,14,15,16,17,
     16,17,18,19,20,21, 20,21,22,23,24,25, 24,25,26,27,28,29, 28,29,30,31,32,1]
P = [16,7,20,21,29,12,28,17, 1,15,23,26,5,18,31,10,
     2,8,24,14,32,27,3,9, 19,13,30,6,22,11,4,25]
PC1 = [57,49,41,33,25,17,9, 1,58,50,42,34,26,18, 10,2,59,51,43,35,27,
       19,11,3,60,52,44,36, 63,55,47,39,31,23,15, 7,62,54,46,38,30,22,
       14,6,61,53,45,37,29, 21,13,5,28,20,12,4]
PC2 = [14,17,11,24,1,5, 3,28,15,6,21,10, 23,19,12,4,26,8, 16,7,27,20,13,2,
       41,52,31,37,47,55, 30,40,51,45,33,48, 44,49,39,56,34,53, 46,42,50,36,29,32]
SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
S = [
 [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
  [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
 [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
  [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
 [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
  [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
 [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
  [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
 [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
  [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
 [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
  [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
 [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
  [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
 [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
  [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]],
]

def group(bits, n):
    return " ".join(bits[i:i + n] for i in range(0, len(bits), n))

def permute(bits, table):
    return "".join(bits[i - 1] for i in table)

def xor(a, b):
    return "".join("1" if x != y else "0" for x, y in zip(a, b))

def lshift(bits, n):
    return bits[n:] + bits[:n]

def text_to_bits(text):
    return "".join(format(ord(c), "08b") for c in text)

def bits_to_hex(bits):
    return format(int(bits, 2), "0%dX" % (len(bits) // 4))

def show_table(name, table, row):
    print(f"\nTabelul {name}:")
    for i in range(0, len(table), row):
        print("  " + " ".join(f"{x:2d}" for x in table[i:i + row]))

def show_sboxes(indices=range(8)):
    for j in indices:
        print(f"\nS{j + 1}:")
        print("        " + " ".join(f"{c:2d}" for c in range(16)))
        for r in range(4):
            print(f"  r={r}   " + " ".join(f"{x:2d}" for x in S[j][r]))

def sbox(j, six):
    row = int(six[0] + six[5], 2)
    col = int(six[1:5], 2)
    val = S[j][row][col]
    return row, col, val, format(val, "04b")

def ask_bits(prompt, n):
    while True:
        s = input(f"{prompt} [{n} biti, binar sau hex cu prefix 0x; 'r' = aleator]: ").strip()
        if s.lower() == "r":
            b = "".join(random.choice("01") for _ in range(n))
            print(f"  generat: {group(b, 8 if n % 8 == 0 else 6)}")
            return b
        s = s.replace(" ", "")
        try:
            if s.lower().startswith("0x"):
                b = bin(int(s, 16))[2:].zfill((len(s) - 2) * 4)
            else:
                int(s, 2)
                b = s
        except ValueError:
            print("  valoare invalida.")
            continue
        if len(b) == n:
            return b
        print(f"  trebuie exact {n} biti (ai introdus {len(b)}).")

def ask_ciphertext_bits(prompt):
    while True:
        s = input(f"{prompt} [binar sau hex cu prefix 0x; 'r' = aleator]: ").strip()
        if s.lower() == "r":
            block_count = ask_int("Numarul de blocuri", 1, 100)
            b = "".join(random.choice("01") for _ in range(block_count * 64))
            print(f"  generat: {group(b, 16)}")
            return b
        s = s.replace(" ", "")
        try:
            if s.lower().startswith("0x"):
                if len(s[2:]) == 0 or len(s[2:]) % 16 != 0:
                    raise ValueError
                b = bin(int(s, 16))[2:].zfill(len(s[2:]) * 4)
            else:
                int(s, 2)
                b = s
        except ValueError:
            print("  valoare hex binar invalida sau lungimea hex nu este un bloc.")
            continue
        if b and len(b) % 64 == 0:
            return b
        print("  lungimea criptotextului trebuie sa fie multiplu de 64 biti.")

def ask_text8(prompt):
    while True:
        s = input(f"{prompt} [8 caractere ASCII; 'r' = aleator]: ")
        if s.lower() == "r":
            s = "".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
                        for _ in range(8))
            print(f"  generat: {s}")
        if len(s) == 8 and all(ord(c) < 128 for c in s):
            return s
        print("  trebuie exact 8 caractere ASCII.")

def ask_int(prompt, lo, hi):
    while True:
        try:
            v = int(input(f"{prompt} [{lo}..{hi}]: "))
            if lo <= v <= hi:
                return v
        except ValueError:
            pass
        print("  valoare invalida.")

def compute_kplus(key_bits, verbose=True):
    kp = permute(key_bits, PC1)
    if verbose:
        show_table("PC-1", PC1, 7)
        print(f"\nCheia K (64 biti)  : {group(key_bits, 8)}")
        print(f"K+ = PC-1(K) (56 b): {group(kp, 7)}")
        print(f"K+ (hex)           : {bits_to_hex(kp)}")
    return kp

def compute_CD(kp, upto, verbose=True):
    C, D = kp[:28], kp[28:]
    if verbose:
        print(f"\nC0 = {group(C, 4)}\nD0 = {group(D, 4)}")
    CD = [(C, D)]
    for i in range(1, upto + 1):
        C, D = lshift(C, SHIFTS[i - 1]), lshift(D, SHIFTS[i - 1])
        CD.append((C, D))
        if verbose:
            print(f"C{i:<2} = {group(C, 4)}   (shift stanga cu {SHIFTS[i - 1]})")
            print(f"D{i:<2} = {group(D, 4)}")
    return CD

def round_key(C, D):
    return permute(C + D, PC2)

def all_round_keys(kp, verbose=False):
    CD = compute_CD(kp, 16, verbose)
    return [round_key(*CD[i]) for i in range(1, 17)]

def task_2_1():
    key = ask_text8("Cheia DES")
    kb = text_to_bits(key)
    print("\nCaractere -> cod ASCII pe 8 biti:")
    for c in key:
        print(f"  '{c}' = {ord(c):3d} = {format(ord(c), '08b')}")
    compute_kplus(kb)

def task_2_2():
    kp = ask_bits("K+", 56)
    i = ask_int("i", 0, 16)
    print(f"\nK+ = {group(kp, 7)}")
    show_table("deplasari (nr. de shift-uri stanga per runda)", SHIFTS, 16)
    CD = compute_CD(kp, i)
    print(f"\nRezultat: C{i} = {CD[i][0]}\n          D{i} = {CD[i][1]}")

def task_2_3():
    kp = ask_bits("K+", 56)
    i = ask_int("i", 1, 16)
    CD = compute_CD(kp, i)
    show_table("PC-2", PC2, 6)
    CDc = CD[i][0] + CD[i][1]
    ki = round_key(*CD[i])
    print(f"\nC{i}D{i} (56 b): {group(CDc, 7)}")
    print(f"K{i} = PC-2(C{i}D{i}) (48 b): {group(ki, 6)}")
    print(f"K{i} (hex): {bits_to_hex(ki)}")

def task_2_4():
    m = ask_text8("Mesajul")
    mb = text_to_bits(m)
    print("\nMesaj in binar:")
    for c in m:
        print(f"  '{c}' = {format(ord(c), '08b')}")
    show_table("IP", IP, 8)
    ip = permute(mb, IP)
    L0, R0 = ip[:32], ip[32:]
    print(f"\nM        = {group(mb, 8)}")
    print(f"IP(M)    = {group(ip, 8)}")
    print(f"L0 = {group(L0, 8)}\nR0 = {group(R0, 8)}")
    print(f"\nL1 = R0 = {group(R0, 8)}   (hex: {bits_to_hex(R0)})")

def task_2_5():
    kp = ask_bits("K+", 56)
    show_table("PC-2", PC2, 6)
    CD = compute_CD(kp, 16)
    print("\nCheile de runda K1..K16:")
    for i in range(1, 17):
        ki = round_key(*CD[i])
        print(f"K{i:<2} = {group(ki, 6)}   hex={bits_to_hex(ki)}")

def task_2_6():
    i = ask_int("Runda i", 1, 16)
    ki = ask_bits(f"K{i}", 48)
    r = ask_bits(f"R{i - 1}", 32)
    show_table("E (expansiune 32 -> 48)", E, 6)
    er = permute(r, E)
    x = xor(ki, er)
    print(f"\nR{i - 1}          = {group(r, 8)}")
    print(f"E(R{i - 1})       = {group(er, 6)}")
    print(f"K{i}            = {group(ki, 6)}")
    print(f"K{i} + E(R{i - 1}) = {group(x, 6)}")
    print("\nB1B2...B8:")
    for j in range(8):
        print(f"  B{j + 1} = {x[6 * j:6 * j + 6]}")

def task_2_7():
    x = ask_bits("B1B2...B8 (concatenat)", 48)
    show_sboxes()
    out = ""
    print("\nCalcul S-box:")
    for j in range(8):
        b = x[6 * j:6 * j + 6]
        row, col, val, v4 = sbox(j, b)
        out += v4
        print(f"  B{j + 1}={b}: rand=({b[0]}{b[5]})={row}, col=({b[1:5]})={col}"
              f" -> S{j + 1}={val:2d} = {v4}")
    print(f"\nS1(B1)...S8(B8) = {group(out, 4)}")
    print(f"                = {out}   (hex: {bits_to_hex(out)})")

def task_2_8():
    k = ask_int("Runda k", 1, 16)
    l = ask_bits(f"L{k - 1}", 32)
    s = ask_bits("Rezultatul cutiilor S (32 biti)", 32)
    show_table("P", P, 8)
    ps = permute(s, P)
    r = xor(l, ps)
    print(f"\nS-out        = {group(s, 8)}")
    print(f"P(S-out)     = {group(ps, 8)}")
    print(f"L{k - 1}         = {group(l, 8)}")
    print(f"R{k} = L{k - 1} + P(S-out) = {group(r, 8)}   (hex: {bits_to_hex(r)})")

def task_2_9():
    x = ask_bits("Ki + E(Ri-1)", 48)
    j = ask_int("j (cutia S)", 1, 8)
    b = x[6 * (j - 1):6 * j]
    print(f"\nKi + E(Ri-1) = {group(x, 6)}")
    for t in range(8):
        print(f"  B{t + 1} = {x[6 * t:6 * t + 6]}")
    show_sboxes([j - 1])
    row, col, val, v4 = sbox(j - 1, b)
    print(f"\nB{j} = {b}")
    print(f"rand   = primul+ultimul bit = {b[0]}{b[5]} = {row}")
    print(f"coloana= biti mijlocii      = {b[1:5]} = {col}")
    print(f"S{j}(B{j}) = {val} = {v4}")

def task_2_10():
    i = ask_int("Runda i", 1, 16)
    s = ask_bits("S1(B1)...S8(B8) (32 biti)", 32)
    l = ask_bits(f"L{i - 1}", 32)
    show_table("P", P, 8)
    ps = permute(s, P)
    r = xor(l, ps)
    print(f"\nS1(B1)...S8(B8) = {group(s, 4)}")
    print(f"f = P(...)      = {group(ps, 8)}")
    print(f"L{i - 1}            = {group(l, 8)}")
    print(f"R{i} = L{i - 1} + f = {group(r, 8)}   (hex: {bits_to_hex(r)})")

def task_2_11():
    l16 = ask_bits("L16", 32)
    r16 = ask_bits("R16", 32)
    show_table("IP^-1 (permutarea finala)", FP, 8)
    pre = r16 + l16
    c = permute(pre, FP)
    print(f"\nL16 = {group(l16, 8)}\nR16 = {group(r16, 8)}")
    print(f"R16L16 (se inverseaza!) = {group(pre, 8)}")
    print(f"C = IP^-1(R16L16)       = {group(c, 8)}")
    print(f"\nBloc criptat (hex): {bits_to_hex(c)}")

def feistel(r, ki, verbose=False):
    er = permute(r, E)
    x = xor(ki, er)
    out = ""
    for j in range(8):
        out += sbox(j, x[6 * j:6 * j + 6])[3]
    return permute(out, P)

def des_encrypt_block(block_bits, key_bits, rounds=16, verbose=False):
    keys = all_round_keys(compute_kplus(key_bits, False))
    ip = permute(block_bits, IP)
    L, R = ip[:32], ip[32:]
    if verbose:
        print(f"IP = {group(ip, 8)}\nL0 = {group(L, 8)}\nR0 = {group(R, 8)}")
    for i in range(1, rounds + 1):
        L, R = R, xor(L, feistel(R, keys[i - 1]))
        if verbose:
            print(f"Runda {i:2d}: K={bits_to_hex(keys[i - 1])} L={bits_to_hex(L)} R={bits_to_hex(R)}")
    return permute(R + L, FP)

def des_decrypt_block(block_bits, key_bits, verbose=False):
    keys = list(reversed(all_round_keys(compute_kplus(key_bits, False))))
    ip = permute(block_bits, IP)
    L, R = ip[:32], ip[32:]
    if verbose:
        print(f"IP = {group(ip, 8)}\nL16 = {group(L, 8)}\nR16 = {group(R, 8)}")
    for round_index, key in enumerate(keys, 1):
        L, R = R, xor(L, feistel(R, key))
        if verbose:
            print(f"Runda inversa {round_index:2d}: K={bits_to_hex(key)} "
                  f"L={bits_to_hex(L)} R={bits_to_hex(R)}")
    return permute(R + L, FP)

def pkcs7_pad(text_bits):
    remainder = len(text_bits) % 64
    padding_bits = 64 - remainder if remainder else 64
    padding_byte = padding_bits // 8
    return text_bits + format(padding_byte, "08b") * padding_byte

def pkcs7_unpad(text_bits):
    if not text_bits or len(text_bits) % 64 != 0 or len(text_bits) == 0:
        raise ValueError("lungimea textului nu este multiplu de bloc")
    padding_byte = int(text_bits[-8:], 2)
    if padding_byte < 1 or padding_byte > 8:
        raise ValueError("padding-ul DES nu este valid")
    padding = format(padding_byte, "08b") * padding_byte
    if text_bits[-padding_byte * 8:] != padding:
        raise ValueError("padding-ul DES nu este valid")
    return text_bits[:-padding_byte * 8]

def des_encrypt_text(text, key, verbose=False):
    plaintext_bits = text_to_bits(text)
    padded_bits = pkcs7_pad(plaintext_bits)
    ciphertext = []
    for offset in range(0, len(padded_bits), 64):
        ciphertext.append(des_encrypt_block(
            padded_bits[offset:offset + 64], text_to_bits(key), verbose=verbose))
    return "".join(ciphertext), bits_to_hex("".join(ciphertext))

def des_decrypt_text(ciphertext_bits, key):
    if not ciphertext_bits or len(ciphertext_bits) % 64 != 0:
        raise ValueError("criptotextul trebuie sa contina unul sau mai multe blocuri de 64 biti")
    plaintext_padded = ""
    for offset in range(0, len(ciphertext_bits), 64):
        plaintext_padded += des_decrypt_block(
            ciphertext_bits[offset:offset + 64], text_to_bits(key))
    plaintext_bits = pkcs7_unpad(plaintext_padded)
    try:
        characters = [chr(int(plaintext_bits[i:i + 8], 2))
                      for i in range(0, len(plaintext_bits), 8)]
        if any(ord(c) >= 128 for c in characters):
            raise ValueError
        return "".join(characters)
    except ValueError as exc:
        raise ValueError("plaintext-ul decriptat nu este ASCII valid") from exc

def task_full():
    m = ask_text8("Blocul de mesaj")
    k = ask_text8("Cheia")
    c = des_encrypt_block(text_to_bits(m), text_to_bits(k), verbose=True)
    print(f"\nBloc criptat: {group(c, 8)}\nHex         : {bits_to_hex(c)}")

def task_full_text():
    m = input("Textul de criptat: ")
    k = ask_text8("Cheia")
    c, c_hex = des_encrypt_text(m, k)
    print(f"\nText criptat (binar, padding PKCS#7): {group(c, 8)}")
    print(f"Text criptat (hex):                    {c_hex}")

def task_full_decrypt():
    c = ask_ciphertext_bits("Criptotextul")
    k = ask_text8("Cheia")
    try:
        recovered = des_decrypt_text(c, k)
        print(f"\nText decriptat: {recovered}")
    except ValueError as exc:
        print(f"\nEROARE: {exc}")

def self_test():
    k = format(0x133457799BBCDFF1, "064b")
    m = format(0x0123456789ABCDEF, "064b")
    got = bits_to_hex(des_encrypt_block(m, k))
    decrypted = bits_to_hex(des_decrypt_block(format(int(got, 16), "064b"), k))
    print("Self-test criptare:",
          "OK" if got == "85E813540F0AB405" else f"EROARE ({got})")
    print("Self-test decriptare:",
          "OK" if decrypted == "0123456789ABCDEF" else f"EROARE ({decrypted})")

TASKS = {
    1: ("K+ din cheia de 8 simboluri", task_2_1),
    2: ("Ci si Di pentru un i dat", task_2_2),
    3: ("Cheia de runda Ki", task_2_3),
    4: ("L1 din mesajul de 8 caractere", task_2_4),
    5: ("Toate cele 16 chei de runda", task_2_5),
    6: ("B1..B8 = Ki + E(Ri-1)", task_2_6),
    7: ("S1(B1)...S8(B8) din B1..B8", task_2_7),
    8: ("Ri din Lk-1 si iesirea cutiilor S", task_2_8),
    9: ("Sj(Bj) pentru un j dat", task_2_9),
    10: ("Ri din iesirea cutiilor S si Li-1", task_2_10),
    11: ("Blocul criptat din L16, R16", task_2_11),
    12: ("(bonus) Criptare DES completa a unui bloc", task_full),
    13: ("(bonus) Criptare text DES cu padding PKCS#7", task_full_text),
    14: ("(bonus) Decriptare text DES cu padding PKCS#7", task_full_decrypt),
}

def main():
    self_test()
    while True:
        print("\n=== DES - Lucrare de laborator nr. 4 ===")
        for n, (d, _) in TASKS.items():
            print(f" 2.{n:<2} {d}" if n <= 11 else f"{n:>4}  {d}")
        print("  0  Iesire")
        try:
            c = ask_int("Alege", 0, max(TASKS))
        except (EOFError, KeyboardInterrupt):
            break
        if c == 0:
            break
        TASKS[c][1]()

if __name__ == "__main__":
    main()