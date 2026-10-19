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


def add_salt_pepper(image, prob=0.05, seed=None):
    """Ruido impulsivo 'sal y pimienta'.

    prob: probabilidad de que un píxel sea corrompido (la mitad pasa a 0 y
    la otra mitad a 255).
    """
    rng = np.random.default_rng(seed)
    noisy = image.copy()
    r = rng.random(size=image.shape)
    noisy[r < prob / 2] = 0
    noisy[(r >= prob / 2) & (r < prob)] = 255
    return noisy


def image_to_bits(image):
    """Convierte la imagen en un flujo de bits (8 bits por valor)."""
    return np.unpackbits(image.reshape(-1))


def bits_to_image(bits, shape):
    """Reconstruye la imagen a partir de un flujo de bits."""
    return np.packbits(bits).reshape(shape)


def binary_symmetric_channel(bits, p=0.01, seed=None):
    """Canal binario simétrico: cada bit se invierte con probabilidad p."""
    rng = np.random.default_rng(seed)
    flips = (rng.random(size=bits.shape) < p).astype(np.uint8)
    return bits ^ flips


def transmit_bits(image, p=0.01, seed=None):
    """Transmisión digital completa: imagen -> bits -> canal binario ruidoso
    -> bits recibidos -> imagen recibida.

    Devuelve (imagen_recibida, bits_enviados, bits_recibidos).
    """
    sent = image_to_bits(image)
    received = binary_symmetric_channel(sent, p=p, seed=seed)
    return bits_to_image(received, image.shape), sent, received


def transmit(image, channel="awgn", param=None, seed=None):
    """Envía una imagen por el canal elegido y devuelve la imagen recibida.

    channel: 'awgn', 'salt_pepper' o 'bsc'
    param:   sigma (awgn), probabilidad (salt_pepper) o probabilidad de
             error de bit (bsc). Si es None se usa un valor por defecto.
    """
    if channel == "awgn":
        return add_awgn(image, sigma=20.0 if param is None else param, seed=seed)
    if channel == "salt_pepper":
        return add_salt_pepper(image, prob=0.05 if param is None else param, seed=seed)
    if channel == "bsc":
        received, _, _ = transmit_bits(image, p=0.01 if param is None else param, seed=seed)
        return received
    raise ValueError(f"Canal desconocido: {channel}")
