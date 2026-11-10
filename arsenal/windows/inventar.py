"""Inventar de procese si jurnal de evenimente Windows, modelate ca obiecte."""
from dataclasses import dataclass, asdict
import json

# Cai din folderul utilizatorului: semn clasic de malware
CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")

# 4625 logon esuat, 1102 jurnal sters, 7045 serviciu instalat
SUSPECTE_ID = {4625, 1102, 7045}


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        """True daca procesul ruleaza din Temp sau Roaming."""
        return any(c in self.cale for c in CAI_SUSPECTE)


@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        """True daca ID-ul e cunoscut ca periculos sau nivelul e critical."""
        return self.id in SUSPECTE_ID or self.nivel == "critical"


def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]


def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]


@dataclass
class Inventar:
    procese: list

    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])

    def __len__(self):
        return len(self.procese)

    def suspecte(self):
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self):
        grupe = {}
        for p in self.procese:
            grupe.setdefault(p.user, []).append(p.nume)
        return grupe


def main():
    import argparse
    p = argparse.ArgumentParser(description="Raport de alarme: procese si evenimente Windows")
    p.add_argument("capturi", help="folderul cu procese.json si evenimente.json")
    p.add_argument("--json", action="store_true", help="iesire in format JSON")
    a = p.parse_args()

    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")
    suspecte = inv.suspecte()
    alarma = [e for e in ev if e.e_suspect()]

    if a.json:
        raport = {
            "procese_suspecte": [asdict(s) for s in suspecte],
            "evenimente_alarma": [asdict(e) for e in alarma],
        }
        print(json.dumps(raport, indent=2, ensure_ascii=False))
    else:
        print(f"Procese: {len(inv)} | suspecte: {len(suspecte)}")
        for s in suspecte:
            print(f"  [{s.pid}] {s.nume}  ({s.user})  {s.cale}")
        print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")
        for e in alarma:
            print(f"  {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")


if __name__ == "__main__":
    main()