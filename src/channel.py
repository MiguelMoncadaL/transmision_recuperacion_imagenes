"""Modelos del canal con ruido.

El canal recibe una imagen (arreglo uint8) y devuelve la versión degradada
que llegaría al receptor. Funciona con cualquier imagen, sin importar su
tamaño o si es de color o escala de grises.
"""
import numpy as np


def add_awgn(image, sigma=20.0, seed=None):
    """Ruido blanco gaussiano aditivo (AWGN) sobre el valor de cada píxel.

    sigma: desviación estándar del ruido (en niveles de intensidad 0-255).
    """
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, sigma, size=image.shape)
    noisy = image.astype(np.float64) + noise
    return np.clip(noisy, 0, 255).round().astype(np.uint8)

