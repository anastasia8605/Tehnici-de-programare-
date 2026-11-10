import argparse
import csv
import time
from datetime import datetime

import webtools
from webtools import get_title, security_headers
from webtools import DEFAULT_HEADERS


def write_csv(results: dict, filename: str = "report.csv") -> None:
    """Exercițiul 49. Salvează rezultatul check_paths() în CSV (path, status, checked_at)."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "status", "checked_at"])
        for path, status in results.items():
            writer.writerow([path, status, datetime.now().isoformat()])
    print(f"Salvat în {filename}")


def main():
    """Exercițiul 48. Citește URL-ul din linia de comandă și rulează toate verificările."""
    parser = argparse.ArgumentParser(description="Raport despre un site web")
    parser.add_argument("url", help="adresa site-ului, ex. https://cybercor.org")
    args = parser.parse_args()
    url = args.url

    print("=== Exercițiul 44. Crearea unui modul ===")
    print("Titlu (import webtools):", webtools.get_title(webtools.fetch(url).text))
    time.sleep(1)

    print("\n=== Exercițiul 45. Importarea anumitor nume ===")
    print("Titlu (from webtools import):", get_title(webtools.fetch(url).text))
    time.sleep(1)
    print("Antete de securitate:", security_headers(url))
    time.sleep(1)

    print("\n=== Exercițiul 47. Constante de modul ===")
    print("DEFAULT_HEADERS:", DEFAULT_HEADERS)

    print("\n=== Exercițiul 49. Un raport CSV ===")
    rezultate = webtools.check_paths(url, ["/", "/robots.txt", "/sitemap.xml"])
    print(rezultate)
    write_csv(rezultate)

    print("\n=== Exercițiul 50. Proiect final ===")
    webtools.site_report(url)


if __name__ == "__main__":
    main()