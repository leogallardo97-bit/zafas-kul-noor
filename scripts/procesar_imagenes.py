# -----------------------------------------------------------------------------
# ¡COME! (كُلْ · Kul) · Posproceso de imágenes de la propuesta
# Autoría: Restaurante Noor · Dirección y supervisión: Paco Morales y Paola Gualandi
# -----------------------------------------------------------------------------
# Recorta, redimensiona y guarda en JPEG o WebP con los metadatos de autoría
# (EXIF y XMP en UTF-8). Los originales no se tocan.
#
#   python scripts/procesar_imagenes.py og      <entrada> assets/img/og-kul.jpg      "descripción" [--sintesis]
#   python scripts/procesar_imagenes.py plato   <entrada> assets/img/plato-qar.webp  "descripción"
#   python scripts/procesar_imagenes.py esmalte <entrada> assets/img/zafa-esmalte.webp "descripción"
#   python scripts/procesar_imagenes.py ver     <imagen>
#
# og:      1200 × 630, recorte centrado (imagen para compartir el enlace).
#          Con --sintesis añade el aviso de imagen generada; sin él, es una captura de la web.
# plato:   cuadrado centrado de 1024 px (superficie del guiso, de borde a borde).
# esmalte: cuadrado centrado de 1024 px (zafa vacía vista desde arriba).
# plato y esmalte llevan siempre el aviso de imagen de síntesis.
# -----------------------------------------------------------------------------
import io
import sys
from xml.sax.saxutils import escape

from PIL import Image, ImageOps

AUTORIA = "Autoría: Restaurante Noor · Dirección y supervisión: Paco Morales y Paola Gualandi"
AVISO = "Recreación visual de la propuesta (imagen de síntesis)"


def xmp(descripcion):
    d, a = escape(descripcion), escape(AUTORIA)
    return (
        '<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>'
        '<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
        '<rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/">'
        '<dc:creator><rdf:Seq><rdf:li>Restaurante Noor</rdf:li></rdf:Seq></dc:creator>'
        f'<dc:rights><rdf:Alt><rdf:li xml:lang="x-default">{a}</rdf:li></rdf:Alt></dc:rights>'
        f'<dc:description><rdf:Alt><rdf:li xml:lang="x-default">{d}</rdf:li></rdf:Alt></dc:description>'
        '</rdf:Description></rdf:RDF></x:xmpmeta><?xpacket end="w"?>'
    ).encode("utf-8")


def exif(descripcion):
    e = Image.Exif()
    e[0x013B] = "Restaurante Noor"                 # Artist
    e[0x8298] = AUTORIA.encode("utf-8")            # Copyright
    e[0x010E] = descripcion.encode("utf-8")        # ImageDescription
    return e.tobytes()


def guardar(img, destino, descripcion, sintesis):
    if sintesis and AVISO not in descripcion:
        descripcion = f"{descripcion} · {AVISO}"
    img = img.convert("RGB")
    opts = {"exif": exif(descripcion), "xmp": xmp(descripcion)}
    if destino.lower().endswith(".webp"):
        img.save(destino, "WEBP", quality=82, method=6, **opts)
    else:
        img.save(destino, "JPEG", quality=86, optimize=True, progressive=True, **opts)


def cuadrado(img, lado):
    return ImageOps.fit(img, (lado, lado), Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def ver(ruta):
    img = Image.open(ruta)
    print(ruta, img.format, img.size)
    e = img.getexif()
    for tag, nombre in ((0x013B, "Artist"), (0x8298, "Copyright"), (0x010E, "ImageDescription")):
        v = e.get(tag)
        if isinstance(v, str):  # Pillow descodifica EXIF como Latin-1; se guardó en UTF-8
            v = v.encode("latin-1", "ignore")
        if isinstance(v, bytes):
            v = v.decode("utf-8", "replace")
        print(f"  {nombre}: {v}")
    x = img.info.get("xmp")
    if isinstance(x, bytes):
        x = x.decode("utf-8", "replace")
    print("  XMP con autoría:", bool(x and "Restaurante Noor" in x))


def main(argv):
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    modo = argv[1]
    if modo == "ver":
        ver(argv[2]); return
    origen, destino, descripcion = argv[2], argv[3], argv[4]
    img = Image.open(origen)
    if modo == "og":
        img = ImageOps.fit(img, (1200, 630), Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        sintesis = "--sintesis" in argv
    elif modo in ("plato", "esmalte"):
        img = cuadrado(img, 1024)
        sintesis = True
    else:
        raise SystemExit(f"Modo desconocido: {modo}")
    guardar(img, destino, descripcion, sintesis)
    ver(destino)


if __name__ == "__main__":
    main(sys.argv)
