"""Lectura, representación numérica y visualización de imágenes."""
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
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


def to_gray(image):
    """Convierte una imagen RGB a escala de grises (luminancia).

    Si la imagen ya es 2D se devuelve igual. Se usa para analizar una sola
    señal de intensidad por imagen (por ejemplo, el perfil de una fila).
    """
    if image.ndim == 2:
        return image
    pesos = np.array([0.299, 0.587, 0.114])
    return (image[..., :3] @ pesos).round().astype(np.uint8)



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


def show_comparison(original, received, title_received="Imagen recibida",
                    save_path=None, show=True):
    """Muestra lado a lado la imagen original, la recibida y su diferencia."""
    if not show:
        matplotlib.use("Agg")

    diff = np.abs(original.astype(np.int16) - received.astype(np.int16))
    diff = diff.astype(np.uint8)
    cmap = "gray" if original.ndim == 2 else None

    fig, axes = plt.subplots(1, 3, figsize=(13, 5), layout="constrained")
    axes[0].imshow(original, cmap=cmap, vmin=0, vmax=255)
    axes[0].set_title("Imagen original")
    axes[1].imshow(received, cmap=cmap, vmin=0, vmax=255)
    axes[1].set_title(title_received)
    axes[2].imshow(diff, cmap=cmap, vmin=0, vmax=255)
    axes[2].set_title("Diferencia absoluta")
    for ax in axes:
        ax.axis("off")

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=120)
    if show:
        plt.show()
    plt.close(fig)

