import re
import base64
import hashlib
import argparse
import json
from urllib.parse import unquote


def ghici_strat(s):
    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"
    return "necunoscut"


def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    if strat == "hex":
        return strat, bytes.fromhex(s)
    if strat == "url":
        return strat, unquote(s).encode()
    return strat, s.encode()


def citibil(b):
    return all(32 <= c < 127 for c in b)


def desfa_tot(val):
    for _ in range(8):
        strat, b = desfa(val)
        if strat == "necunoscut" or not citibil(b):
            break
        val = b.decode()
    return val


def sparge_xor(date):
    for k in range(256):
        clar = bytes(x ^ k for x in date)
        if citibil(clar):
            return k, clar.decode()
    return None, None


def sparge_hash(tinta):
    if len(tinta) == 32:
        algoritm = "md5"
    elif len(tinta) == 40:
        algoritm = "sha1"
    elif len(tinta) == 64:
        algoritm = "sha256"
    else:
        return None, None
    for cuv in open("probe/wordlist.txt", encoding="latin1"):
        cuv = cuv.strip()
        h = hashlib.new(algoritm, cuv.encode()).hexdigest()
        if h == tinta:
            return algoritm, cuv
    return algoritm, None


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    if a.fisier:
        s = open(a.intrare, encoding="latin1").read().strip()
    else:
        s = a.intrare

    rezultat = desfa_tot(s)
    fisa = {"intrare": s, "rezultat": rezultat}
    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
        json.dump(fisa, f, ensure_ascii=False, indent=2)

    print("rezultat:", rezultat)
    print("fisa salvata in arsenal/forensics/fisa.json")