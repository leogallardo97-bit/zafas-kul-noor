# -----------------------------------------------------------------------------
# ¡COME! (كُلْ · Kul) · Bibliometría de los ingredientes de vanguardia (Scopus)
# Autoría: Restaurante Noor · Dirección y supervisión: Paco Morales y Paola Gualandi
# -----------------------------------------------------------------------------
# Repite en Scopus (TITLE-ABS-KEY) las mismas ecuaciones del script de OpenAlex,
# para contrastar los dos recuentos. Necesita una clave de la API de Elsevier y,
# fuera de la red de la universidad, un token institucional:
#   setx SCOPUS_API_KEY "..."      (y, si la biblioteca lo facilita)
#   setx SCOPUS_INSTTOKEN "..."
# Tras crear las variables hay que reiniciar VS Code. Las condiciones de uso de
# Elsevier están pensadas para investigación: conviene citar los recuentos como
# resultado de búsqueda y no redistribuir los registros de Scopus.
#
# Uso:  python scripts/bibliometria_ingredientes_scopus.py
# Salida: bibliometria_ingredientes_scopus.csv (UTF-8 con BOM, para Excel)
# -----------------------------------------------------------------------------
import csv
import datetime
import io
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import bibliometria_ingredientes_openalex as oa  # noqa: E402  (mismas ecuaciones)

API = "https://api.elsevier.com/content/search/scopus"
OUT = pathlib.Path(__file__).resolve().parent.parent / "bibliometria_ingredientes_scopus.csv"
PERIODOS = {
    "2016_2020": "PUBYEAR > 2015 AND PUBYEAR < 2021",
    "2021_2025": "PUBYEAR > 2020 AND PUBYEAR < 2026",
    "2026_parcial": "PUBYEAR = 2026",
}


class SinAcceso(Exception):
    pass


def total(query):
    key = os.environ.get("SCOPUS_API_KEY") or os.environ.get("ELSEVIER_API_KEY")
    if not key:
        raise SinAcceso("no hay SCOPUS_API_KEY en el entorno")
    url = API + "?" + urllib.parse.urlencode({"query": query, "count": 1, "field": "dc:identifier"})
    req = urllib.request.Request(url, headers={"X-ELS-APIKey": key, "Accept": "application/json"})
    token = os.environ.get("SCOPUS_INSTTOKEN") or os.environ.get("ELSEVIER_INSTTOKEN")
    if token:
        req.add_header("X-ELS-Insttoken", token)
    wait = 2.0
    for _ in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return int(json.load(r)["search-results"]["opensearch:totalResults"])
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise SinAcceso(f"HTTP {e.code}: clave no válida o sin derechos desde esta red")
            if e.code != 429:
                raise
        except urllib.error.URLError:
            pass
        time.sleep(wait)
        wait *= 2
    raise SinAcceso("Scopus no responde o cuota agotada")


def main():
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    hoy = datetime.date.today().isoformat()
    filas = []
    for rol, ilus, nombre, q_food, q_hist in oa.CANDIDATOS:
        food = f"TITLE-ABS-KEY(({q_food}) AND {oa.FOOD})"
        hist = f"TITLE-ABS-KEY({oa.ANDALUS} AND {q_hist})"
        counts: dict[str, int] = {}
        for k, filtro in PERIODOS.items():
            counts[k] = total(f"{food} AND {filtro}"); time.sleep(0.2)
        nh = total(hist); time.sleep(0.2)
        n1, n2 = counts["2016_2020"], counts["2021_2025"]
        crec = round(n2 / n1, 2) if n1 else ""
        filas.append({
            "rol": rol, "ilustracion": ilus, "ingrediente": nombre,
            "n_alimentos_2016_2020": n1, "n_alimentos_2021_2025": n2,
            "crecimiento": crec, "n_alimentos_2026_parcial": counts["2026_parcial"],
            "n_enfoque_andalusi": nh,
            "consulta_alimentos": food, "consulta_andalusi": hist,
            "fecha_consulta": hoy, "fuente": "Scopus Search API (Elsevier)",
        })
        print(f"{nombre:48s} {n1:>5} {n2:>5} x{crec!s:<5} andalusí:{nh:>3}")
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print("Escrito:", OUT)


if __name__ == "__main__":
    try:
        main()
    except SinAcceso as e:
        print("Sin acceso a Scopus:", e)
        sys.exit(2)
