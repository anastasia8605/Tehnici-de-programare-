import re
import json
import socket
import ssl
import time
from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin

import requests

TIMEOUT = 10

DEFAULT_HEADERS = {"User-Agent": "WebLab-CormanAnastasia"}

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Descarcă adresa url (cu DEFAULT_HEADERS) și returnează obiectul răspuns."""
    return requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS)


def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    return fetch(url).status_code


def get_title(html: str) -> str:
    """Extrage titlul dintre <title> și </title> dintr-un șir HTML."""
    start = html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = html.find("</title>", start)
    return html[start:end].strip()


def security_headers(url: str) -> dict:
    """Returnează {antet: True/False} pentru cele cinci antete de securitate."""
    response = fetch(url)
    return {h: h in response.headers for h in SECURITY_HEADERS}


def score_headers(results: dict) -> str:
    """Returnează scorul antetelor de securitate sub forma "3/5"."""
    return f"{sum(results.values())}/{len(results)}"


def check_paths(base: str, paths: list) -> dict:
    """Returnează {cale: cod de stare} pentru fiecare cale, cu pauză între cereri."""
    rezultat = {}
    for path in paths:
        rezultat[path] = get_status(base.rstrip("/") + path)
        time.sleep(1)
    return rezultat


def fetch_robots(base: str):
    """Returnează textul fișierului /robots.txt sau None dacă lipsește."""
    try:
        response = fetch(base.rstrip("/") + "/robots.txt")
    except requests.RequestException:
        return None
    return response.text if response.status_code == 200 else None


def disallowed_paths(robots_text) -> list:
    """Returnează lista valorilor Disallow: (listă goală pentru None)."""
    if robots_text is None:
        return []
    cai = []
    for linie in robots_text.splitlines():
        if linie.strip().lower().startswith("disallow:"):
            valoare = linie.split(":", 1)[1].strip()
            if valoare:
                cai.append(valoare)
    return list(dict.fromkeys(cai))


def extract_links(html: str) -> list:
    """Returnează valorile href din html, fără duplicate."""
    return list(dict.fromkeys(re.findall(r'href="([^"]+)"', html)))


def split_links(links: list, base: str) -> tuple:
    """Împarte legăturile în (interne, externe) față de domeniul lui base."""
    domain = urlparse(base).netloc
    interne, externe = [], []
    for link in links:
        complet = urljoin(base.rstrip("/") + "/", link)
        netloc = urlparse(complet).netloc
        if netloc == domain or netloc.endswith("." + domain):
            interne.append(complet)
        else:
            externe.append(complet)
    return interne, externe


def resolve(hostname: str) -> str:
    """Returnează adresa IP a domeniului hostname."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Returnează câte zile mai sunt până la expirarea certificatului TLS."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
    expira = ssl.cert_time_to_seconds(cert["notAfter"])
    return int((expira - datetime.now(timezone.utc).timestamp()) // 86400)


def redirect_chain(hostname: str) -> list:
    """Returnează lanțul de redirecționări pornind de la http://hostname."""
    response = fetch("http://" + hostname)
    return [f"{r.status_code} -> {r.headers.get('Location', r.url)}" for r in response.history]


def site_report(url: str, filename: str = "report.json") -> dict:
    """Exercițiul 50. Colectează informațiile despre site, le afișează și le salvează în JSON."""
    hostname = urlparse(url).netloc
    response = fetch(url)
    time.sleep(1)
    links = extract_links(response.text)
    interne, externe = split_links(links, url)
    lant = redirect_chain(hostname)
    time.sleep(1)
    scor = score_headers(security_headers(url))
    time.sleep(1)
    interzise = disallowed_paths(fetch_robots(url))

    raport = {
        "url": url,
        "status": response.status_code,
        "final_url": response.url,
        "title": get_title(response.text),
        "ip": resolve(hostname),
        "redirects": lant,
        "security_score": scor,
        "cert_days_left": cert_days_left(hostname),
        "internal_links": len(interne),
        "external_links": len(externe),
        "disallowed": interzise,
    }

    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare:      {raport['status']} ({raport['final_url']})")
    print(f"Titlu:             {raport['title']}")
    print(f"Adresă IP:         {raport['ip']}")
    print(f"Redirecționări:    {', '.join(lant) if lant else 'niciuna'}")
    print(f"Scor securitate:   {scor}")
    print(f"Certificat:        {raport['cert_days_left']} de zile rămase")
    print(f"Legături:          {len(interne)} interne, {len(externe)} externe")
    print(f"Căi interzise:     {', '.join(interzise) if interzise else 'niciuna'}")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print(f"Salvat în {filename}")
    return raport


if __name__ == "__main__":
    print("=== Exercițiul 46. Blocul main ===")
    print("Autotest:", get_status("https://cybercor.org"))