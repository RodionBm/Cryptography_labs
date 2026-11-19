import random

P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

def group(bits, n):
    return " ".join(bits[i:i + n] for i in range(0, len(bits), n))

def permute(bits, table):
    return "".join(bits[i - 1] for i in table)

def xor(a, b):
    return "".join("1" if x != y else "0" for x, y in zip(a, b))

def bits_to_hex(bits):
    return format(int(bits, 2), "0%dX" % (len(bits) // 4))

def show_table(name, table, row):
    print(f"\nTabelul {name}:")
    for i in range(0, len(table), row):
        print("  " + " ".join(f"{x:2d}" for x in table[i:i + row]))

def ask_int(prompt, lo, hi):
    while True:
        s = input(f"{prompt} [{lo}..{hi}; 'r' = aleator]: ").strip()
        if s.lower() == "r":
            v = random.randint(lo, hi)
            print(f"  generat: {v}")
            return v
        try:
            v = int(s)
            if lo <= v <= hi:
                return v
        except ValueError:
            pass
        print("  valoare invalida.")

def ask_bits(prompt, n):
    while True:
        s = input(f"{prompt} [{n} biti: binar sau hex cu prefix 0x; 'r' = aleator]: ").strip()
        if s.lower() == "r":
            b = "".join(random.choice("01") for _ in range(n))
            print(f"  generat: {group(b, 4)}  (hex {bits_to_hex(b)})")
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

def compute_rk(k, l_prev, s_out, verbose=True):
    f = permute(s_out, P)
    r_k = xor(l_prev, f)
    if not verbose:
        return r_k
    print(f"\n   Runda k = {k}")
    print(f"{'L' + str(k - 1):<5} = {group(l_prev, 4)}   (hex {bits_to_hex(l_prev)})")
    print(f"S-out = {group(s_out, 4)}   (hex {bits_to_hex(s_out)})")
    print("\nPasul 1. Iesirea cutiilor S (8 grupe de 4 biti):")
    for j in range(8):
        v = s_out[4 * j:4 * j + 4]
        print(f"  S{j + 1}(B{j + 1}) = {v} = {int(v, 2):2d}"
              f"   (bitii {4 * j + 1:2d}..{4 * j + 4:2d})")
    show_table("P (permutare 32 -> 32)", P, 8)
    print("\nPasul 2. f = P(S-out): bitul j al lui f = bitul P[j] din S-out")
    for row in range(4):
        idx = P[8 * row:8 * row + 8]
        picked = "".join(s_out[i - 1] for i in idx)
        pos = f"{8 * row + 1:2d}..{8 * row + 8:2d}"
        print(f"  f[{pos}] <- S-out[" + ",".join(f"{i:2d}" for i in idx) + f"] = {group(picked, 4)}")
    print(f"  f = P(S-out) = {group(f, 4)}   (hex {bits_to_hex(f)})")
    print(f"\nPasul 3. R{k} = L{k - 1} XOR f (bit cu bit, 0^0=0, 0^1=1, 1^0=1, 1^1=0):")
    print(f"  {'L' + str(k - 1):<9} = {group(l_prev, 4)}")
    print(f"  f         = {group(f, 4)}")
    print("  " + "-" * 50)
    print(f"  {'R' + str(k):<9} = {group(r_k, 4)}")
    print(f"\nRezultat: R{k} = {r_k}")
    print(f"          R{k} (hex) = {bits_to_hex(r_k)}")
    if k < 16:
        print(f"(Nota: L{k} = R{k - 1}; R{k} intra in functia f in runda {k + 1}.)")
    else:
        print("(Nota: dupa runda 16 urmeaza swap-ul R16L16 si permutarea finala IP^-1.)")
    return r_k

def task_2_8():
    k = ask_int("Runda k", 1, 16)
    l_prev = ask_bits(f"L{k - 1}", 32)
    s_out = ask_bits("Rezultatul cutiilor S, S1(B1)...S8(B8)", 32)
    compute_rk(k, l_prev, s_out)

def example():
    print("\nExemplul clasic: K = 133457799BBCDFF1, M = 0123456789ABCDEF, runda 1.")
    print("Din IP(M) se obtine L0 = CC00CCFF, iar cutiile S dau S-out = 5C82B597.")
    l0 = format(0xCC00CCFF, "032b")
    s = format(0x5C82B597, "032b")
    r1 = compute_rk(1, l0, s)
    print("Valoarea asteptata din literatura: R1 = EF4A6544 ->",
          "OK" if bits_to_hex(r1) == "EF4A6544" else "EROARE")

def self_test():
    assert sorted(P) == list(range(1, 33)), "P nu este o permutare"
    got = bits_to_hex(compute_rk(1, format(0xCC00CCFF, "032b"),
                                 format(0x5C82B597, "032b"), verbose=False))
    print("Self-test (R1 = EF4A6544):", "OK" if got == "EF4A6544" else f"EROARE ({got})")

def main():
    self_test()
    while True:
        print("\n  DES, Sarcina 2.8: R_k din L_(k-1) si iesirea cutiilor S")
        print(" 1  Calculeaza R_k (date introduse sau generate aleator)")
        print(" 2  Exemplul clasic (vectorul de test DES, runda 1)")
        print(" 0  Iesire")
        c = input("Alege: ").strip()
        if c == "1":
            task_2_8()
        elif c == "2":
            example()
        elif c == "0":
            break
        else:
            print("  optiune invalida.")

if __name__ == "__main__":
    main()