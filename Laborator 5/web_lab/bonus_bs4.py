from bs4 import BeautifulSoup

import webtools

URL = "https://cybercor.org"


def get_title_bs4(html: str) -> str:
    """Returnează titlul paginii folosind BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.get_text(strip=True) if soup.title else ""


def extract_links_bs4(html: str) -> list:
    """Returnează toate legăturile href, fără duplicate, folosind BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")
    return list(dict.fromkeys(a["href"] for a in soup.find_all("a", href=True)))


if __name__ == "__main__":
    html = webtools.fetch(URL).text

    print("=== Exercițiu bonus. Titlul paginii ===")
    print("Varianta cu .find():       ", webtools.get_title(html))
    print("Varianta cu BeautifulSoup: ", get_title_bs4(html))

    print("\n=== Exercițiu bonus. Legăturile ===")
    print("Varianta cu re.findall():  ", len(webtools.extract_links(html)), "legături")
    print("Varianta cu BeautifulSoup: ", len(extract_links_bs4(html)), "legături")