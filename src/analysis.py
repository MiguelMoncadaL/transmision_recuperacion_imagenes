"""Caracterización de la imagen vista como señal.

Una imagen en escala de grises es una señal bidimensional discreta f[m, n]:
muestreada en el espacio (una muestra por píxel) y cuantizada en amplitud
(256 niveles posibles, 8 bits por muestra).
"""
import numpy as np

from src.image_io import to_gray


def characterize(image):
    """Características básicas de la señal (equivalente a las que se piden
    para una señal temporal: mínimo, máximo, media, número de muestras...)."""
    alto, ancho = image.shape[:2]
    canales = 1 if image.ndim == 2 else image.shape[2]
    datos = image.astype(np.float64)
    return {
        "Alto (muestras en vertical)": alto,
        "Ancho (muestras en horizontal)": ancho,
        "Canales": canales,
        "Número total de muestras": int(image.size),
        "Bits por muestra": 8,
        "Niveles de cuantización": 256,
        "Total de bits": int(image.size * 8),
        "Mínimo": int(image.min()),
        "Máximo": int(image.max()),
        "Media (nivel DC)": float(datos.mean()),
        "Desviación estándar": float(datos.std()),
        "Potencia media (x^2)": float(np.mean(datos ** 2)),
    }


def noise_statistics(original, received):
    """Estadísticas del error e[m, n] = recibida - original (ruido efectivo).

    Sirve para verificar los parámetros del canal: por ejemplo, en AWGN la
    media del error debe ser cercana a 0 y su desviación cercana a sigma.
    """
    error = received.astype(np.float64) - original.astype(np.float64)
    return {
        "Media del error": float(error.mean()),
        "Desviación estándar del error": float(error.std()),
        "Porcentaje de muestras alteradas": float(100 * np.mean(error != 0)),
    }


def row_profile(image, row=None):
    """Fila de la imagen como señal 1D: intensidad vs. posición horizontal."""
    gris = to_gray(image)
    if row is None:
        row = gris.shape[0] // 2
    row = int(np.clip(row, 0, gris.shape[0] - 1))
    return gris[row, :], row
