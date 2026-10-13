import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    # lstrip("/") scoate "/" de la început, ca să nu apară "//" în adresă
    return "https://" + host.rstrip("/") + "/" + path.lstrip("/")


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        r = requests.get(url, timeout=5)
        print("Status:", r.status_code)
        print("Content-Type:", r.headers.get("Content-Type", "unknown"))
    except requests.RequestException as e:
        # nu lăsăm programul să se oprească dacă site-ul nu răspunde
        print("Eroare:", type(e).__name__)


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        r = requests.get(url, timeout=5)
    except requests.RequestException as e:
        # site inexistent, prea lent sau fără conexiune
        return {"status": None, "error": type(e).__name__}

    # păstrăm doar tipul, fără "; charset=..."
    content_type = r.headers.get("Content-Type", "unknown").split(";")[0].strip()

    return {
        "status": r.status_code,
        "content_type": content_type,
        "length": len(r.content),               # mărimea răspunsului, în octeți
        "server": r.headers.get("Server", "unknown"),
    }


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []
    for url in SITES:
        info = check_site(url)
        info["url"] = url          # adăugăm adresa, ca s-o putem afișa
        results.append(info)

    # păstrăm doar paginile cu status 200
    ok_sites = [info for info in results if info["status"] == 200]
    # cele mai mari primele
    ok_sites.sort(key=lambda info: info["length"], reverse=True)

    for info in ok_sites:
        print(info["url"], "->", info["status"], str(info["length"]) + " octeți")

    failed = len(results) - len(ok_sites)
    print("Reușite:", len(ok_sites), "| Eșuate:", failed)


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        r = requests.get(url, timeout=5)
    except requests.RequestException as e:
        return {"status": None, "error": type(e).__name__}

    present = []
    missing = []
    # parcurgem lista în ordine, ca să păstrăm ordinea din SECURITY_HEADERS
    for header in SECURITY_HEADERS:
        # r.headers nu ține cont de majuscule, deci x-frame-options se potrivește
        if header in r.headers:
            present.append(header)
        else:
            missing.append(header)

    score = len(present) * 100 // len(SECURITY_HEADERS)   # procent, număr întreg
    return {"present": present, "missing": missing, "score": score}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    status = None      # ultimul status primit
    error = None       # ultima eroare de conexiune
    used = 0           # câte cereri am trimis cu adevărat

    for _ in range(attempts):
        used += 1
        try:
            r = requests.get(url, timeout=5)
        except requests.RequestException as e:
            error = type(e).__name__
            continue                       # eșec de conexiune: încercăm din nou

        status = r.status_code
        if status < 500:
            break                          # sub 500 (inclusiv 404): ne oprim imediat

    result = {"status": status, "attempts": used}
    if status is None:
        result["error"] = error            # toate încercările au eșuat
    return result


