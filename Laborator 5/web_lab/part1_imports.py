BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10
HEADERS = {"User-Agent": "WebLab-CormanAnastasia"}

import time
import pydoc

print("=== Exercițiul 1. Primul import ===")
import requests
print("Versiunea requests:", requests.__version__)

import urllib.request
print("Modulul urllib.request a fost importat:", urllib.request.__name__)

print("\n=== Exercițiul 2. Două stiluri de import ===")
r = requests.get(BASE_URL, timeout=TIMEOUT, headers=HEADERS)
print("import requests       -> cod de stare:", r.status_code)
time.sleep(1)

from requests import get
r = get(BASE_URL, timeout=TIMEOUT, headers=HEADERS)
print("from requests import get -> cod de stare:", r.status_code)

print("\n=== Exercițiul 3. Alias-uri ===")
import requests as rq
time.sleep(1)
r = rq.get(BASE_URL, timeout=TIMEOUT, headers=HEADERS)
print("rq.get -> cod de stare:", r.status_code)

print("\n=== Exercițiul 4. Doar biblioteca standard ===")
time.sleep(1)
cerere = urllib.request.Request(BASE_URL, headers=HEADERS)
with urllib.request.urlopen(cerere, timeout=TIMEOUT) as raspuns:
    print("Status:", raspuns.status)
    corp = raspuns.read().decode("utf-8")
    print("Primele 200 de caractere:")
    print(corp[:200])

print("\n=== Exercițiul 5. Priviți în interiorul unui modul ===")
print(dir(requests))

print("\n=== Exercițiul 6. Citiți documentația ===")
print(pydoc.render_doc(requests.get, renderer=pydoc.plaintext))
time.sleep(1)
r = requests.get(BASE_URL, timeout=5, headers=HEADERS)
print("Cerere cu timeout=5 -> cod de stare:", r.status_code)

print("\n=== Exercițiul 7. Cronometrarea unei cereri ===")
time.sleep(1)
start = time.perf_counter()
r = requests.get(BASE_URL, timeout=TIMEOUT, headers=HEADERS)
durata = time.perf_counter() - start
print(f"time.perf_counter(): {durata:.3f} s")
print(f"response.elapsed:    {r.elapsed.total_seconds():.3f} s")

print("\n=== Exercițiul 8. Când un import eșuează ===")
try:
    import bs4
    print("Modulul bs4 este instalat, versiunea", bs4.__version__)
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")