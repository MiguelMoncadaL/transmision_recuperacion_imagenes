# Datos del Proyecto

Imágenes de muestra incluidas en la carpeta para ejecutar los scripts de transmisión, ruido y recuperación de imágenes.

Todas las imágenes contenidas en esta carpeta provienen de la base de datos estandarizada **USC-SIPI Image Database** (Volumen *Miscellaneous*).

---

## Imágenes Incluidas

| Archivo | Descripción | Tipo / Formato | Tamaño | ID USC-SIPI |
| :--- | :--- | :--- | :--- | :--- |
| `arbol` | Árbol en el acantilado | Color RGB (24 bits) | 512 x 512 | `4.2.04` (*Tree*) |
| `casa` | Casa residencial | Color RGB (24 bits) | 512 x 512 | `4.2.05` (*House*) |
| `reloj` | Reloj con libros y fotos | Escala de grises (8 bits) | 256 x 256 / 512 x 512 | `5.1.12` / `7.1.10` (*Clock*) |

---

## Enlace y Descarga de Imágenes Adicionales

Si deseas probar el proyecto con más imágenes de la base de datos:

1. Ingresa a la fuente oficial: [USC-SIPI Image Database (Volume 3: Miscellaneous)](https://sipi.usc.edu/database/database.php?volume=misc&image=17#top).
2. Descarga imágenes adicionales (por ejemplo, `4.2.07` *Peppers*, `4.2.03` *Mandrill/Baboon* o `boat.512`).
3. Guárdalas dentro de esta carpeta (`data/`).
4. Ejecuta el script principal (`python main.py`) para seleccionarlas.

---

## Cita y Referencia Bibliográfica

```text
Weber, A. G. (2018). The USC-SIPI Image Database: Version 6 (USC-SIPI Report #432). 
University of Southern California.
```