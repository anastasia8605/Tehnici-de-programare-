BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10
HEADERS = {"User-Agent": "WebLab-CormanAnastasia"}

import time
import pydoc
import requests


def fetch(url):
    """Descarcă adresa url și returnează obiectul răspuns."""
    return requests.get(url, timeout=TIMEOUT, headers=HEADERS)


print("=== Exercițiul 21. Prima funcție ===")
print("Cod de stare:", fetch(BASE_URL).status_code)


def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
    return response.status_code


print("\n=== Exercițiul 22. Returnarea unei singure valori ===")
for cale in ["/", "/robots.txt", "/sitemap.xml"]:
    time.sleep(1)
    print(cale, "->", get_status(BASE_URL + cale))


def fetch(url: str, timeout: int = 10) -> requests.Response:
    """Descarcă adresa url (timeout implicit 10 s) și returnează răspunsul."""
    return requests.get(url, timeout=timeout, headers=HEADERS)


print("\n=== Exercițiul 23. Parametri impliciți ===")
time.sleep(1)
print("Cu timeout implicit (10):", fetch(BASE_URL).status_code)
time.sleep(1)
print("Cu timeout=3:", fetch(BASE_URL, timeout=3).status_code)


def get_title(html: str) -> str:
    """Extrage titlul paginii dintr-un șir HTML.

    Caută textul dintre <title> și </title> și îl returnează curățat
    de spații. Funcția nu face nicio cerere în rețea: primește HTML-ul
    deja descărcat. Dacă nu există titlu, returnează un șir gol.
    """
    start = html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = html.find("</title>", start)
    return html[start:end].strip()


print("\n=== Exercițiul 24. O singură sarcină pe funcție ===")
time.sleep(1)
pagina = fetch(BASE_URL)
print("Titlu:", get_title(pagina.text))

print("\n=== Exercițiul 25. Docstring-uri ===")
print(pydoc.render_doc(get_title, renderer=pydoc.plaintext))

print("\n=== Exercițiul 26. Adnotări de tip ===")
try:
    get_status(123)
except Exception as e:
    print("get_status(123) a dat eroare:", type(e).__name__, "-", e)


def page_exists(url: str) -> bool:
    """Returnează True dacă pagina răspunde cu succes, altfel False (fără erori)."""
    try:
        response = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
        return response.ok
    except requests.RequestException:
        return False


print("\n=== Exercițiul 27. Fără opriri neașteptate ===")
time.sleep(1)
print(BASE_URL, "->", page_exists(BASE_URL))
print("https://this-domain-does-not-exist.invalid ->",
      page_exists("https://this-domain-does-not-exist.invalid"))


def check_paths(base: str, paths: list) -> dict:
    """Returnează un dicționar {cale: cod de stare} pentru fiecare cale din paths."""
    rezultat = {}
    for path in paths:
        rezultat[path] = get_status(base + path)
        time.sleep(1)
    return rezultat


print("\n=== Exercițiul 28. Returnarea unui dicționar ===")
print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))


def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Returnează valoarea antetului name al adresei url sau default dacă lipsește."""
    response = requests.head(url, timeout=TIMEOUT, headers=HEADERS)
    return response.headers.get(name, default)


print("\n=== Exercițiul 29. Argumente cu nume ===")
print("Server:", get_header(BASE_URL, name="Server"))
time.sleep(1)
print("X-Inexistent:", get_header(BASE_URL, name="X-Inexistent", default="nu există"))

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


def security_headers(url: str) -> dict:
    """Returnează {antet: True/False} pentru cele cinci antete de securitate."""
    response = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
    return {h: h in response.headers for h in SECURITY_HEADERS}


print("\n=== Exercițiul 30. Antete de securitate ===")
time.sleep(1)
rezultate = security_headers(BASE_URL)
for antet, prezent in rezultate.items():
    print(f"{antet}: {prezent}")


def score_headers(results: dict) -> str:
    """Primește rezultatul lui security_headers și returnează scorul, ex. "3/5"."""
    return f"{sum(results.values())}/{len(results)}"


print("\n=== Exercițiul 31. Funcții care apelează funcții ===")
time.sleep(1)
print("Scor securitate:", score_headers(security_headers(BASE_URL)))


def fetch_robots(base: str):
    """Returnează textul fișierului /robots.txt sau None dacă lipsește."""
    try:
        response = requests.get(base + "/robots.txt", timeout=TIMEOUT, headers=HEADERS)
    except requests.RequestException:
        return None
    if response.status_code != 200:
        return None
    return response.text


def disallowed_paths(robots_text) -> list:
    """Returnează lista valorilor Disallow: din robots.txt (listă goală pentru None)."""
    if robots_text is None:
        return []
    cai = []
    for linie in robots_text.splitlines():
        if linie.strip().lower().startswith("disallow:"):
            valoare = linie.split(":", 1)[1].strip()
            if valoare:
                cai.append(valoare)
    return list(dict.fromkeys(cai))


print("\n=== Exercițiul 32. Două funcții, o sarcină ===")
time.sleep(1)
robots = fetch_robots(BASE_URL)
print("robots.txt găsit:", robots is not None)
print("Căi interzise:", disallowed_paths(robots))
print("Pentru None:", disallowed_paths(None))


def response_times(*urls) -> dict:
    """Returnează {url: secunde} cu durata cererii pentru fiecare url primit."""
    timpi = {}
    for url in urls:
        start = time.perf_counter()
        requests.get(url, timeout=TIMEOUT, headers=HEADERS)
        timpi[url] = round(time.perf_counter() - start, 3)
        time.sleep(1)
    return timpi


print("\n=== Exercițiul 33. Oricâte argumente ===")
print(response_times(BASE_URL, BASE_URL + "/robots.txt"))


def log(message: str, **details) -> None:
    """Afișează mesajul urmat de fiecare detaliu, în forma cheie=valoare."""
    parti = [message] + [f"{k}={v}" for k, v in details.items()]
    print(" | ".join(parti))


print("\n=== Exercițiul 34. Argumente cu nume colectate ===")
log("verificat", url=BASE_URL, status=200)