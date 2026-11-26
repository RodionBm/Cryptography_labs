import hashlib
import math
import os
import secrets
import sys

P = int(
    "3231700607131100730015351347782516336248805713348907517458843413926"
    "980683413621000279205636264016468545855635793533081692882902308057347"
    "262527355474246124574102620252791657297286270630032526342821314576693"
    "141422365422094111134862999165747826803423055308634905063555771221918"
    "789033272956969612974385624174123623722519734640269185579776797682301"
    "462539793305801522685873076119753243646747585546071504389684494036613"
    "049769781285429595865959756705128385213278446852292550456827287911372"
    "009893187395914337417583782600027803497319855206060753323412260325468"
    "4088120031105907484281003994966956119696956248629032338072839127039"
)
G = 2

def is_probable_prime(n, rounds=64):
    if n < 2:
        return False
    for sp in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % sp == 0:
            return n == sp
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def random_prime(bits):
    while True:
        c = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(c):
            return c

def text_to_int(text):
    h = text.encode("utf-8").hex()
    return h, int(h, 16)

def int_to_text(m):
    b = m.to_bytes((m.bit_length() + 7) // 8, "big")
    return b.hex(), b.decode("utf-8")

def rsa(m):
    e = 65537
    while True:
        p = random_prime(1024)
        q = random_prime(1024)
        n = p * q
        phi = (p - 1) * (q - 1)
        if p != q and n.bit_length() >= 2048 and math.gcd(e, phi) == 1:
            break
    d = pow(e, -1, phi)
    assert m < n
    c = pow(m, e, n)
    m2 = pow(c, d, n)
    assert m2 == m
    return dict(p=p, q=q, n=n, n_bits=n.bit_length(), phi=phi, e=e, d=d,
                check_ed=(e * d) % phi, c=c, m_dec=m2)

def elgamal(m):
    assert m < P
    x = secrets.randbelow(P - 3) + 2          
    y = pow(G, x, P)                         
    while True:
        k = secrets.randbelow(P - 3) + 2     
        if math.gcd(k, P - 1) == 1:
            break
    c1 = pow(G, k, P)                        
    c2 = (m * pow(y, k, P)) % P            
    s = pow(c1, x, P)                      
    s_inv = pow(s, -1, P)                     
    m2 = (c2 * s_inv) % P
    assert m2 == m
    return dict(x=x, y=y, k=k, c1=c1, c2=c2, s=s, s_inv=s_inv, m_dec=m2)

def diffie_hellman():
    a = secrets.randbelow(P - 3) + 2
    b = secrets.randbelow(P - 3) + 2
    A = pow(G, a, P)            
    B = pow(G, b, P)             
    K_alice = pow(B, a, P)     
    K_bob = pow(A, b, P)        
    assert K_alice == K_bob
    K = K_alice
    aes_key_mod = K % (1 << 256)
    k_bytes = K.to_bytes((P.bit_length() + 7) // 8, "big")
    aes_key_sha = hashlib.sha256(k_bytes).hexdigest()
    return dict(a=a, b=b, A=A, B=B, K_alice=K_alice, K_bob=K_bob, K=K,
                aes_key_mod=aes_key_mod, aes_key_mod_hex=f"{aes_key_mod:064x}",
                aes_key_sha_hex=aes_key_sha)

def aes_demo(key_hex, plaintext):
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        return None
    key = bytes.fromhex(key_hex)
    nonce = os.urandom(12)
    ct = AESGCM(key).encrypt(nonce, plaintext.encode(), None)
    pt = AESGCM(key).decrypt(nonce, ct, None).decode()
    return dict(nonce=nonce.hex(), ct=ct.hex(), pt=pt)

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) >= 2:
        name = " ".join(sys.argv[1:])
    else:
        name = input("Introduceți mesajul (Nume Prenume): ").strip()
    if not name:
        sys.exit('Utilizare: python lab5_crypto.py "Nume Prenume"')
    m_hex, m = text_to_int(name)
    r = rsa(m)
    eg = elgamal(m)
    dh = diffie_hellman()
    aes = aes_demo(dh["aes_key_mod_hex"], name)
    out = []
    w = out.append
    w(f"Mesaj: {name!r}")
    w(f"Hex (ASCII): {m_hex}")
    w(f"m (zecimal): {m}")
    w(f"biți m: {m.bit_length()}\n")
    w("=== Sarcina 2.1 RSA ===")
    for k in ("p", "q", "n", "n_bits", "phi", "e", "d", "check_ed", "c", "m_dec"):
        w(f"{k} = {r[k]}")
    w(f"text decriptat = {int_to_text(r['m_dec'])[1]!r}\n")
    w("=== Sarcina 2.2 ElGamal ===")
    w(f"p = {P}\ng = {G}\nbiți p = {P.bit_length()}")
    for k in ("x", "y", "k", "c1", "c2", "s", "s_inv", "m_dec"):
        w(f"{k} = {eg[k]}")
    w(f"text decriptat = {int_to_text(eg['m_dec'])[1]!r}\n")
    w("=== Sarcina 3 Diffie-Hellman ===")
    for k in ("a", "b", "A", "B", "K_alice", "K_bob", "aes_key_mod", "aes_key_mod_hex", "aes_key_sha_hex"):
        w(f"{k} = {dh[k]}")
    w(f"K_alice == K_bob: {dh['K_alice'] == dh['K_bob']}")
    if aes:
        w(f"AES-256-GCM demo: nonce={aes['nonce']} ct={aes['ct']} -> decriptat={aes['pt']!r}")
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "results.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

    wl = f'''(* ===================== Laborator 5 - Criptografia cu chei publice ===================== *)
(* Mesajul: "{name}" -> hex ASCII -> zecimal *)
msg = "{name}";
hex = StringJoin[IntegerString[#, 16, 2] & /@ ToCharacterCode[msg]]   (* {m_hex} *)
m = FromDigits[hex, 16]

(* ============================ Sarcina 2.1  RSA ============================ *)
(* Generare aleatoare (rulați pentru valori noi):
   p = RandomPrime[{{2^1023, 2^1024 - 1}}]; q = RandomPrime[{{2^1023, 2^1024 - 1}}];
   Mai jos sunt valorile folosite în raport: *)
p = {r["p"]};
q = {r["q"]};
PrimeQ[p] && PrimeQ[q]
n = p*q
BitLength[n]                     (* >= 2048 *)
phi = (p - 1)*(q - 1)
e = 65537;
GCD[e, phi]                      (* trebuie să fie 1 *)
d = PowerMod[e, -1, phi]
Mod[e*d, phi]                    (* = 1 *)
c = PowerMod[m, e, n]            (* criptare: c = m^e mod n *)
mDec = PowerMod[c, d, n]         (* decriptare: m = c^d mod n *)
mDec == m
FromCharacterCode[IntegerDigits[mDec, 256]]

(* ============================ Sarcina 2.2  ElGamal ============================ *)
pp = {P};
g = 2;
BitLength[pp]
(* Generare: x = RandomInteger[{{2, pp - 2}}]; k = RandomInteger[{{2, pp - 2}}] cu GCD[k, pp-1]==1 *)
x = {eg["x"]};
y = PowerMod[g, x, pp]           (* cheia publică *)
k = {eg["k"]};
GCD[k, pp - 1]                   (* = 1 *)
c1 = PowerMod[g, k, pp]          (* a = g^k mod p *)
c2 = Mod[m*PowerMod[y, k, pp], pp]  (* b = m * y^k mod p *)
s = PowerMod[c1, x, pp]
sInv = PowerMod[s, -1, pp]
mDec2 = Mod[c2*sInv, pp]
mDec2 == m
FromCharacterCode[IntegerDigits[mDec2, 256]]

(* ============================ Sarcina 3  Diffie-Hellman ============================ *)
(* Generare: a = RandomInteger[{{2, pp - 2}}]; b = RandomInteger[{{2, pp - 2}}] *)
a = {dh["a"]};
b = {dh["b"]};
A = PowerMod[g, a, pp]           (* Alisa -> Bob *)
B = PowerMod[g, b, pp]           (* Bob -> Alisa *)
KA = PowerMod[B, a, pp]          (* calculat de Alisa *)
KB = PowerMod[A, b, pp]          (* calculat de Bob *)
KA == KB
aesKey = Mod[KA, 2^256]          (* cheia AES de 256 biți *)
IntegerString[aesKey, 16, 64]
'''
    with open(os.path.join(here, "lab5.wl"), "w", encoding="utf-8") as f:
        f.write(wl)

    print("\n".join(out))

if __name__ == "__main__":
    main()