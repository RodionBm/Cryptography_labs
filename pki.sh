#!/usr/bin/env bash
# =============================================================================
#  Laborator nr. 5 - Infrastructură cu chei publice (PKI) și semnătură digitală
#  PKI internă construită cu OpenSSL.
#
#  Utilizare:
#    ./pki.sh init                          - inițializează CA (cheie RSA 4096 + cert. self-signed 3650 zile)
#    ./pki.sh issue  <user> [biți]          - emite cheie RSA (>=2048) + certificat 365 zile pentru utilizator
#    ./pki.sh revoke <user> [motiv]         - revocă certificatul utilizatorului și regenerează CRL
#    ./pki.sh sign   <user> <fișier>        - semnează fișierul (RSA + SHA-256) -> <fișier>.<user>.sig
#    ./pki.sh verify <user> <fișier> [sig]  - verifică certificatul (lanț + CRL) și semnătura
#    ./pki.sh list                          - afișează baza de date a certificatelor emise
#    ./pki.sh show   <user>                 - afișează detaliile certificatului utilizatorului
# =============================================================================
set -euo pipefail

# În Git Bash (MSYS) argumentele de tip "/CN=..." sunt convertite în căi Windows;
# dezactivăm această conversie.
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL="*"

cd "$(dirname "$0")"
CNF="./openssl.cnf"
CA_DIR="./ca"
USERS_DIR="./users"
CA_KEY="$CA_DIR/private/ca.key.pem"
CA_CERT="$CA_DIR/certs/ca.cert.pem"
CA_CRL="$CA_DIR/crl/ca.crl.pem"

CA_SUBJ="/C=MD/L=Chisinau/O=UTM Lab PKI/OU=Criptografie/CN=UTM Lab Root CA"

info() { printf '\033[1;34m[*]\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m[+]\033[0m %s\n' "$*"; }
err()  { printf '\033[1;31m[-]\033[0m %s\n' "$*" >&2; }
die()  { err "$*"; exit 1; }

require_ca() { [[ -f "$CA_CERT" && -f "$CA_KEY" ]] || die "CA nu este inițializată. Rulați: $0 init"; }

# -----------------------------------------------------------------------------
gen_crl() {
    # Generează lista certificatelor revocate (CRL), semnată de CA
    openssl ca -config "$CNF" -gencrl -out "$CA_CRL" -batch 2>/dev/null
}

# -----------------------------------------------------------------------------
cmd_init() {
    [[ -f "$CA_KEY" ]] && die "CA există deja ($CA_KEY). Ștergeți directorul '$CA_DIR' pentru reinițializare."

    info "Creare structură directoare CA"
    mkdir -p "$CA_DIR"/{certs,crl,newcerts,private} "$USERS_DIR"
    chmod 700 "$CA_DIR/private"
    : > "$CA_DIR/index.txt"            # baza de date a certificatelor
    echo 1000 > "$CA_DIR/serial"        # primul număr serial
    echo 1000 > "$CA_DIR/crlnumber"     # primul număr CRL

    info "Generare cheie privată rădăcină RSA 4096 biți"
    openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out "$CA_KEY"
    chmod 400 "$CA_KEY"

    info "Generare certificat auto-semnat CA (valabil 3650 zile)"
    openssl req -config "$CNF" -new -x509 -key "$CA_KEY" -sha256 \
        -days 3650 -subj "$CA_SUBJ" -extensions v3_ca -out "$CA_CERT"

    gen_crl
    ok "CA inițializată:"
    openssl x509 -in "$CA_CERT" -noout -subject -issuer -dates
    openssl x509 -in "$CA_CERT" -noout -text | grep -E "Public-Key|CA:"
}

# -----------------------------------------------------------------------------
cmd_issue() {
    require_ca
    local user="${1:?Specificați numele utilizatorului}"
    local bits="${2:-2048}"
    (( bits >= 2048 )) || die "Dimensiunea cheii trebuie să fie de minim 2048 biți."

    local udir="$USERS_DIR/$user"
    if [[ -f "$udir/$user.cert.pem" ]] && ! is_revoked "$user"; then
        die "Utilizatorul '$user' are deja un certificat valid. Revocați-l mai întâi."
    fi
    if [[ -d "$udir" ]]; then
        # Cheia/certificatul vechi (revocat) se arhivează, nu se șterg
        local arch="$udir/revoked-$(date +%Y%m%d%H%M%S)"
        mkdir -p "$arch"
        find "$udir" -maxdepth 1 -type f -exec mv {} "$arch"/ \;
        info "Cheia și certificatul vechi au fost arhivate în $arch"
    fi
    mkdir -p "$udir"

    info "Generare cheie privată RSA $bits biți pentru '$user'"
    openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:"$bits" -out "$udir/$user.key.pem"
    chmod 400 "$udir/$user.key.pem" 2>/dev/null || true

    info "Generare cerere de semnare a certificatului (CSR)"
    openssl req -config "$CNF" -new -key "$udir/$user.key.pem" -sha256 \
        -subj "/C=MD/O=UTM Lab PKI/OU=Utilizatori/CN=$user" -out "$udir/$user.csr.pem"

    info "CA semnează CSR-ul -> certificat valabil 365 zile"
    openssl ca -config "$CNF" -extensions usr_cert -days 365 -notext -md sha256 -batch \
        -in "$udir/$user.csr.pem" -out "$udir/$user.cert.pem"

    ok "Certificat emis pentru '$user':"
    openssl x509 -in "$udir/$user.cert.pem" -noout -subject -issuer -serial -dates
    openssl verify -CAfile "$CA_CERT" "$udir/$user.cert.pem"
}

# -----------------------------------------------------------------------------
is_revoked() {
    local cert="$USERS_DIR/$1/$1.cert.pem"
    [[ -f "$cert" ]] || return 1
    local serial
    serial=$(openssl x509 -in "$cert" -noout -serial | cut -d= -f2)
    grep -qE "^R.*[[:space:]]$serial[[:space:]]" "$CA_DIR/index.txt"
}

cmd_revoke() {
    require_ca
    local user="${1:?Specificați numele utilizatorului}"
    local reason="${2:-keyCompromise}"
    local cert="$USERS_DIR/$user/$user.cert.pem"
    [[ -f "$cert" ]] || die "Nu există certificat pentru '$user'."
    is_revoked "$user" && die "Certificatul lui '$user' este deja revocat."

    info "Revocare certificat '$user' (motiv: $reason)"
    openssl ca -config "$CNF" -revoke "$cert" -crl_reason "$reason" -batch

    info "Regenerare CRL"
    gen_crl
    ok "Certificat revocat. Conținut CRL:"
    openssl crl -in "$CA_CRL" -noout -text | grep -A3 "Serial Number" || true
}

# -----------------------------------------------------------------------------
# Verifică certificatul utilizatorului: lanțul până la CA + lista de revocare
check_cert() {
    local cert="$1"
    openssl verify -CAfile "$CA_CERT" -CRLfile "$CA_CRL" -crl_check "$cert"
}

cmd_sign() {
    require_ca
    local user="${1:?Specificați utilizatorul}" file="${2:?Specificați fișierul}"
    local key="$USERS_DIR/$user/$user.key.pem" cert="$USERS_DIR/$user/$user.cert.pem"
    [[ -f "$key" && -f "$cert" ]] || die "Utilizatorul '$user' nu are cheie/certificat."
    [[ -f "$file" ]] || die "Fișierul '$file' nu există."

    info "Verificare validitate certificat '$user' înainte de semnare"
    check_cert "$cert" || die "Certificatul lui '$user' NU este valid (revocat/expirat). Semnarea refuzată."

    local sig="$file.$user.sig"
    info "Semnare: hash SHA-256 al fișierului, criptat cu cheia privată RSA a lui '$user'"
    openssl dgst -sha256 -sign "$key" -out "$sig" "$file"
    ok "Semnătura salvată în: $sig"
}

cmd_verify() {
    require_ca
    local user="${1:?Specificați utilizatorul}" file="${2:?Specificați fișierul}"
    local sig="${3:-$file.$user.sig}"
    local cert="$USERS_DIR/$user/$user.cert.pem"
    [[ -f "$cert" ]] || die "Nu există certificat pentru '$user'."
    [[ -f "$sig" ]] || die "Semnătura '$sig' nu există."

    info "Pas 1: verificare certificat (lanț de încredere + CRL)"
    if ! check_cert "$cert"; then
        err "Certificatul lui '$user' nu este de încredere -> semnătura NU este acceptată."
        return 1
    fi

    info "Pas 2: extragere cheie publică din certificat"
    local pub="$USERS_DIR/$user/$user.pub.pem"
    openssl x509 -in "$cert" -noout -pubkey > "$pub"

    info "Pas 3: verificare semnătură RSA/SHA-256"
    if openssl dgst -sha256 -verify "$pub" -signature "$sig" "$file"; then
        ok "Semnătura este VALIDĂ: fișierul a fost semnat de '$user' și nu a fost modificat."
    else
        err "Semnătura este INVALIDĂ (fișier modificat sau semnătură falsă)."
        return 1
    fi
}

# -----------------------------------------------------------------------------
cmd_list() {
    require_ca
    echo "Stare | Expiră        | Revocat la    | Serial | Subiect"
    awk -F'\t' '{printf "%-5s | %s | %-13s | %s | %s\n", $1, $2, ($3==""?"-":$3), $4, $6}' "$CA_DIR/index.txt"
}

cmd_show() {
    local cert="$USERS_DIR/${1:?Specificați utilizatorul}/$1.cert.pem"
    [[ -f "$cert" ]] || die "Nu există certificat pentru '$1'."
    openssl x509 -in "$cert" -noout -text
}

# -----------------------------------------------------------------------------
case "${1:-}" in
    init)   shift; cmd_init "$@" ;;
    issue)  shift; cmd_issue "$@" ;;
    revoke) shift; cmd_revoke "$@" ;;
    sign)   shift; cmd_sign "$@" ;;
    verify) shift; cmd_verify "$@" ;;
    list)   shift; cmd_list ;;
    show)   shift; cmd_show "$@" ;;
    *)      sed -n '2,15p' "$0"; exit 1 ;;
esac
