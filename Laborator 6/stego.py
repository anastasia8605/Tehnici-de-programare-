from PIL import Image

mesaj = b"FLAG{ascuns_in_pixeli}"

img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())

# transform mesajul in biti, plus un octet 0 la final (marcheaza sfarsitul)
biti = "".join(f"{x:08b}" for x in mesaj) + "00000000"

px_nou = []
idx = 0
for (r, g, b) in px:
    canale = [r, g, b]
    for i in range(3):
        if idx < len(biti):
            canale[i] = (canale[i] & ~1) | int(biti[idx])
            idx += 1
    px_nou.append(tuple(canale))

img.putdata(px_nou)
img.save("stego.png")
print("Mesaj ascuns in stego.png")
print("Biti scrisi:", len(biti))

print("--- B6: dezvaluire mesaj din stego.png ---")
px = list(Image.open("stego.png").convert("RGB").getdata())

biti = ""
for (r, g, b) in px:
    biti += str(r & 1)
    biti += str(g & 1)
    biti += str(b & 1)

mesaj_iesit = bytearray()
for i in range(0, len(biti), 8):
    octet = biti[i:i+8]
    valoare = int(octet, 2)
    if valoare == 0:
        break
    mesaj_iesit.append(valoare)

print("Mesaj dezvaluit:", mesaj_iesit.decode())