import re
from PIL import Image
from PIL.ExifTags import TAGS


def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return "necunoscut (" + cap.hex() + ")"


print("--- B1: tipul real al fisierelor ---")
for fisier in ["probe/foto.jpg", "probe/ascuns.png", "probe/mesaj.txt", "probe/challenge.bin"]:
    print(fisier, "->", tip_real(fisier))


print("--- B2: strings din ascuns.png ---")
date = open("probe/ascuns.png", "rb").read()
for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())


print("--- B3: EXIF si GPS din foto.jpg ---")
exif = Image.open("probe/foto.jpg")._getexif() or {}
for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)

gps = exif.get(34853, {})


def la_zecimal(dms, ref):
    grade = float(dms[0])
    minute = float(dms[1])
    secunde = float(dms[2])
    val = grade + minute / 60 + secunde / 3600
    if ref in ("S", "W"):
        val = -val
    return val


if gps:
    lat = la_zecimal(gps[2], gps[1])
    lon = la_zecimal(gps[4], gps[3])
    print("Latitudine:", lat)
    print("Longitudine:", lon)

print("--- B4: file carving din ascuns.png ---")
date = open("probe/ascuns.png", "rb").read()
i = date.find(b"PK\x03\x04")
if i != -1:
    with open("gasit.zip", "wb") as f:
        f.write(date[i:])
    print("arhiva extrasa de la octetul", i)

    import zipfile
    with zipfile.ZipFile("gasit.zip") as z:
        print("fisiere in arhiva:", z.namelist())
        for nume in z.namelist():
            continut = z.read(nume)
            print(nume, "->", continut.decode())