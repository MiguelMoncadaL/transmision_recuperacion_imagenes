"""Lectura, representación numérica y visualización de imágenes."""
from pathlib import Path

import numpy as np
from PIL import Image

def load_image(path, grayscale=False):
    """Lee cualquier imagen (PNG, JPG, TIFF, BMP...) y la devuelve como
    arreglo NumPy de enteros de 8 bits (uint8).

    - Escala de grises: arreglo 2D de forma (alto, ancho)
    - Color (RGB):      arreglo 3D de forma (alto, ancho, 3)

    Cada valor es la intensidad de un píxel entre 0 (negro) y 255 (máximo).
    """
    img = Image.open(path)
    img = img.convert("L" if grayscale else "RGB")
    return np.array(img, dtype=np.uint8)


def save_image(array, path):
    """Guarda un arreglo uint8 como archivo de imagen."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(array).save(path)


def describe_image(array):
    """Devuelve un resumen de cómo se representa la imagen numéricamente."""
    return {
        "forma": array.shape,
        "tipo_de_dato": str(array.dtype),
        "valor_minimo": int(array.min()),
        "valor_maximo": int(array.max()),
        "total_de_pixeles": int(array.shape[0] * array.shape[1]),
        "total_de_bits": int(array.size * 8),
    }



