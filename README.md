# ¡COME! · كُلْ
### Cerámica andalusí del siglo XI, epigrafía cúfica y propuesta gastronómica para Restaurante Noor (Córdoba)

[![Live Demo](https://img.shields.io/badge/Demo_Interactivo-GitHub_Pages-2c6e4f?style=for-the-badge&logo=github)](https://leogallardo97-bit.github.io/zafas-kul-noor/)
[![Investigación](https://img.shields.io/badge/Estudio_Histórico-Pau_Armengol_&_Carmen_Barceló-a8741f?style=for-the-badge)](./Informe_Epigrafia_Ceramica_Alimentacion_alAndalus.md)
[![Propuesta](https://img.shields.io/badge/Propuesta_para-Restaurante_Noor_Córdoba-2a1d22?style=for-the-badge)](./02_Propuesta_Noor_Zafas_Kul/Dossier_Propuesta_Gerencia_Noor.md)

---

## 🌟 [Ver la Maquetación Interactiva en Vivo](https://leogallardo97-bit.github.io/zafas-kul-noor/)

> Puedes interactuar directamente con la pieza: arrastra sobre el guiso para comerlo con el ratón o el dedo (en móvil/tablet), o pulsa *«Comer de un bocado»*. Al terminarse el plato, el fondo desvela la inscripción árabe en verde de cobre con contorno de manganeso.

---

## 📜 Resumen del Proyecto

Este proyecto formula una propuesta conceptual, gastronómica y de servicio de sala para **Restaurante Noor** (3 estrellas Michelin, Córdoba), bajo la dirección y supervisión de **Paco Morales** y **Paola Gualandi**.

El fundamento nace de una serie de **40 zafas cerámicas del siglo XI** (época de las Taifas) estudiadas por Pau Armengol y Carmen Barceló (*Boletín de Arqueología Medieval*, 2024). A diferencia de la vajilla califal cordobesa previa —que portaba fórmulas propiciatorias abstractas (*al-mulk*, *baraka*, *yumn*)—, estas zafas llevaban pintada en el fondo interior una **orden directa y funcional**: el imperativo árabe **كُلْ (*kul*, «¡come!»)** acompañado del nombre del guiso servido.

```
[ GESTO HISTÓRICO (s. XI) ]              [ EXPERIENCIA NOOR ]
Cerámica con mandato directo         ──>  El comensal degusta el guiso
Fondo cubierto por el alimento       ──>  Al rebañar, el fondo queda limpio
Epígrafe: kul + nombre del manjar    ──>  Se desvela el mandato caligráfico
```

---

## 🍲 Los Cuatro Pases de Temporada

Los cuatro pases toman como raíz los cuatro guisos atestiguados en las zafas originales, cruzados con los grandes recetarios andalusíes (*Ibn Razīn al-Tuŷībī* y el *Anónimo Almohade* del siglo XIII). Cada uno suma un **ingrediente de vanguardia**:

1. **Pase I · ¡Come la berenjena! (*Kul al-bāḏinŷān* · كل الباذنجان)**  
   *Inspirado en la baqliyya (guiso de verduras).* Berenjena asada a la brasa y bañada con el jugo del guiso de cordero, cilantro y alcaravea, bajo una costra fina de almendra, huevo y pan.  
   *Vanguardia:* **alcaparra** (hoja, brote y alcaparrón), lactofermentada.
2. **Pase II · ¡Come la calabaza! (*Kul al-qarʿ* · كل القرع)**  
   *Inspirado en la qarʿiyya (guiso de calabaza vinatera, Lagenaria siceraria).* Calabaza de cuello en láminas finas, confitada en la grasa del cordero lechal, con caldo reducido con orégano y tomillo.  
   *Vanguardia:* **semilla verde de cilantro**, fresca o en salmuera ligera.
3. **Pase III · ¡Come la almendra! (*Kul al-lawz* · كل اللوز)**  
   *Inspirado en la ŷulaydiyya («el encostradito»).* Capón o gallina de corral bajo una costra de almendra, yema y pan, horneada en la propia zafa.  
   *Vanguardia:* **alloza** (almendra verde; del árabe *allawza*, «la almendra»), tierna en primavera y encurtida el resto del año.
4. **Pase IV · ¡Come el azafrán! (*Kul al-zaʿfarān* · كل الزعفران)**  
   *Inspirado en la gassāniyya (guiso de al-Gassānī).* Transición hacia el dulce: sémola en caldo de cordero con miel, azafrán y canela, láminas de almendra y yema curada.  
   *Vanguardia:* **tépalo de la flor del azafrán**, pendiente de confirmar con AESAN si cuenta como nuevo alimento.

La portada (*kul baqliyya*, la inscripción documentada) suma la **verdolaga**, *al-baqla al-ḥamqāʾ*, de la misma raíz que *baqliyya*.

---

## 🌱 Despensa de vanguardia

Cada ingrediente cumple cuatro criterios:

1. Está documentado en el siglo XI andalusí: en el tratado agrícola de Ibn Baṣṣāl o en letrinas de los siglos X a XII de Córdoba, Mértola, Badajoz y Almería (Peralta-Gómez *et al.*, *Vegetation History and Archaeobotany*, 2026).
2. Apenas se ha estudiado desde la historia de al-Andalus: entre 0 y 5 trabajos en OpenAlex.
3. Su investigación en ciencia de los alimentos crece entre 1,7 y 2,3 veces de 2016–2020 a 2021–2025.
4. Es viable en la cocina de Noor.

Los recuentos y las consultas exactas están en [`bibliometria_ingredientes_openalex.csv`](./bibliometria_ingredientes_openalex.csv). Se pueden repetir con [`scripts/bibliometria_ingredientes_openalex.py`](./scripts/bibliometria_ingredientes_openalex.py) y contrastar en Scopus con [`scripts/bibliometria_ingredientes_scopus.py`](./scripts/bibliometria_ingredientes_scopus.py), que necesita la clave de Elsevier.

---

## 📂 Contenido del Repositorio

* [**`index.html`**](./index.html): **Maquetación interactiva** de 16 láminas, lista para navegador, pantalla táctil o impresión a PDF en formato lámina. Es la única fuente: las copias se generan con [`scripts/sincronizar_copias.py`](./scripts/sincronizar_copias.py).
* [**`assets/`**](./assets/): tipografías alojadas en el propio sitio (SIL Open Font License, con sus licencias), favicon e imágenes.
* [**`02_Propuesta_Noor_Zafas_Kul/`**](./02_Propuesta_Noor_Zafas_Kul/):
  * `Dossier_Propuesta_Gerencia_Noor.md`: Dossier técnico y de desarrollo de Noor (justificación arqueológica, especificaciones de alfarería sin plomo, diseño de pases, ingredientes de vanguardia, guion de sala de 30 segundos y plan de trabajo).
  * `index.html`: Copia de respaldo de la presentación.
* [**`02_Propuesta_Noor_Kul/`**](./02_Propuesta_Noor_Kul/): copia autónoma para abrir con doble clic y sin conexión (`Kul_Noor_presentacion.html`), PDF y enlaces.
* [**`Informe_Epigrafia_Ceramica_Alimentacion_alAndalus.md`**](./Informe_Epigrafia_Ceramica_Alimentacion_alAndalus.md): Informe científico de base sobre epigrafía andalusí, análisis tipológico y bibliometría en OpenAlex, con la bibliometría de los ingredientes (§2.9).
* [**`01_Articulos_PDF/`**](./01_Articulos_PDF/): Corpus de artículos científicos descargados y ordenados por carpetas temáticas con índices en CSV y Excel.
* [**`scripts/`**](./scripts/): bibliometría de los ingredientes (OpenAlex y Scopus), posproceso de imágenes con metadatos de autoría y sincronización de copias.

---

## 🏺 Especificaciones de la Zafa

* **Morfología:** Zafa (*ṣaḥfa*), cuenco semiesférico de base anular y borde engrosado al exterior.
* **Tallas:**
  * *Zafa de pase (degustación individual):* Ø 160 mm, altura 60 mm.
  * *Zafa de mesa (pase compartido al centro):* Ø 275 mm, altura 120 mm. Las originales, de 250 a 300 mm, admitían de 2 a 3 kg para 6 a 12 comensales; en Noor, de 1,2 a 1,8 kg por servicio para 4 a 8.
* **Esmalte y Vidriado:** Vidriado blanco de estaño (*tin-opacified glaze*) en el interior, 100% libre de plomo según normativa alimentaria CE.
* **Técnica pictórica:** Verde de cobre y manganeso sobre blanco. Caligrafía cúfica trazada artesanalmente por maestro calígrafo.

---
*Autoría: **Restaurante Noor** · Dirección y supervisión: **Paco Morales** y **Paola Gualandi** · Octubre de 2026.*
