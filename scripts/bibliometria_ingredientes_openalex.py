# -----------------------------------------------------------------------------
# ¡COME! (كُلْ · Kul) · Bibliometría de los ingredientes de vanguardia (OpenAlex)
# Autoría: Restaurante Noor · Dirección y supervisión: Paco Morales y Paola Gualandi
# -----------------------------------------------------------------------------
# Para cada ingrediente candidato cuenta, en OpenAlex (búsqueda en título y
# resumen), dos cosas:
#   1. Ciencia de los alimentos: trabajos de 2016-2020, 2021-2025 y 2026.
#   2. Historia: trabajos con enfoque andalusí (sin límite de años).
# Los recuentos son órdenes de magnitud: la búsqueda léxica recoge ruido y
# OpenAlex cubre mal las revistas españolas de ámbito regional.
#
# OpenAlex limita las peticiones sin clave a un presupuesto diario por IP
# (unas 100 búsquedas). Con clave propia y gratuita el límite es mayor:
#   set OPENALEX_API_KEY=...   (cmd)   ·   $env:OPENALEX_API_KEY="..."  (PowerShell)
# Si se agota el presupuesto, el script guarda lo obtenido y marca el resto
# como pendiente.
#
# Uso:  python scripts/bibliometria_ingredientes_openalex.py
# Salida: bibliometria_ingredientes_openalex.csv (UTF-8 con BOM, para Excel)
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

API = "https://api.openalex.org/works"
OUT = pathlib.Path(__file__).resolve().parent.parent / "bibliometria_ingredientes_openalex.csv"

FOOD = '(food OR culinary OR gastronomy OR edible OR "functional food" OR ingredient)'
ANDALUS = '("al-Andalus" OR Andalusi OR "Islamic Iberia" OR "Muslim Spain" OR "Islamic Spain" OR andalusí)'

# rol, ilustración, ingrediente, términos (ciencia de los alimentos), términos (historia andalusí)
CANDIDATOS = [
    ("titular", "Portada · kul baqliyya", "Verdolaga (Portulaca oleracea)",
     '("Portulaca oleracea" OR purslane)', "(purslane OR verdolaga OR Portulaca)"),
    ("titular", "Pase I · berenjena", "Alcaparra (Capparis spinosa)",
     '("Capparis spinosa" OR caper OR capers)', "(caper OR capers OR alcaparra OR Capparis)"),
    ("titular", "Pase II · calabaza", "Semilla verde de cilantro (Coriandrum sativum)",
     '("Coriandrum sativum" OR coriander) AND (seed OR seeds OR fruit OR fruits)', "(coriander OR cilantro)"),
    ("titular", "Pase III · almendra", "Alloza: almendra verde (Prunus dulcis)",
     '("green almond" OR "green almonds" OR "immature almond" OR "almond hull" OR "almond hulls")', "(almond OR almendra OR almendras)"),
    ("titular", "Pase IV · azafrán", "Tépalo de la flor del azafrán (Crocus sativus)",
     '("Crocus sativus" OR saffron) AND (tepal OR tepals OR petal OR petals OR "floral by-product" OR "floral bio-residues" OR "by-products")',
     '(saffron OR azafrán OR "Crocus sativus")'),
    ("alternativa", "Portada · kul baqliyya", "Mastuerzo (Lepidium sativum)",
     '("Lepidium sativum" OR "garden cress" OR "cress seed")', "(cress OR mastuerzo OR Lepidium)"),
    ("alternativa", "Pase I · berenjena", "Almorí: murrī de cebada",
     '(murri OR almori OR budhaj OR "barley koji")', '(murri OR almorí OR almori OR "fermented sauce")'),
    ("alternativa", "Pase II · calabaza", "Polen de hinojo silvestre (Foeniculum vulgare)",
     '("Foeniculum vulgare" OR "wild fennel" OR "fennel pollen")', "(fennel OR hinojo OR Foeniculum)"),
    ("alternativa", "Pase III · almendra", "Mora negra (Morus nigra)",
     '("Morus nigra" OR "black mulberry" OR "black mulberries")', "(mulberry OR morera OR moral OR Morus)"),
    ("alternativa", "Pase IV · azafrán", "Almecina: fruto del almez (Celtis australis)",
     '("Celtis australis" OR "European hackberry" OR "nettle tree")', "(Celtis OR almez OR hackberry OR almecina)"),
]


class PresupuestoAgotado(Exception):
    pass


def count(search, years=None):
    flt = "title_and_abstract.search:" + search
    if years:
        flt += ",publication_year:" + years
    url = API + "?" + urllib.parse.urlencode({"filter": flt, "per_page": 1})
    req = urllib.request.Request(url)
    key = os.environ.get("OPENALEX_API_KEY")
    if key:
        req.add_header("Authorization", "Bearer " + key)
    wait = 2.0
    for _ in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)["meta"]["count"]
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            if int(e.headers.get("Retry-After") or 0) > 300:
                raise PresupuestoAgotado(e.headers.get("Retry-After"))
        except urllib.error.URLError:
            pass
        time.sleep(wait)
        wait *= 2
    raise PresupuestoAgotado("sin respuesta")


def main():
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    hoy = datetime.date.today().isoformat()
    prev = {}
    if OUT.exists() and "--force" not in sys.argv:
        with OUT.open("r", encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                prev[r["ingrediente"]] = r
    filas, agotado = [], None
    for rol, ilus, nombre, q_food, q_hist in CANDIDATOS:
        food = "(" + q_food + ") AND " + FOOD
        hist = ANDALUS + " AND " + q_hist
        old = prev.get(nombre, {})
        fila = {
            "rol": rol, "ilustracion": ilus, "ingrediente": nombre,
            "n_alimentos_2016_2020": old.get("n_alimentos_2016_2020", ""),
            "n_alimentos_2021_2025": old.get("n_alimentos_2021_2025", ""),
            "crecimiento": old.get("crecimiento", ""),
            "n_alimentos_2026_parcial": old.get("n_alimentos_2026_parcial", ""),
            "n_enfoque_andalusi": old.get("n_enfoque_andalusi", ""),
            "consulta_alimentos": food, "consulta_andalusi": hist,
            "fecha_consulta": old.get("fecha_consulta") or hoy,
            "fuente": "OpenAlex API, filtro title_and_abstract.search",
            "estado": "completo",
        }
        try:
            if agotado:
                raise PresupuestoAgotado(agotado)
            changed = False
            if fila["n_alimentos_2016_2020"] == "":
                fila["n_alimentos_2016_2020"] = count(food, "2016-2020"); time.sleep(1.2); changed = True
            if fila["n_alimentos_2021_2025"] == "":
                fila["n_alimentos_2021_2025"] = count(food, "2021-2025"); time.sleep(1.2); changed = True
            if fila["n_alimentos_2026_parcial"] == "":
                fila["n_alimentos_2026_parcial"] = count(food, "2026"); time.sleep(1.2); changed = True
            if fila["n_enfoque_andalusi"] == "":
                fila["n_enfoque_andalusi"] = count(hist); time.sleep(1.2); changed = True
            n1, n2 = int(fila["n_alimentos_2016_2020"]), int(fila["n_alimentos_2021_2025"])
            fila["crecimiento"] = round(n2 / n1, 2) if n1 else ""
            if changed:
                fila["fecha_consulta"] = hoy
            print(f"{nombre:48s} {n1:>5} {n2:>5} x{fila['crecimiento']!s:<5} 2026:{fila['n_alimentos_2026_parcial']!s:>4}  andalusí:{fila['n_enfoque_andalusi']!s:>3}")
        except PresupuestoAgotado as e:
            agotado = str(e)
            fila["estado"] = "pendiente: presupuesto diario de OpenAlex agotado"
            print(f"{nombre:48s} pendiente")
        filas.append(fila)
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print("Escrito:", OUT)
    if agotado:
        print("Presupuesto de OpenAlex agotado: vuelve a ejecutar tras la medianoche UTC o con OPENALEX_API_KEY.")


if __name__ == "__main__":
    main()
