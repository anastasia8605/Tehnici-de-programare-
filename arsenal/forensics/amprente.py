import os, hashlib, argparse

MAGIC = {b"\x89PNG": "PNG", b"%PDF": "PDF", b"PK\x03\x04": "ZIP"}


def tip(head):
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    return "necunoscut"          # DUPA bucla, nu in ea!


def amprenta_fisier(cale):
    with open(cale, "rb") as f:      # "rb" = binar; with = inchide singur
        date = f.read()
    return {"nume": os.path.basename(cale),
            "tip": tip(date[:8]),
            "sha256": hashlib.sha256(date).hexdigest()[:16]}


def scaneaza(folder):
    rez = []
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            rez.append(amprenta_fisier(cale))
    return rez


def amprente_lenes(folder):
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            yield amprenta_fisier(cale)   # produce unul, apoi se opreste


def main():
    parser = argparse.ArgumentParser(description="Amprente forensics")
    parser.add_argument("folder", help="folderul cu probe")
    args = parser.parse_args()
    for fisa in scaneaza(args.folder):
        print(f"{fisa['nume']:14} {fisa['tip']:11} {fisa['sha256']}")


if __name__ == "__main__":
    main()