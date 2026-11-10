"""Verificarea pasilor A1-B2 din fisa. Rulare: python -m arsenal.windows.pasi A1"""
import sys
from arsenal.windows.inventar import (Proces, Eveniment, Inventar,
                                      procese_din_json)

START = "arsenal/windows/start/procese.json"
pas = sys.argv[1] if len(sys.argv) > 1 else "A1"

p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")

if pas == "A1":
    print(p.pid, p.nume)
    print(p)

elif pas == "A2":
    print(p.e_suspect())

elif pas == "A3":
    e1 = Eveniment(4625, "warning", "Security", "administrator", "An account failed to log on")
    e2 = Eveniment(4624, "info", "Security", "ana", "An account was successfully logged on")
    print(e1.id, e1.e_suspect())
    print(e2.id, e2.e_suspect())

elif pas == "A4":
    procese = procese_din_json(START)
    print("procese:", len(procese))
    print("suspecte:", sum(1 for p in procese if p.e_suspect()))

elif pas == "B1":
    inv = Inventar.din_json(START)
    print("procese:", len(inv))

elif pas == "B2":
    inv = Inventar.din_json(START)
    for p in inv.suspecte():
        print(f"  [{p.pid}] {p.nume}  {p.cale}")
    print(inv.pe_user())