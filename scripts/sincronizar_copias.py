# -----------------------------------------------------------------------------
# ¡COME! (كُلْ · Kul) · Copias de la presentación en las carpetas de entrega
# Autoría: Restaurante Noor · Dirección y supervisión: Paco Morales y Paola Gualandi
# -----------------------------------------------------------------------------
# index.html (raíz) es la única fuente. Ejecutar después de cada cambio:
#   python scripts/sincronizar_copias.py
#
# 02_Propuesta_Noor_Zafas_Kul/index.html
#     Copia de respaldo: mismas rutas, un nivel más abajo (../assets/).
# 02_Propuesta_Noor_Kul/Kul_Noor_presentacion.html
#     Copia autónoma para abrir con doble clic, sin conexión o enviada suelta:
#     tipografías, favicon e imágenes de assets/ van incrustadas en el archivo.
# -----------------------------------------------------------------------------
import base64
import io
import mimetypes
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "index.html"
RESPALDO = RAIZ / "02_Propuesta_Noor_Zafas_Kul" / "index.html"
AUTONOMA = RAIZ / "02_Propuesta_Noor_Kul" / "Kul_Noor_presentacion.html"
RUTA = re.compile(r'(\b(?:href|src|data-photo|data-glaze)=")assets/')
FONTS_LINK = '<link rel="stylesheet" href="assets/fonts/fonts.css">'


def data_uri(ruta):
    tipo = mimetypes.guess_type(ruta.name)[0] or "application/octet-stream"
    if ruta.suffix == ".woff2":
        tipo = "font/woff2"
    return f"data:{tipo};base64," + base64.b64encode(ruta.read_bytes()).decode("ascii")


def autonoma(html):
    css = (RAIZ / "assets" / "fonts" / "fonts.css").read_text(encoding="utf-8")
    # el subconjunto vietnamita no hace falta para los textos de la presentación
    css = re.sub(r"/\* vietnamese \*/\s*@font-face \{.*?\}\s*", "", css, flags=re.S)
    css = re.sub(r'url\("([^"]+\.woff2)"\)',
                 lambda m: f'url("{data_uri(RAIZ / "assets" / "fonts" / m.group(1))}")', css)
    if FONTS_LINK not in html:
        raise SystemExit("No encuentro el enlace a assets/fonts/fonts.css en index.html")
    html = re.sub(r'\s*<link rel="preload"[^>]*>', "", html)
    html = html.replace(FONTS_LINK, "<style>\n" + css + "</style>")
    return re.sub(r'(\b(?:href|src|data-photo|data-glaze)=")(assets/[^"]+)"',
                  lambda m: f'{m.group(1)}{data_uri(RAIZ / m.group(2))}"', html)


def main():
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    html = FUENTE.read_text(encoding="utf-8")
    respaldo, n = RUTA.subn(r"\1../assets/", html)
    RESPALDO.write_text(respaldo, encoding="utf-8")
    print(f"{RESPALDO.relative_to(RAIZ)}: {n} rutas reescritas")
    AUTONOMA.write_text(autonoma(html), encoding="utf-8")
    print(f"{AUTONOMA.relative_to(RAIZ)}: autónoma, {AUTONOMA.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
