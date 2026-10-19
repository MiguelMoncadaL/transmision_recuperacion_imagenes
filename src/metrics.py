"""Métricas para comparar la imagen original con la imagen recibida
(y, más adelante, con la imagen recuperada)."""
import numpy as np


def mse(original, other):
    """Error cuadrático medio. 0 = imágenes idénticas."""
    diff = original.astype(np.float64) - other.astype(np.float64)
    return float(np.mean(diff ** 2))


def psnr(original, other, max_value=255.0):
    """Relación pico señal a ruido en dB. Más alto = más parecida."""
    error = mse(original, other)
    if error == 0:
        return float("inf")
    return float(10 * np.log10(max_value ** 2 / error))


def snr(original, other):
    """Relación señal a ruido en dB (potencia de la señal / potencia del error)."""
    signal_power = np.mean(original.astype(np.float64) ** 2)
    noise_power = mse(original, other)
    if noise_power == 0:
        return float("inf")
    return float(10 * np.log10(signal_power / noise_power))


def bit_error_rate(bits_sent, bits_received):
    """Fracción de bits que llegaron con error."""
    return float(np.mean(bits_sent != bits_received))


def evaluate(original, other):
    """Devuelve un diccionario con las métricas principales."""
    return {"MSE": mse(original, other),
            "PSNR (dB)": psnr(original, other),
            "SNR (dB)": snr(original, other)}
