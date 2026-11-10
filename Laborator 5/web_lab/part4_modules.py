BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10
HEADERS = {"User-Agent": "WebLab-CormanAnastasia"}

import time
import re
import json
import socket
import ssl
import hashlib
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

import requests


def parse_url(url):
    """Descompune url și afișează schema, domeniul, calea, interogarea și fragmentul."""
    p = urlparse(url)
    print("scheme:  ", p.scheme)
    print("netloc:  ", p.netloc)
    print("path:    ", p.path)
    print("query:   ", p.query)
    print("fragment:", p.fragment)
    return p


print("=== Exercițiul 35. Descompunerea unui URL ===")
parse_url("https://cybercor.org/path?x=1#top")


def full_urls(base, relative_links):
    """Transformă legăturile relative în URL-uri complete pornind de la base."""
    return [urljoin(base + "/", link) for link in relative_links]


print("\n=== Exercițiul 36. Compunerea URL-urilor ===")
for rel, full in zip(["/about", "contact.html", "../index.html"],
                     full_urls(BASE_URL, ["/about", "contact.html", "../index.html"])):
    print(f"{rel:15} -> {full}")


def extract_links(html):
    """Returnează toate valorile href din html, fără duplicate, în ordinea apariției."""
    links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(links))


print("\n=== Exercițiul 37. Extragerea legăturilor ===")
response = requests.get(BASE_URL, timeout=TIMEOUT, headers=HEADERS)
links = extract_links(response.text)
print("Legături unice găsite:", len(links))
for link in links[:10]:
    print(" ", link)
if len(links) > 10:
    print("  ...")


def split_links(links, domain):
    """Împarte legăturile în (interne, externe) după domeniul lor."""
    interne, externe = [], []
    for link in links:
        complet = urljoin(BASE_URL + "/", link)
        netloc = urlparse(complet).netloc
        if netloc == domain or netloc.endswith("." + domain):
            interne.append(complet)
        else:
            externe.append(complet)
    return interne, externe


print("\n=== Exercițiul 38. Interne sau externe? ===")
interne, externe = split_links(links, "cybercor.org")
print("Interne:", len(interne))
print("Externe:", len(externe))
for e in externe[:5]:
    print("  extern:", e)

print("\n=== Exercițiul 39. Propriile metode ===")


class ImageFinder(HTMLParser):
    """Parser HTML care colectează atributul src al fiecărui tag <img>."""

    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Apelată automat de feed() pentru fiecare tag de deschidere."""
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)


test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)
print(finder.images)

assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp",
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut!")

time.sleep(1)
response = requests.get(BASE_URL, timeout=TIMEOUT, headers=HEADERS)
finder = ImageFinder()
finder.feed(response.text)
print(len(finder.images), "imagini găsite")
for src in finder.images:
    print(src)
print("Verificare cu count('<img'):", response.text.lower().count("<img"))


def page_fingerprint(url):
    """Returnează amprenta SHA-256 a conținutului paginii url."""
    response = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
    return hashlib.sha256(response.content).hexdigest()


print("\n=== Exercițiul 40. Amprenta paginii ===")
time.sleep(1)
h1 = page_fingerprint(BASE_URL)
time.sleep(1)
h2 = page_fingerprint(BASE_URL)
print("Prima amprentă: ", h1)
print("A doua amprentă:", h2)
print("Identice:", h1 == h2)


def save_headers(url, filename="headers.json"):
    """Salvează antetele răspunsului de la url în fișierul JSON filename."""
    response = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dict(response.headers), f, indent=2)
    return filename


def load_headers(filename="headers.json"):
    """Încarcă antetele din fișierul JSON filename și le returnează ca dicționar."""
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


print("\n=== Exercițiul 41. Salvarea în JSON ===")
time.sleep(1)
fisier = save_headers(BASE_URL)
incarcate = load_headers(fisier)
print("Salvat în", fisier)
print("Content-Type din fișier:", incarcate.get("Content-Type", "lipsește"))


def resolve(hostname):
    """Returnează adresa IP a domeniului hostname (interogare DNS)."""
    return socket.gethostbyname(hostname)


print("\n=== Exercițiul 42. Interogare DNS ===")
print("cybercor.org ->", resolve("cybercor.org"))


def cert_days_left(hostname):
    """Returnează numărul de zile rămase până la expirarea certificatului TLS."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
    expira = ssl.cert_time_to_seconds(cert["notAfter"])
    acum = datetime.now(timezone.utc).timestamp()
    return int((expira - acum) // 86400)


print("\n=== Exercițiul 43. Expirarea certificatului ===")
print("Zile rămase:", cert_days_left("cybercor.org"))