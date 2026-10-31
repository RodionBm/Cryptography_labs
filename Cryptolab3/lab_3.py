import re
import sys

ALFABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
SIMBOLURI_COMPLETARE = "01234"
SIMBOLURI_MATRICE = ALFABET + SIMBOLURI_COMPLETARE
RANDURI, COLOANE = 6, 6
LUNGIME_MINIMA_CHEIE = 7
CARACTER_COMPLETARE = "X"
CARACTER_COMPLETARE_ALTERNATIV = "Q"
assert len(ALFABET) == 31 and len(set(ALFABET)) == 31
assert len(SIMBOLURI_MATRICE) == RANDURI * COLOANE

def normalizeaza_text(text, nume="Text"):
    if not text or not text.strip():
        raise ValueError(f"{nume} nu poate fi gol.")
    if not re.fullmatch(r"[A-Za-z ]+", text):
        raise ValueError(
            f"{nume} contine caractere nepermise. "
            "Diapazon permis: literele 'A'-'Z' si 'a'-'z' "
            "(spatiile sunt eliminate)."
        )
    return text.replace(" ", "").upper()

def valideaza_cheie(cheie):
    cheie = normalizeaza_text(cheie, "Cheia")
    if len(cheie) < LUNGIME_MINIMA_CHEIE:
        raise ValueError(
            f"Cheia trebuie sa aiba cel putin {LUNGIME_MINIMA_CHEIE} "
            f"litere dupa eliminarea spatiilor (ai introdus {len(cheie)})."
        )
    return cheie

def normalizeaza_criptograma(criptograma):
    if not criptograma or not criptograma.strip():
        raise ValueError("Criptograma nu poate fi goala.")
    simboluri = []
    for caracter in criptograma:
        if caracter == " ":
            continue
        majuscula = caracter.upper()
        if len(majuscula) != 1 or majuscula not in SIMBOLURI_MATRICE:
            raise ValueError(
                f"Caracter invalid in criptograma: {caracter!r}. "
                "Diapazon permis: literele alfabetului romanesc "
                f"({ALFABET}) si cifrele {SIMBOLURI_COMPLETARE}."
            )
        simboluri.append(majuscula)
    rezultat = "".join(simboluri)
    if len(rezultat) % 2:
        raise ValueError("Criptograma trebuie sa aiba un numar par de simboluri.")
    return rezultat

def construieste_matrice(cheie):
    cheie = valideaza_cheie(cheie)
    simboluri = []
    vazute = set()
    for caracter in cheie + ALFABET + SIMBOLURI_COMPLETARE:
        if caracter not in vazute:
            vazute.add(caracter)
            simboluri.append(caracter)
    if len(simboluri) != RANDURI * COLOANE:
        raise ValueError("Nu s-a putut construi matricea Playfair 6x6.")
    return [
        simboluri[i * COLOANE:(i + 1) * COLOANE]
        for i in range(RANDURI)
    ]

def afiseaza_matrice(matrice):
    print("\nMatricea de criptare:")
    for rand in matrice:
        print("  " + " ".join(rand))
    print()

def construieste_index(matrice):
    return {
        caracter: (rand, coloana)
        for rand, linie in enumerate(matrice)
        for coloana, caracter in enumerate(linie)
    }

def pregateste_perechi(mesaj):
    text = normalizeaza_text(mesaj, "Mesajul")
    perechi = []
    index = 0
    while index < len(text):
        primul = text[index]
        completare = (
            CARACTER_COMPLETARE
            if primul != CARACTER_COMPLETARE
            else CARACTER_COMPLETARE_ALTERNATIV
        )
        if index + 1 >= len(text):
            perechi.append(primul + completare)
            index += 1
        elif text[index] == text[index + 1]:
            perechi.append(primul + completare)
            index += 1
        else:
            perechi.append(text[index:index + 2])
            index += 2
    return perechi

def transforma_pereche(matrice, index, primul, al_doilea, directie):
    rand1, coloana1 = index[primul]
    rand2, coloana2 = index[al_doilea]
    if rand1 == rand2:
        return (
            matrice[rand1][(coloana1 + directie) % COLOANE]
            + matrice[rand2][(coloana2 + directie) % COLOANE]
        )
    if coloana1 == coloana2:
        return (
            matrice[(rand1 + directie) % RANDURI][coloana1]
            + matrice[(rand2 + directie) % RANDURI][coloana2]
        )
    return matrice[rand1][coloana2] + matrice[rand2][coloana1]

def cripteaza(matrice, mesaj):
    perechi = pregateste_perechi(mesaj)
    index = construieste_index(matrice)
    rezultat = "".join(
        transforma_pereche(matrice, index, pereche[0], pereche[1], 1)
        for pereche in perechi
    )
    return perechi, rezultat

def decripteaza(matrice, criptograma):
    text = normalizeaza_criptograma(criptograma)
    index = construieste_index(matrice)
    return "".join(
        transforma_pereche(matrice, index, text[i], text[i + 1], -1)
        for i in range(0, len(text), 2)
    )

def citeste_valid(prompt, validator):
    while True:
        try:
            return validator(input(prompt))
        except ValueError as eroare:
            print(f"  [!] {eroare}")

def citeste_operatia():
    while True:
        optiune = input(
            "Alege operatia (1 = criptare, 2 = decriptare, 0 = iesire): "
        ).strip().upper()
        if optiune in ("1", "C"):
            return "C"
        if optiune in ("2", "D"):
            return "D"
        if optiune == "0":
            return "0"
        print("  [!] Optiune invalida. Alege 1, 2 sau 0.")

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 60)
    print(" Cifrul Playfair - alfabet romanesc (31 de litere)")
    print("=" * 60)
    print("Cheia si mesajul accepta literele A-Z/a-z; spatiile se elimina.")
    while True:
        operatie = citeste_operatia()
        if operatie == "0":
            print("La revedere!")
            return
        cheie = citeste_valid(
            f"Cheia (minimum {LUNGIME_MINIMA_CHEIE} litere): ",
            valideaza_cheie,
        )
        matrice = construieste_matrice(cheie)
        afiseaza_matrice(matrice)
        if operatie == "C":
            mesaj = citeste_valid(
                "Mesajul de criptat: ",
                lambda text: normalizeaza_text(text, "Mesajul"),
            )
            perechi, criptograma = cripteaza(matrice, mesaj)
            print(f"Mesaj pregatit (perechi): {' '.join(perechi)}")
            print(f"Criptograma: {criptograma}")
        else:
            criptograma = citeste_valid(
                "Criptograma: ",
                normalizeaza_criptograma,
            )
            mesaj = decripteaza(matrice, criptograma)
            print(f"Mesaj decriptat: {mesaj}")
            print(
                "(Elimina manual literele X/Q de completare si "
                "reintrodu spatiile conform sensului.)"
            )

if __name__ == "__main__":
    main()
