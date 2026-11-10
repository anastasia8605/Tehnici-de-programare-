BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10
HEADERS = {"User-Agent": "WebLab-CormanAnastasia"}

import time
import requests

response = requests.get(BASE_URL, timeout=TIMEOUT, headers=HEADERS)

print("=== Exercițiul 9. Elementele de bază ale răspunsului ===")
print("status_code:", response.status_code)
print("ok:", response.ok)
print("url:", response.url)
print("encoding:", response.encoding)

print("\n=== Exercițiul 10. Tratarea erorilor cu o metodă ===")
response.raise_for_status()
print("Pagina principală: nicio eroare.")
time.sleep(1)
try:
    r404 = requests.get(BASE_URL + "/this-page-does-not-exist",
                        timeout=TIMEOUT, headers=HEADERS)
    r404.raise_for_status()
except requests.HTTPError as e:
    print("Pagina nu a fost găsită, dar programul continuă.")
    print("Detalii:", e)

print("\n=== Exercițiul 11. Toate antetele ===")
for nume, valoare in response.headers.items():
    print(f"{nume}: {valoare}")

print("\n=== Exercițiul 12. Metode de dicționar ===")
print("Server:", response.headers.get("Server", "lipsește"))
print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
print("content-type:", response.headers.get("content-type", "lipsește"))

print("\n=== Exercițiul 13. Înlănțuirea metodelor de șir ===")
nr = response.text.lower().count("cyber")
print("Cuvântul 'cyber' apare de", nr, "ori")

print("\n=== Exercițiul 14. Găsirea titlului ===")
html = response.text
start = html.find("<title>") + len("<title>")
end = html.find("</title>", start)
titlu = html[start:end].strip()
print("Titlul paginii:", titlu)

print("\n=== Exercițiul 15. Numărarea liniilor ===")
lines = html.splitlines()
print("Număr de linii:", len(lines))
print("Cea mai lungă linie are", len(max(lines, key=len)), "caractere")

print("\n=== Exercițiul 16. Verificarea HTTPS ===")
if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")

print("\n=== Exercițiul 17. Urmărirea redirecționărilor ===")
time.sleep(1)
r = requests.get("http://cybercor.org", timeout=TIMEOUT, headers=HEADERS)
if not r.history:
    print("Nicio redirecționare.")
for pas in r.history:
    print(pas.status_code, "->", pas.url)
print("URL final:", r.url)

print("\n=== Exercițiul 18. HEAD versus GET ===")
time.sleep(1)
r_head = requests.head(BASE_URL, timeout=TIMEOUT, headers=HEADERS)
time.sleep(1)
r_get = requests.get(BASE_URL, timeout=TIMEOUT, headers=HEADERS)
print("HEAD -> len(content):", len(r_head.content))
print("GET  -> len(content):", len(r_get.content))

print("\n=== Exercițiul 19. Cookie-uri ===")
if len(response.cookies) == 0:
    print("Niciun cookie setat")
for cookie in response.cookies:
    print(cookie.name, "secure =", cookie.secure)

print("\n=== Exercițiul 20. Sesiuni ===")
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-CormanAnastasia"})
time.sleep(1)
r = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
trimis = r.json()["headers"]["User-Agent"]
print("User-Agent primit de httpbin:", trimis)
print("Antetul a fost trimis:", trimis == "WebLab-CormanAnastasia")